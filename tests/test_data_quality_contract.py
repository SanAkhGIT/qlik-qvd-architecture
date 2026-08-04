"""Guardrails for the Qlik data-quality gate."""
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "qlik" / "05_data_quality.qvs"


def test_orders_quality_gate_covers_key_integrity_rules() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    required = [
        "DistinctOrderIDs",
        "NullOrderIDs",
        "OrphanCustomerReferences",
        "OrphanProductReferences",
        "InvalidDates",
        "InvalidQuantities",
        "InvalidSalesAmounts",
    ]
    for rule in required:
        assert rule in text, f"Missing DQ rule: {rule}"


def test_quality_gate_can_fail_the_reload() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert "vDQFailOnError" in text
    assert "EXIT SCRIPT" in text
    assert "DATA QUALITY FAILURE" in text


def test_audit_qvds_are_persisted() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert "DQ_Orders.qvd" in text
    assert "DQ_Customers.qvd" in text
    assert "DQ_Products.qvd" in text
