"""Static checks for deterministic incremental-load design decisions."""
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "qlik" / "04_incremental_orders.qvs"


def test_incremental_script_has_deterministic_tie_breaker() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert "FirstSortedValue" in text
    assert "ModifiedTimestamp" in text
    assert "OrderID" in text
    assert "TieBreak" in text or "ModifiedSequence" in text or "ChangeSequence" in text


def test_incremental_script_documents_delete_limitation() -> None:
    text = SCRIPT.read_text(encoding="utf-8").lower()
    assert "delete" in text
