"""P2: easter-egg route is hidden unless HCL_P2_EASTER is set."""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

os.environ.setdefault("CS_UNIVERSE_API_TOKEN", "p1-test-token-hex")
os.environ["CS_UNIVERSE_DB_PATH"] = str(
    _ROOT / "data" / "test_p2_easter_unittest.db"
)


class P2EasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from carbon_silicon_universe import api_app
        from carbon_silicon_universe.confirm_sync import get_db_connection

        _ = get_db_connection()
        cls.client = api_app.API_APP.test_client()

    def test_easter_off_is_404(self) -> None:
        os.environ.pop("HCL_P2_EASTER", None)
        r = self.client.get("/api/p2/easter-egg")
        self.assertEqual(r.status_code, 404)

    def test_easter_on_is_json_200(self) -> None:
        os.environ["HCL_P2_EASTER"] = "1"
        r = self.client.get("/api/p2/easter-egg")
        self.assertEqual(r.status_code, 200)
        j = r.get_json()
        self.assertEqual(j.get("p2"), "easter-egg")
        self.assertIn("lines", j)


if __name__ == "__main__":
    unittest.main()
