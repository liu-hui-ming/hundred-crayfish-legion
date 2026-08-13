# RTT package — statistical observation plugin. No /core-axioms/ I/O.
"""Reverse Turing Test observation operators."""

from .accounts import Sample, disc, w_si_global
from .dedup import dedup_samples
from .gates import GateBlocked, SceneCounts, assert_scene_quota, assert_se_gate, assert_monthly_ratio
from .identity import PINNED_DISCLAIMER, RESIDUAL_RISK, assert_not_core_axioms, assert_plugin_identity
from .nlp_guard import intercept
from .operators import (
    dual_admit,
    p_pure,
    quarterly_rebuild,
    readscore_final,
    thousand_entity_density,
)
from .report import bind_footer
from .window import process_queue, window_ok

__all__ = [
    "PINNED_DISCLAIMER",
    "RESIDUAL_RISK",
    "GateBlocked",
    "SceneCounts",
    "Sample",
    "assert_not_core_axioms",
    "assert_plugin_identity",
    "assert_scene_quota",
    "assert_se_gate",
    "assert_monthly_ratio",
    "bind_footer",
    "dedup_samples",
    "disc",
    "dual_admit",
    "intercept",
    "p_pure",
    "process_queue",
    "quarterly_rebuild",
    "readscore_final",
    "thousand_entity_density",
    "w_si_global",
    "window_ok",
]
