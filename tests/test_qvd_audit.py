import json
from pathlib import Path

from python.qvd_audit import build_audit, write_outputs


def test_audit_creates_run_metadata(tmp_path: Path) -> None:
    header = b'''<?xml version="1.0"?><QvdTableHeader><RecordByteSize>10</RecordByteSize><NoOfRecords>2</NoOfRecords><CreateUtcTime>2026-09-04T00:00:00.000Z</CreateUtcTime><Fields><QvdFieldHeader><FieldName>OrderID</FieldName><NoOfSymbols>2</NoOfSymbols></QvdFieldHeader></Fields></QvdTableHeader>'''
    qvd_dir = tmp_path / "qvd"
    qvd_dir.mkdir()
    (qvd_dir / "FactOrders.qvd").write_bytes(header + b"\x00" + b"data")

    audit = build_audit(qvd_dir, 1, None)
    assert audit["status"] == "PASS"
    assert audit["qvd_count"] == 1
    assert audit["results"][0]["record_count"] == 2
    assert audit["results"][0]["status"] == "PASS"
    assert audit["run_id"]

    json_out = tmp_path / "audit.json"
    csv_out = tmp_path / "audit.csv"
    write_outputs(audit, json_out, csv_out)
    assert json.loads(json_out.read_text())["run_id"] == audit["run_id"]
    assert "run_id,q" not in csv_out.read_text()
