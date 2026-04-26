"""P1: smoke tests for liveness, readiness, and P1 static admin route."""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

# python/ on path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Deterministic token for test client
os.environ["CS_UNIVERSE_API_TOKEN"] = "p1-test-token-hex"


class P1APITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from carbon_silicon_universe.confirm_config import UNIVERSE_API_TOKEN
        from carbon_silicon_universe import api_app

        assert UNIVERSE_API_TOKEN == "p1-test-token-hex"
        # Avoid long startup side effects: patch system_startup in __main__ not used here
        from carbon_silicon_universe.confirm_sync import get_db_connection

        _ = get_db_connection()
        cls.client = api_app.API_APP.test_client()

    def test_live(self) -> None:
        r = self.client.get("/api/health/live")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["status"], "live")

    def test_ready(self) -> None:
        r = self.client.get("/api/health/ready")
        self.assertIn(r.status_code, (200, 503))
        if r.status_code == 200:
            self.assertEqual(r.get_json()["status"], "ready")

    def test_p1_admin_served(self) -> None:
        r = self.client.get("/p1/")
        self.assertEqual(r.status_code, 200)
        text = r.get_data(as_text=True)
        self.assertIn("HCL", text)
        self.assertIn("P1", text)

    def test_ops_p1_with_token(self) -> None:
        r = self.client.get(
            "/api/ops/p1", headers={"X-CS-Token": "p1-test-token-hex"}
        )
        self.assertEqual(r.status_code, 200)
        d = r.get_json()["data"]
        self.assertIn("p1", d)
        self.assertIn("rust_core", d)


if __name__ == "__main__":
    unittest.main()
