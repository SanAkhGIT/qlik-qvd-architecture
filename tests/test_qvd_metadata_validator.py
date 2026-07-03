from pathlib import Path

from python.qvd_metadata_validator import read_qvd_metadata, validate


SAMPLE_HEADER = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<QvdTableHeader>\n<RecordByteSize>42</RecordByteSize>\n<NoOfRecords>3</NoOfRecords>\n<CreateUtcTime>2026-09-04T00:00:00.000Z</CreateUtcTime>\n<SourceFileSize>123</SourceFileSize>\n<Fields>\n<QvdFieldHeader>\n<FieldName>OrderID</FieldName>\n<BitOffset>0</BitOffset>\n<BitWidth>8</BitWidth>\n<NoOfSymbols>3</NoOfSymbols>\n</QvdFieldHeader>\n<QvdFieldHeader>\n<FieldName>SalesAmount</FieldName>\n<BitOffset>8</BitOffset>\n<BitWidth>16</BitWidth>\n<NoOfSymbols>3</NoOfSymbols>\n</QvdFieldHeader>\n</Fields>\n</QvdTableHeader>\n'''


def test_reads_qvd_header(tmp_path: Path) -> None:
    qvd = tmp_path / "FactOrders.qvd"
    qvd.write_bytes(SAMPLE_HEADER + b"\x00" + b"binary-data")

    metadata = read_qvd_metadata(qvd)

    assert metadata.no_of_records == 3
    assert metadata.record_byte_size == 42
    assert [field.name for field in metadata.fields] == ["OrderID", "SalesAmount"]
    assert metadata.header_size_bytes == len(SAMPLE_HEADER) + 1


def test_validates_required_fields(tmp_path: Path) -> None:
    qvd = tmp_path / "FactOrders.qvd"
    qvd.write_bytes(SAMPLE_HEADER + b"\x00" + b"binary-data")
    metadata = read_qvd_metadata(qvd)

    assert validate(metadata, min_records=1, expected_fields=["OrderID", "SalesAmount"]) == []
    assert validate(metadata, min_records=1, expected_fields=["OrderID", "MissingField"])
