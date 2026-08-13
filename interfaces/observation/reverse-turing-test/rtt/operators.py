# RTT operators — T-02 six-layer controls (sealed). Observation plugin only.
# Denied: /core-axioms/ I/O, axiom derivation, grading, certification.
"""ReadScore, D_info, Gain_info, P_pure, SE, quarterly ρ rebuild."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Iterable, Sequence

# --- sealed numeric constants (WeChat final) ---
GAIN_INFO_ELASTIC = 0.10
RHO_REBUILD = 0.60
OMEGA_LAMBDA_FLAP = 0.08
SE_BLOCK = 0.15
HOLLOW_FLOOR = 4.0  # D_info below this is hollow
HOLLOW_KAPPA = 0.85
READSCORE_ADMIT = 0.35
PURE_WEIGHTS = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)

_TERM_RE = re.compile(
    r"(SHA-?256|SHA-?1|RTT|CI|API|SE|FIFO|NLP|T-02|Y-04|ReadScore|D_info|P_pure)",
    re.I,
)
_ENTITY_RE = re.compile(
    r"[A-Z][A-Za-z0-9_\-]{1,}|[\u4e00-\u9fff]{2,}|[0-9]+(?:\.[0-9]+)?",
)


def thousand_entity_density(text: str) -> float:
    """D_info = 1000 * n_entities / n_chars (千实体密度)."""
    n_chars = max(len(text.strip()), 1)
    n_ent = len(_ENTITY_RE.findall(text))
    return 1000.0 * n_ent / n_chars


def sentence_len(text: str) -> float:
    parts = [p for p in re.split(r"[。！？.!?;；\n]+", text) if p.strip()]
    if not parts:
        return 0.0
    return sum(len(p) for p in parts) / len(parts)


def layer_count(text: str) -> int:
    return max(1, len(re.findall(r"(?m)^(#{1,6}\s|[-*]\s|\d+\.\s)", text)) or text.count("\n") + 1)


def term_count(text: str) -> int:
    return len(_TERM_RE.findall(text))


def _z(x: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


@dataclass
class ReadScoreWeights:
    omega: float = 0.30
    lam: float = 0.30
    gamma: float = 0.20
    delta: float = 0.20

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.omega, self.lam, self.gamma, self.delta)

    def normalized(self) -> "ReadScoreWeights":
        s = self.omega + self.lam + self.gamma + self.delta
        if s <= 0:
            return ReadScoreWeights()
        return ReadScoreWeights(self.omega / s, self.lam / s, self.gamma / s, self.delta / s)


@dataclass
class TextFeatures:
    text_id: str
    text: str
    sentence_len: float
    layers: int
    terms: int
    d_info: float
    readscore_raw: float
    readscore_final: float
    below_threshold: bool
    se_omega: float = 0.0
    se_lambda: float = 0.0
    se_gamma: float = 0.0
    se_delta: float = 0.0


def readscore_raw(text: str, w: ReadScoreWeights | None = None) -> float:
    """ReadScore_raw = ω z(len) + λ z(layers) + γ z(terms) + δ z(D_info)."""
    w = (w or ReadScoreWeights()).normalized()
    d = thousand_entity_density(text)
    return (
        w.omega * _z(sentence_len(text), 8.0, 80.0)
        + w.lam * _z(float(layer_count(text)), 1.0, 12.0)
        + w.gamma * _z(float(term_count(text)), 0.0, 8.0)
        + w.delta * _z(d, 1.0, 80.0)
    )


def readscore_final(text: str, w: ReadScoreWeights | None = None) -> float:
    """ReadScore_final = ReadScore_raw * (1 - κ * hollow). D_info 负向压制空洞文本."""
    raw = readscore_raw(text, w)
    d = thousand_entity_density(text)
    hollow = max(0.0, HOLLOW_FLOOR - d) / HOLLOW_FLOOR
    return raw * (1.0 - HOLLOW_KAPPA * hollow)


def gain_info(d_before: float, d_after: float) -> float:
    base = max(abs(d_before), 1e-9)
    return (d_after - d_before) / base


def dual_admit(
    d_before: float,
    d_after: float,
    text: str,
    w: ReadScoreWeights | None = None,
    gain_ref: float = 0.0,
) -> tuple[bool, dict]:
    """Gain_info ±10% elastic band AND ReadScore_final admission."""
    g = gain_info(d_before, d_after)
    band = GAIN_INFO_ELASTIC * max(abs(gain_ref), 1.0)
    gain_ok = abs(g - gain_ref) <= band
    final = readscore_final(text, w)
    score_ok = final >= READSCORE_ADMIT
    return gain_ok and score_ok, {
        "Gain_info": g,
        "gain_ok": gain_ok,
        "ReadScore_final": final,
        "score_ok": score_ok,
    }


def p_pure(r_anth: float, h_halluc: float, i_false: float) -> float:
    """P_pure uses ONLY R_anth, H_halluc, I_false. ReadScore never enters."""
    w1, w2, w3 = PURE_WEIGHTS
    val = 1.0 - (w1 * r_anth + w2 * h_halluc + w3 * i_false)
    return max(0.0, min(1.0, val))


def linreg_slope_se(x: Sequence[float], y: Sequence[float]) -> tuple[float, float]:
    n = len(x)
    if n < 3:
        return 0.0, 1.0
    mx = sum(x) / n
    my = sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    if sxx <= 0:
        return 0.0, 1.0
    slope = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sxx
    intercept = my - slope * mx
    sse = sum((yi - (intercept + slope * xi)) ** 2 for xi, yi in zip(x, y))
    sigma2 = sse / (n - 2)
    se = math.sqrt(sigma2 / sxx)
    return slope, se


def any_se_blocks(ses: Iterable[float]) -> bool:
    return any(se > SE_BLOCK for se in ses)


def quarterly_rebuild(rho: float, w: ReadScoreWeights, x: Sequence[float], y: Sequence[float]) -> ReadScoreWeights:
    """ρ < 0.6 → rebuild ReadScore weights from calibration pairs."""
    if rho >= RHO_REBUILD:
        return w.normalized()
    slope, _se = linreg_slope_se(x, y)
    adj = max(0.05, min(0.90, 0.5 + 0.5 * math.tanh(slope)))
    rebuilt = ReadScoreWeights(adj, 1.0 - adj / 2.0, 0.15, 0.15)
    return rebuilt.normalized()


def weight_flap_triggers_expand(prev: ReadScoreWeights, cur: ReadScoreWeights) -> bool:
    return abs(cur.omega - prev.omega) > OMEGA_LAMBDA_FLAP or abs(cur.lam - prev.lam) > OMEGA_LAMBDA_FLAP


def extract_features(text_id: str, text: str, w: ReadScoreWeights | None = None, ses: dict | None = None) -> TextFeatures:
    w = w or ReadScoreWeights()
    ses = ses or {}
    raw = readscore_raw(text, w)
    final = readscore_final(text, w)
    return TextFeatures(
        text_id=text_id,
        text=text,
        sentence_len=sentence_len(text),
        layers=layer_count(text),
        terms=term_count(text),
        d_info=thousand_entity_density(text),
        readscore_raw=raw,
        readscore_final=final,
        below_threshold=final < READSCORE_ADMIT,
        se_omega=float(ses.get("omega", 0.0)),
        se_lambda=float(ses.get("lam", 0.0)),
        se_gamma=float(ses.get("gamma", 0.0)),
        se_delta=float(ses.get("delta", 0.0)),
    )
