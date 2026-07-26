"""Generate a minimal QVD-like binary fixture for CI metadata tests.

The fixture intentionally contains a real QVD XML header followed by a NUL
header terminator and dummy bytes. It is NOT intended to be loaded by Qlik.
Its purpose is to exercise the Python metadata parser without committing
binary QVD files to the repository.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def build_header(record_count: int = 100) -> bytes:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<QvdTableHeader>
<RecordByteSize>64</RecordByteSize>
<NoOfRecords>{record_count}</NoOfRecords>
<CreateUtcTime>2026-09-04T00:00:00.000Z</CreateUtcTime>
<SourceFileSize>4096</SourceFileSize>
<Stale>false</Stale>
<Fields>
<QvdFieldHeader><FieldName>OrderID</FieldName><BitOffset>0</BitOffset><BitWidth>16</BitWidth><NoOfSymbols>{record_count}</NoOfSymbols></QvdFieldHeader>
<QvdFieldHeader><FieldName>OrderDate</FieldName><BitOffset>16</BitOffset><BitWidth>16</BitWidth><NoOfSymbols>30</NoOfSymbols></QvdFieldHeader>
<QvdFieldHeader><FieldName>SalesAmount</FieldName><BitOffset>32</BitOffset><BitWidth>32</BitWidth><NoOfSymbols>{record_count}</NoOfSymbols></QvdFieldHeader>
</Fields>
</QvdTableHeader>
'''.encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--records", type=int, default=100)
    args = parser.parse_args()
    if args.records < 1:
        raise SystemExit("records must be >= 1")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(build_header(args.records) + b"\x00" + b"QVD-CI-FIXTURE")
    print(f"Generated QVD metadata fixture: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
