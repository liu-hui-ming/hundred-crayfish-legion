# RTT report footer — undeletable hash warning + 16-char fingerprint.
# Residual risk: screenshot-copy of text fingerprint can bypass. Phase-2 visual watermark not in this release.
"""Bind report footer hash warning."""

from __future__ import annotations

import hashlib

WARNING = (
    "【不可删除哈希警示】本报告为接口层量化观测输出，不构成觉知判定、文明等级、"
    "资质认证或商业背书。指纹绑定如下。当前版本：截图抄写文字指纹可绕过校验；"
    "完整视觉水印封堵纳入二期迭代，本次不实现、不隐瞒、不造假。"
)


def fingerprint16(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def sha256_full(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def bind_footer(body: str) -> str:
    fp = fingerprint16(body)
    digest = sha256_full(body)
    return (
        body.rstrip()
        + "\n\n"
        + WARNING
        + f"\nSHA-256={digest}\nDOC_FP16={fp}\n"
    )
