# RTT dual dedup — SHA-1(prompt,response) + semantic similarity > 0.95.
# Observation plugin only. No /core-axioms/ I/O.
"""Collapse collusion / near-duplicate samples."""

from __future__ import annotations

import hashlib
from difflib import SequenceMatcher
from typing import Iterable


def pair_sha1(prompt: str, response: str) -> str:
    blob = (prompt + "\0" + response).encode("utf-8")
    return hashlib.sha1(blob).hexdigest()


def semantic_sim(a: str, b: str) -> float:
    """Sealed similarity: SequenceMatcher ratio. Threshold 0.95."""
    if not a and not b:
        return 1.0
    return SequenceMatcher(None, a, b).ratio()


def dedup_samples(rows: Iterable[dict]) -> list[dict]:
    """
    1) Same SHA-1(prompt,response) appearing >3 times counts as 1.
    2) semantic sim > 0.95 → merge as homologous perturbation.
    """
    by_hash: dict[str, list[dict]] = {}
    for row in rows:
        h = pair_sha1(row.get("prompt", ""), row.get("response", ""))
        by_hash.setdefault(h, []).append(row)

    collapsed: list[dict] = []
    for _h, group in by_hash.items():
        collapsed.append(group[0])  # >3 times still 1

    merged: list[dict] = []
    for row in collapsed:
        text = (row.get("prompt", "") + " " + row.get("response", "")).strip()
        hit = None
        for i, kept in enumerate(merged):
            ktext = (kept.get("prompt", "") + " " + kept.get("response", "")).strip()
            if semantic_sim(text, ktext) > 0.95:
                hit = i
                break
        if hit is None:
            merged.append(row)
    return merged
