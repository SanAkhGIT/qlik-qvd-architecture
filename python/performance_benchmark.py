"""Validate and summarise measured Qlik performance benchmarks.

This tool deliberately does not generate synthetic performance numbers.
It converts measurements captured in a target Qlik environment into a
review-friendly summary.
"""

import argparse
import csv
import json
from pathlib import Path

REQUIRED_METRICS = {
    "source_rows_read",
    "reload_duration_seconds",
    "qvd_size_bytes",
    "ram_peak_mb",
    "app_response_seconds",
}


def load_measurements(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate(rows):
    errors = []
    if not rows:
        return ["No measurements found; collect benchmarks in a real Qlik environment."]

    for index, row in enumerate(rows, start=2):
        missing = [
            field
            for field in ("scenario", "metric", "baseline_value", "optimised_value", "unit", "environment", "measured_at")
            if not row.get(field)
        ]
        if missing:
            errors.append(f"row {index}: missing {', '.join(missing)}")
        if row.get("metric") and row["metric"] not in REQUIRED_METRICS:
            errors.append(f"row {index}: unsupported metric '{row['metric']}'")
        for field in ("baseline_value", "optimised_value"):
            if row.get(field):
                try:
                    float(row[field])
                except ValueError:
                    errors.append(f"row {index}: {field} must be numeric")
    return errors


def summarise(rows):
    summary = []
    for row in rows:
        baseline = float(row["baseline_value"])
        optimised = float(row["optimised_value"])
        delta = optimised - baseline
        pct = None if baseline == 0 else (delta / baseline) * 100
        summary.append({
            "scenario": row["scenario"],
            "metric": row["metric"],
            "baseline": baseline,
            "optimised": optimised,
            "unit": row["unit"],
            "delta": delta,
            "delta_percent": pct,
            "environment": row["environment"],
            "measured_at": row["measured_at"],
        })
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    rows = load_measurements(args.input)
    errors = validate(rows)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    report = {"measurement_count": len(rows), "results": summarise(rows)}
    print(json.dumps(report, indent=2))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
