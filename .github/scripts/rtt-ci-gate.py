#!/usr/bin/env python3
# RTT identity gate — byte-identical copy used by pre-commit AND CI.
# MD5 of this file must match its twin. Observation plugin only.
# Denied: /core-axioms/ I/O, axiom derivation, grading, certification.
"""Shared pre-commit / CI gate for RTT."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve()
# Resolve repo root: this file lives in either
#   interfaces/observation/reverse-turing-test/scripts/pre-commit-gate.py
# or .github/scripts/rtt-ci-gate.py
if REPO.parent.name == "scripts" and REPO.parent.parent.name == "reverse-turing-test":
    RTT_ROOT = REPO.parent.parent
    ROOT = RTT_ROOT.parents[2]
else:
    ROOT = REPO.parents[2]
    RTT_ROOT = ROOT / "interfaces" / "observation" / "reverse-turing-test"

TWIN_A = ROOT / "interfaces" / "observation" / "reverse-turing-test" / "scripts" / "pre-commit-gate.py"
TWIN_B = ROOT / ".github" / "scripts" / "rtt-ci-gate.py"
HASHLOCK = RTT_ROOT / "HASHLOCK.sha256"
MANIFEST = RTT_ROOT / "scene_manifest.json"


def md5_bytes(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def check_twins() -> None:
    if not TWIN_A.exists() or not TWIN_B.exists():
        raise SystemExit("pre-commit / CI twin scripts missing")
    if md5_bytes(TWIN_A) != md5_bytes(TWIN_B):
        raise SystemExit("pre-commit 与 CI 脚本 MD5 不同源，拒绝继续")


def check_hashlock() -> None:
    if not HASHLOCK.exists():
        raise SystemExit("HASHLOCK.sha256 missing")
    expected = {}
    for ln in HASHLOCK.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        digest, rel = ln.split("  ", 1)
        expected[rel.replace("\\", "/")] = digest
    py_files = sorted((RTT_ROOT / "rtt").glob("*.py"))
    for p in py_files:
        rel = p.relative_to(ROOT).as_posix()
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if expected.get(rel) != got:
            raise SystemExit(f"SHA-256 hash lock failed: {rel}")


def check_no_core_axioms() -> None:
    for p in (RTT_ROOT / "rtt").glob("*.py"):
        text = p.read_text(encoding="utf-8")
        if "open(" in text and "core-axioms" in text.replace("\\", "/"):
            raise SystemExit(f"core-axioms I/O detected: {p}")


def check_scene_manifest() -> None:
    if not MANIFEST.exists():
        return
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    qa = int(data.get("qa", 0))
    reason = int(data.get("reason", 0))
    tool = int(data.get("tool", 0))
    ses = {k: float(v) for k, v in (data.get("se") or {}).items()}
    sys.path.insert(0, str(RTT_ROOT))
    from rtt.gates import GateBlocked, SceneCounts, assert_scene_quota, assert_se_gate

    try:
        assert_scene_quota(SceneCounts(qa, reason, tool))
        if ses:
            assert_se_gate(ses)
    except GateBlocked as e:
        raise SystemExit(str(e)) from e


def main() -> int:
    check_twins()
    check_no_core_axioms()
    check_hashlock()
    check_scene_manifest()
    print("RTT identity gate PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
