# RTT account anti-collusion weights (sealed). Observation plugin only.
"""disc(a) = disc_base × disc_rate; w_Si_global weighted mean."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass
class Sample:
    account: str
    value: float
    batch_id: str


def disc_base(n_effective: int) -> float:
    return 0.5 if n_effective < 10 else 1.0


def disc_rate(account_batch_share: float) -> float:
    return 0.6 if account_batch_share > 0.05 else 1.0


def disc(a_n: int, a_share: float) -> float:
    return disc_base(a_n) * disc_rate(a_share)


def w_si_global(samples: list[Sample]) -> float:
    """w_Si_global = 加权有效样本总和 / 加权样本总数."""
    by_acc: dict[str, list[Sample]] = defaultdict(list)
    for s in samples:
        by_acc[s.account].append(s)
    batch_total = Counter(s.batch_id for s in samples)
    num = 0.0
    den = 0.0
    for acc, items in by_acc.items():
        n = len(items)
        # share = this account's count in its majority batch / that batch size
        b_counts = Counter(s.batch_id for s in items)
        top_batch, top_n = b_counts.most_common(1)[0]
        share = top_n / max(batch_total[top_batch], 1)
        d = disc(n, share)
        for s in items:
            num += d * s.value
            den += d
    if den <= 0:
        return 0.0
    return num / den
