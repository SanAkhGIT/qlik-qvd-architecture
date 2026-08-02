"""Ensure committed sample extracts match the deterministic generator."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).parents[1]


def test_generated_orders_match_committed_sample() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        script = ROOT / "python" / "generate_data.py"
        result = subprocess.run([sys.executable, str(script)], cwd=work, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        generated = work / "data" / "sample" / "orders.csv"
        committed = ROOT / "data" / "sample" / "orders.csv"
        assert generated.read_bytes() == committed.read_bytes()
