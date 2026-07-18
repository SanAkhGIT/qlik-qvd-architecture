"""Create an auditable JSON/CSV record from QVD metadata validation results.

This is intentionally independent of Qlik runtime execution. It is designed to
run immediately before a Qlik reload and provide a machine-readable decision:
PASS means the Qlik pipeline may proceed; FAIL means the reload should be
blocked by the calling orchestrator.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from qvd_metadata_validator import iter_qvds, load_expected_fields, read_qvd_metadata, validate


def build_audit(path: Path, min_records: int, contract_path: Path | None) -> dict:
    run_id = str(uuid.uuid4())
    started = datetime.now(timezone.utc)
    contract = load_expected_fields(contract_path) if contract_path else {}
    results = []
    overall_pass = True

    for qvd in iter_qvds(path):
        try:
            metadata = read_qvd_metadata(qvd)
            expected = contract.get(qvd.name)
            errors = validate(metadata, min_records, expected)
            valid = not errors
            row = {
                "run_id": run_id,
                "checked_at_utc": started.isoformat(),
                "qvd": str(qvd),
                "status": "PASS" if valid else "FAIL",
                "record_count": metadata.no_of_records,
                "field_count": len(metadata.fields),
                "file_size_bytes": metadata.file_size_bytes,
                "header_size_bytes": metadata.header_size_bytes,
                "create_utc_time": metadata.create_utc_time,
                "stale": metadata.stale,
                "errors": errors,
            }
        except (OSError, ValueError) as exc:
            valid = False
            row = {
                "run_id": run_id,
                "checked_at_utc": started.isoformat(),
                "qvd": str(qvd),
                "status": "FAIL",
                "record_count": None,
                "field_count": None,
                "file_size_bytes": qvd.stat().st_size if qvd.exists() else None,
                "header_size_bytes": None,
                "create_utc_time": None,
                "stale": None,
                "errors": [str(exc)],
            }
        overall_pass &= valid
        results.append(row)

    return {
        "run_id": run_id,
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if overall_pass and results else "FAIL",
        "qvd_count": len(results),
        "results": results,
    }


def write_outputs(audit: dict, json_path: Path | None, csv_path: Path | None) -> None:
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    if csv_path:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        rows = audit["results"]
        fields = [
            "run_id", "checked_at_utc", "qvd", "status", "record_count",
            "field_count", "file_size_bytes", "header_size_bytes",
            "create_utc_time", "stale", "errors",
        ]
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                output = dict(row)
                output["errors"] = "; ".join(output["errors"])
                writer.writerow(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an audit record from QVD preflight validation")
    parser.add_argument("--path", required=True, type=Path)
    parser.add_argument("--expected-fields", type=Path)
    parser.add_argument("--min-records", type=int, default=1)
    parser.add_argument("--json-out", type=Path, default=Path("artifacts/qvd_audit.json"))
    parser.add_argument("--csv-out", type=Path, default=Path("artifacts/qvd_audit.csv"))
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: path does not exist: {args.path}", file=sys.stderr)
        return 2

    try:
        audit = build_audit(args.path, args.min_records, args.expected_fields)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: audit failed: {exc}", file=sys.stderr)
        return 2

    write_outputs(audit, args.json_out, args.csv_out)
    print(f"QVD audit run {audit['run_id']}: {audit['status']}")
    print(f"QVDs checked: {audit['qvd_count']}")
    print(f"JSON: {args.json_out}")
    print(f"CSV:  {args.csv_out}")
    return 0 if audit["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
