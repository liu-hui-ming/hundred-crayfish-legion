"""Unit tests for P1 bounded asyncio swarm (no Flask)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


class P1SwarmModuleTest(unittest.IsolatedAsyncioTestCase):
    async def test_run_bounded_returns_sorted_and_positive_elapsed(self) -> None:
        from carbon_silicon_universe.p1_swarm import run_bounded_crayfish_swarm

        results, elapsed_ms = await run_bounded_crayfish_swarm(6, 2)
        self.assertEqual(len(results), 6)
        self.assertEqual([r["id"] for r in results], [0, 1, 2, 3, 4, 5])
        self.assertGreater(elapsed_ms, 0.0)

    def test_clamp_respects_caps(self) -> None:
        from carbon_silicon_universe.p1_swarm import MAX_SWARM_IN_FLIGHT, MAX_SWARM_N, clamp_swarm_params

        n, c = clamp_swarm_params(10_000, 500)
        self.assertEqual(n, MAX_SWARM_N)
        self.assertEqual(c, MAX_SWARM_IN_FLIGHT)


if __name__ == "__main__":
    unittest.main()
