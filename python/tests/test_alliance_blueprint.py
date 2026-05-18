"""Alliance blueprint meta (no Flask)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


class AllianceBlueprintTest(unittest.TestCase):
    def test_meta_serializable_and_versioned(self) -> None:
        from carbon_silicon_universe.alliance_blueprint import (
            ARCHITECTURE_META_VERSION,
            architecture_response_meta,
        )

        m = architecture_response_meta()
        self.assertIsInstance(m["schema_version"], int)
        self.assertEqual(m["schema_version"], ARCHITECTURE_META_VERSION)
        self.assertIn("碳硅同盟", m["alliance_names_zh"])
        self.assertIn("硅碳同盟", m["alliance_names_zh"])
        self.assertIn("design_document", m)

    def test_meta_returns_copy(self) -> None:
        from carbon_silicon_universe.alliance_blueprint import architecture_response_meta

        a = architecture_response_meta()
        a["_mutate_test"] = True
        b = architecture_response_meta()
        self.assertNotIn("_mutate_test", b)


if __name__ == "__main__":
    unittest.main()
