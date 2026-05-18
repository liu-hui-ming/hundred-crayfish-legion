"""P1: bounded-concurrency crayfish swarm (stdlib asyncio), aligned with Rust `CrayfishSwarm` demo."""

from __future__ import annotations

import asyncio
import time
from typing import Any

# API / UI guardrails (abuse-resistant defaults)
MAX_SWARM_N = 64
MAX_SWARM_IN_FLIGHT = 32


def clamp_swarm_params(n: int, max_in_flight: int) -> tuple[int, int]:
    n_clamped = max(1, min(int(n), MAX_SWARM_N))
    cap = max(1, min(int(max_in_flight), MAX_SWARM_IN_FLIGHT))
    return n_clamped, cap


async def run_bounded_crayfish_swarm(
    n: int, max_in_flight: int
) -> tuple[list[dict[str, Any]], float]:
    """
    Run ``n`` async agent ticks with at most ``max_in_flight`` concurrent.
    Returns ``(results_sorted_by_id, elapsed_ms)``.
    """
    n, cap = clamp_swarm_params(n, max_in_flight)
    sem = asyncio.Semaphore(cap)

    async def one(agent_id: int) -> dict[str, Any]:
        async with sem:
            ms = 20 + (agent_id % 6) * 20
            await asyncio.sleep(ms / 1000.0)
            return {"id": agent_id, "label": f"crayfish-{agent_id}"}

    t0 = time.perf_counter()
    raw = await asyncio.gather(*(one(i) for i in range(n)))
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
    return sorted(raw, key=lambda x: int(x["id"])), elapsed_ms
