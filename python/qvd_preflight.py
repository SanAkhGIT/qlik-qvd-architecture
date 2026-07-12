"""Run QVD metadata checks as a pipeline preflight gate."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from qvd_metadata_validator import iter_qvds, load_expected_fields, read_qvd_metadata, validate


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate QVD metadata before a Qlik reload")
    parser.add_argument("--path", required=True, type=Path, help="QVD file or directory")
    parser.add_argument("--contract", required=True, type=Path, help="JSON metadata contract")
    parser.add_argument("--min-records", type=int, default=1)
    args = parser.parse_args()

    if not args.path.exists():
        print(f"PREFLIGHT FAIL: path does not exist: {args.path}", file=sys.stderr)
        return 2
    if not args.contract.exists():
        print(f"PREFLIGHT FAIL: contract does not exist: {args.contract}", file=sys.stderr)
        return 2

    try:
        contract = load_expected_fields(args.contract)
    except Exception as exc:
        print(f"PREFLIGHT FAIL: invalid contract: {exc}", file=sys.stderr)
        return 2

    qvds = iter_qvds(args.path)
    if not qvds:
        print(f"PREFLIGHT FAIL: no QVD files found under {args.path}", file=sys.stderr)
        return 2

    failed = False
    print("QVD METADATA PREFLIGHT")
    print("=" * 24)
    for qvd in qvds:
        try:
            metadata = read_qvd_metadata(qvd)
            expected = contract.get(qvd.name, [])
            errors = validate(metadata, args.min_records, expected)
        except Exception as exc:
            errors = [str(exc)]

        if errors:
            failed = True
            print(f"FAIL  {qvd.name}")
            for error in errors:
                print(f"      - {error}")
        else:
            print(f"PASS  {qvd.name} | records={metadata.no_of_records} | fields={len(metadata.fields)}")

    print("=" * 24)
    print("PREFLIGHT FAILED" if failed else "PREFLIGHT PASSED")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
