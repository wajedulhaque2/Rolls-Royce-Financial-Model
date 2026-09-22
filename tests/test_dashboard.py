from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dashboard"))
from model import value_per_share  # noqa: E402


class WorkbookReconciliation(unittest.TestCase):
    def test_dcf_and_saved_checks_reconcile(self) -> None:
        data = json.loads((ROOT / "dashboard" / "data" / "snapshot.json").read_text())
        value, terminal_share = value_per_share(data, data["base_wacc"], data["base_growth"])
        self.assertAlmostEqual(value, data["cached_dcf"], places=10)
        self.assertAlmostEqual(terminal_share, data["terminal_ev_share"], places=10)
        self.assertEqual(data["reference_date"], "2026-06-30")
        self.assertEqual(len(data["checks"]), 13)
        self.assertTrue(all(item["status"] == "PASS" for item in data["checks"]))

    def test_views_and_dark_mode_render(self) -> None:
        app = AppTest.from_file(str(ROOT / "dashboard" / "app.py"), default_timeout=30).run()
        self.assertFalse(app.exception)
        for view in ("Operating forecast", "DCF sensitivity", "Sources & checks"):
            app.radio[0].set_value(view).run()
            self.assertFalse(app.exception, view)
        app.toggle[0].set_value(True).run()
        self.assertFalse(app.exception)
        self.assertTrue(app.toggle[0].value)


if __name__ == "__main__":
    unittest.main()
