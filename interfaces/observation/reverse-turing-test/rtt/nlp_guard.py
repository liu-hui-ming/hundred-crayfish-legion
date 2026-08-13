# RTT NLP high-risk intercept. Observation plugin only.
# Intercept combination: RTT分数 + 认证/等级/资质/觉醒.
"""High-risk semantic guard; FP/FN logging hooks."""

from __future__ import annotations

import re

from .audit import log_fn, log_fp

SCORE_RE = re.compile(r"(RTT\s*分数|RTT\s*score|RTT分数)", re.I)
CERT_RE = re.compile(r"(认证|等级|资质|觉醒|certification|grade|qualif|awaken)", re.I)


def is_high_risk(text: str) -> bool:
    return bool(SCORE_RE.search(text) and CERT_RE.search(text))


def intercept(text: str, human_label: bool | None = None) -> dict:
    """
    human_label: True if human confirms high-risk (for FP/FN).
    误判率硬性红线 <5% is computed from FP/FN logs, not guessed here.
    """
    flagged = is_high_risk(text)
    if human_label is True and not flagged:
        log_fn(text)
    if human_label is False and flagged:
        log_fp(text)
    return {
        "flagged": flagged,
        "action": "block" if flagged else "pass",
        "human_review": flagged,
    }


def misclassification_rate(fp: int, fn: int, n: int) -> float:
    if n <= 0:
        return 1.0
    return (fp + fn) / n


def assert_error_rate_redline(fp: int, fn: int, n: int) -> None:
    rate = misclassification_rate(fp, fn, n)
    if rate >= 0.05:
        raise RuntimeError(f"NLP误判率 {rate:.4f} 未低于 5% 红线")
