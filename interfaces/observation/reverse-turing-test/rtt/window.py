# RTT 70% self-reference window — file lock, FIFO, peak rules. Plugin only.
# No qualitative grading output. Axiom-core directory I/O denied at identity layer.
"""Round window, exclusive lock, peak freeze/review."""

from __future__ import annotations

import json
import os
import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path

from .identity import RTT_ROOT

SAMPLES_PER_ROUND = 10
WINDOW_ROUNDS = 5
VAR_MAX = 0.02
RANGE_MAX = 0.05
LOCK_TIMEOUT_SEC = 30
PEAK_HIGH = 0.70
PEAK_DROP = 0.65
DELTA_REVIEW = 0.15

LOCK_PATH = RTT_ROOT / "window.lock"
QUEUE_PATH = RTT_ROOT / "window.fifo.jsonl"
STATE_PATH = RTT_ROOT / "window.state.json"


@dataclass
class WindowState:
    rounds: list[float] = field(default_factory=list)
    frozen: bool = False
    weak_confidence: bool = False
    baseline_review: bool = False
    last_round: float | None = None


def _lock_acquire(handle, timeout: float = LOCK_TIMEOUT_SEC) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if os.name == "nt":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            time.sleep(0.05)
    return False


def _lock_release(handle) -> None:
    try:
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError:
        pass


def load_state() -> WindowState:
    if not STATE_PATH.exists():
        return WindowState()
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return WindowState(**data)


def save_state(state: WindowState) -> None:
    STATE_PATH.write_text(
        json.dumps(state.__dict__, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def round_weight(samples: list[float]) -> float:
    if len(samples) != SAMPLES_PER_ROUND:
        raise ValueError("每10个有效样本 = 1轮")
    return sum(samples) / SAMPLES_PER_ROUND


def window_ok(rounds: list[float]) -> bool:
    if len(rounds) < WINDOW_ROUNDS:
        return False
    w = rounds[-WINDOW_ROUNDS:]
    var = statistics.pvariance(w) if len(w) > 1 else 0.0
    rng = max(w) - min(w)
    return var < VAR_MAX and rng < RANGE_MAX


def apply_peak_rules(prev: float | None, cur: float, state: WindowState) -> WindowState:
    if prev is not None:
        if prev > PEAK_HIGH and cur < PEAK_DROP:
            state.frozen = True
            state.weak_confidence = True
        if abs(cur - prev) > DELTA_REVIEW:
            state.baseline_review = True
    return state


def enqueue(payload: dict) -> None:
    with QUEUE_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def process_queue() -> WindowState:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCK_PATH.touch(exist_ok=True)
    with LOCK_PATH.open("r+") as handle:
        got = _lock_acquire(handle, LOCK_TIMEOUT_SEC)
        state = load_state()
        if not got:
            baseline = state.last_round
            state = WindowState(rounds=[baseline] if baseline is not None else [], last_round=baseline)
            save_state(state)
            if QUEUE_PATH.exists():
                QUEUE_PATH.write_text("", encoding="utf-8")
            return state
        try:
            if QUEUE_PATH.exists():
                lines = [ln for ln in QUEUE_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
                QUEUE_PATH.write_text("", encoding="utf-8")
            else:
                lines = []
            buf: list[float] = []
            for ln in lines:
                rec = json.loads(ln)
                buf.append(float(rec["value"]))
                if len(buf) == SAMPLES_PER_ROUND:
                    prev = state.last_round
                    cur = round_weight(buf)
                    state = apply_peak_rules(prev, cur, state)
                    if not state.frozen:
                        state.rounds.append(cur)
                        state.last_round = cur
                    buf = []
            save_state(state)
            return state
        finally:
            _lock_release(handle)
