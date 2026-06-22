"""Static validation for the Qlik project structure.

This does not execute Qlik Sense. It catches common portfolio/repository errors:
missing layer scripts, broken Must_Include targets, incorrect load ordering, and
an application script that bypasses the semantic layer.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
QLIK = ROOT / "qlik"
CONFIG = ROOT / "config"

REQUIRED_SCRIPTS = [
    "00_master_reload.qvs",
    "01_raw.qvs",
    "02_transform.qvs",
    "03_semantic.qvs",
    "04_incremental_orders.qvs",
    "05_data_quality.qvs",
    "06_app_load.qvs",
]


def read(name: str) -> str:
    path = QLIK / name
    assert path.exists(), f"Missing Qlik script: {path}"
    return path.read_text(encoding="utf-8")


def main() -> None:
    for name in REQUIRED_SCRIPTS:
        read(name)

    environment = CONFIG / "environment.qvs"
    assert environment.exists(), "Missing config/environment.qvs"

    master = read("00_master_reload.qvs")
    expected_order = [
        "01_raw.qvs",
        "02_transform.qvs",
        "05_data_quality.qvs",
        "03_semantic.qvs",
    ]
    positions = []
    for script in expected_order:
        match = re.search(re.escape(script), master)
        assert match, f"Master reload does not reference {script}"
        positions.append(match.start())
    assert positions == sorted(positions), "Master reload layer order is incorrect"

    for name in REQUIRED_SCRIPTS:
        content = read(name)
        includes = re.findall(r"Must_Include=([^);]+)", content)
        for include in includes:
            if include.startswith("lib://"):
                continue
            include_path = ROOT / include.strip("[]'\"")
            assert include_path.exists(), f"Broken Must_Include in {name}: {include}"

    app = read("06_app_load.qvs")
    assert "vSemanticQvdPath" in app, "Application script must load semantic QVDs"
    assert "vSourcePath" not in app, "Application script must not read source files directly"
    assert "orders.csv" not in app, "Application script must not bypass semantic QVDs"

    environment_text = environment.read_text(encoding="utf-8")
    for variable in ("vSourcePath", "vRawQvdPath", "vTransformQvdPath", "vSemanticQvdPath"):
        assert variable in environment_text, f"Missing environment variable: {variable}"

    print("Static Qlik structure validation passed.")


if __name__ == "__main__":
    main()
