"""Inspect and validate QVD file metadata without loading QVD records.

The QVD format stores an XML header before the compressed/binary data section.
This utility reads only that header, so it is suitable for lightweight pre-load
checks in a Qlik pipeline. It uses only the Python standard library.

Examples:
    python python/qvd_metadata_validator.py --path ./qvd/semantic
    python python/qvd_metadata_validator.py --path ./qvd/semantic --json
    python python/qvd_metadata_validator.py --path ./qvd/semantic --min-records 1
    python python/qvd_metadata_validator.py --path ./qvd/semantic --expected-fields tests/qvd_contract.json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


@dataclass
class QvdField:
    name: str
    bit_offset: int | None = None
    bit_width: int | None = None
    bias: int | None = None
    no_of_symbols: int | None = None
    number_format: str | None = None


@dataclass
class QvdMetadata:
    path: str
    file_size_bytes: int
    header_size_bytes: int
    record_byte_size: int | None
    no_of_records: int | None
    create_utc_time: str | None
    source_file_size: int | None
    stale: str | None
    fields: list[QvdField]


def _text(parent: ET.Element, name: str) -> str | None:
    node = parent.find(name)
    if node is None or node.text is None:
        return None
    value = node.text.strip()
    return value or None


def _int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def read_qvd_metadata(path: Path) -> QvdMetadata:
    """Read the QVD XML header and return metadata; do not parse data rows."""
    with path.open("rb") as handle:
        data = handle.read()

    terminator = data.find(b"\x00")
    if terminator < 0:
        raise ValueError("QVD header terminator (NUL byte) was not found")

    header_bytes = data[:terminator]
    try:
        root = ET.fromstring(header_bytes)
    except ET.ParseError as exc:
        raise ValueError(f"invalid QVD XML header: {exc}") from exc

    if root.tag != "QvdTableHeader":
        raise ValueError(f"unexpected QVD root element: {root.tag!r}")

    fields_parent = root.find("Fields")
    fields: list[QvdField] = []
    if fields_parent is not None:
        for field_node in fields_parent.findall("QvdFieldHeader"):
            name = _text(field_node, "FieldName")
            if not name:
                raise ValueError("QvdFieldHeader is missing FieldName")
            fields.append(
                QvdField(
                    name=name,
                    bit_offset=_int(_text(field_node, "BitOffset")),
                    bit_width=_int(_text(field_node, "BitWidth")),
                    bias=_int(_text(field_node, "Bias")),
                    no_of_symbols=_int(_text(field_node, "NoOfSymbols")),
                    number_format=_text(field_node, "NumberFormat"),
                )
            )

    return QvdMetadata(
        path=str(path),
        file_size_bytes=path.stat().st_size,
        header_size_bytes=terminator + 1,
        record_byte_size=_int(_text(root, "RecordByteSize")),
        no_of_records=_int(_text(root, "NoOfRecords")),
        create_utc_time=_text(root, "CreateUtcTime"),
        source_file_size=_int(_text(root, "SourceFileSize")),
        stale=_text(root, "Stale"),
        fields=fields,
    )


def load_expected_fields(path: Path) -> dict[str, list[str]]:
    """Load {filename: [field, ...]} expectations from a small JSON contract."""
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("expected-fields JSON must contain an object")
    return value


def validate(
    metadata: QvdMetadata,
    min_records: int,
    expected_fields: list[str] | None,
) -> list[str]:
    errors: list[str] = []
    names = [field.name for field in metadata.fields]

    if metadata.file_size_bytes <= metadata.header_size_bytes:
        errors.append("file contains no data section after the QVD header")
    if metadata.no_of_records is None:
        errors.append("NoOfRecords is missing or not numeric")
    elif metadata.no_of_records < min_records:
        errors.append(
            f"NoOfRecords={metadata.no_of_records} is below minimum {min_records}"
        )
    if not names:
        errors.append("QVD contains no field definitions")
    if len(names) != len(set(names)):
        errors.append("duplicate field names detected")

    if expected_fields:
        missing = [name for name in expected_fields if name not in names]
        if missing:
            errors.append(f"missing expected fields: {', '.join(missing)}")

    return errors


def serialise(metadata: QvdMetadata) -> dict[str, Any]:
    return asdict(metadata)


def iter_qvds(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() == ".qvd" else []
    return sorted(path.rglob("*.qvd"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read and validate QVD metadata")
    parser.add_argument("--path", required=True, type=Path, help="QVD file or directory")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--min-records", type=int, default=1)
    parser.add_argument(
        "--expected-fields",
        type=Path,
        help="JSON contract mapping QVD filename to required field names",
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: path does not exist: {args.path}", file=sys.stderr)
        return 2

    qvds = iter_qvds(args.path)
    if not qvds:
        print(f"ERROR: no .qvd files found under {args.path}", file=sys.stderr)
        return 2

    try:
        contract = load_expected_fields(args.expected_fields) if args.expected_fields else {}
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: cannot read expected-fields contract: {exc}", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    failed = False
    for qvd in qvds:
        try:
            metadata = read_qvd_metadata(qvd)
            expected = contract.get(qvd.name)
            if expected is not None and not isinstance(expected, list):
                raise ValueError(f"contract entry for {qvd.name} must be a list")
            errors = validate(metadata, args.min_records, expected)
            failed |= bool(errors)
            result = serialise(metadata)
            result["valid"] = not errors
            result["errors"] = errors
        except (OSError, ValueError, ET.ParseError) as exc:
            failed = True
            result = {"path": str(qvd), "valid": False, "errors": [str(exc)]}
        results.append(result)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(f"\n{result['path']}")
            if not result["valid"]:
                print("  STATUS: FAIL")
                for error in result["errors"]:
                    print(f"  - {error}")
                continue
            print("  STATUS: PASS")
            print(f"  Records: {result.get('no_of_records')}")
            print(f"  Fields:  {len(result.get('fields', []))}")
            print(f"  Size:    {result.get('file_size_bytes')} bytes")
            print("  Field names: " + ", ".join(field["name"] for field in result["fields"]))

        print(f"\nChecked {len(results)} QVD file(s): {'FAIL' if failed else 'PASS'}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
