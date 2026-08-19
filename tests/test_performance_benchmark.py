import tempfile
import unittest
from pathlib import Path

from python.performance_benchmark import load_measurements, summarise, validate


class TestPerformanceBenchmark(unittest.TestCase):
    def test_empty_template_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "measurements.csv"
            path.write_text("scenario,metric,baseline_value,optimised_value,unit,environment,measured_at,notes\n", encoding="utf-8")
            self.assertTrue(validate(load_measurements(path)))

    def test_measured_values_are_summarised(self):
        rows = [{
            "scenario": "raw_vs_qvd",
            "metric": "reload_duration_seconds",
            "baseline_value": "100",
            "optimised_value": "70",
            "unit": "seconds",
            "environment": "test",
            "measured_at": "2026-09-04",
            "notes": "example test measurement",
        }]
        self.assertEqual(validate(rows), [])
        result = summarise(rows)[0]
        self.assertEqual(result["delta"], -30)
        self.assertEqual(result["delta_percent"], -30)


if __name__ == "__main__":
    unittest.main()
