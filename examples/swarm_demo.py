"""
Basic async swarm simulation (no external dependencies beyond stdlib).
Run: python examples/swarm_demo.py
"""

from __future__ import annotations

import argparse
import asyncio
import random


async def _crayfish_task(agent_id: int) -> str:
    await asyncio.sleep(random.uniform(0.02, 0.12))
    return f"crayfish-{agent_id}"


async def _run(n: int) -> None:
    print(f"[HCL] Spawning {n} concurrent agent tasks (demo)…")
    results = await asyncio.gather(*(_crayfish_task(i) for i in range(n)))
    print(f"[HCL] Done: {', '.join(results)}")


def main() -> None:
    p = argparse.ArgumentParser(description="HCL swarm demo")
    p.add_argument(
        "-n",
        "--agents",
        type=int,
        default=8,
        help="Number of parallel demo agents (default: 8)",
    )
    args = p.parse_args()
    n = max(1, min(args.agents, 256))
    asyncio.run(_run(n))


if __name__ == "__main__":
    main()
