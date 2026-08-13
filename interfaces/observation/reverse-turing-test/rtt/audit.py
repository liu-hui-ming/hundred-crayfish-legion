# RTT FP/FN append-only audit. Monthly 10% desensitization. Blind-review archive.
# Observation plugin only. Logs are never deleted by this module.
"""Immutable FP/FN logs and monthly desensitize."""

from __future__ import annotations

import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from .identity import RTT_ROOT

AUDIT = RTT_ROOT / "audit"
FP_LOG = AUDIT / "fp.log.jsonl"
FN_LOG = AUDIT / "fn.log.jsonl"
DESENSE_DIR = AUDIT / "desensitized"
BLIND_DIR = AUDIT / "blind-review"
README_RO = BLIND_DIR / "README.md"


def _append(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rec = dict(rec)
    rec["ts"] = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _mask(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"[REDACTED:{h}]"


def log_fp(text: str) -> None:
    _append(FP_LOG, {"kind": "FP", "text": text})


def log_fn(text: str) -> None:
    _append(FN_LOG, {"kind": "FN", "text": text})


def count_logs() -> tuple[int, int]:
    fp = FN = 0
    if FP_LOG.exists():
        fp = sum(1 for ln in FP_LOG.read_text(encoding="utf-8").splitlines() if ln.strip())
    if FN_LOG.exists():
        FN = sum(1 for ln in FN_LOG.read_text(encoding="utf-8").splitlines() if ln.strip())
    return fp, FN


def monthly_desensitize(rng: random.Random | None = None, month: str | None = None) -> Path | None:
    """Random 10% of combined logs, masked, archived."""
    rng = rng or random.Random()
    month = month or datetime.now(timezone.utc).strftime("%Y-%m")
    rows = []
    for path, kind in ((FP_LOG, "FP"), (FN_LOG, "FN")):
        if not path.exists():
            continue
        for ln in path.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            rec = json.loads(ln)
            rec["kind"] = kind
            rows.append(rec)
    if not rows:
        return None
    k = max(1, int(round(len(rows) * 0.10)))
    picked = rng.sample(rows, min(k, len(rows)))
    out_rows = []
    for rec in picked:
        out_rows.append(
            {
                "kind": rec.get("kind"),
                "ts": rec.get("ts"),
                "text": _mask(str(rec.get("text", ""))),
            }
        )
    DESENSE_DIR.mkdir(parents=True, exist_ok=True)
    out = DESENSE_DIR / f"{month}.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for rec in out_rows:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    BLIND_DIR.mkdir(parents=True, exist_ok=True)
    if not README_RO.exists():
        README_RO.write_text(
            "盲审结果公开只读归档。脱敏样本交由完全独立社区志愿者盲审。"
            "本目录只读，杜绝内部操纵数据。\n",
            encoding="utf-8",
        )
    return out
