"""Carbon–Silicon Alliance (碳硅同盟 / 硅碳同盟) — machine-readable design summary for APIs."""

from __future__ import annotations

import sys
from typing import Any

# Bump when `docs/CARBON_SILICON_ALLIANCE_REDESIGN.md` meaningfully changes.
ARCHITECTURE_META_VERSION = 1

_ARCHITECTURE_RESPONSE_META: dict[str, Any] = {
    "schema_version": ARCHITECTURE_META_VERSION,
    "alliance_name_en": "Carbon–Silicon Alliance",
    "alliance_names_zh": ["碳硅同盟", "硅碳同盟"],
    "naming_note_zh": "「硅碳」与「碳硅」指同一同盟；代码包名保持 carbon_silicon 前缀。",
    "hcl_role": (
        "HCL: Rust swarm kernel (core/) + Python 12L control plane "
        "(carbon_silicon_universe)."
    ),
    "design_document": "docs/CARBON_SILICON_ALLIANCE_REDESIGN.md",
    "layers_model": "12_fixed_tiers_L1_L12_no_extension",
    "bands": {
        "L1_L8": "constitutional_and_infrastructure_core",
        "L9_L12": "commercial_operations_delivery_consciousness",
    },
    "p1_python_surface_layers": [2, 4, 8, 10, 11, 12],
}


def architecture_response_meta() -> dict[str, Any]:
    """
    JSON-serializable blob embedded under ``data.meta`` for ``GET /api/architecture/layers``.
    Returns a shallow copy so callers cannot mutate the process-wide template.
    """
    return _ARCHITECTURE_RESPONSE_META.copy()


def public_version_payload() -> dict[str, Any]:
    """Safe, unauthenticated build slice for ``GET /api/version`` (no tokens or paths)."""
    return {
        "service": "hcl-carbon-silicon",
        "python_version": (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        ),
        "architecture_meta_version": ARCHITECTURE_META_VERSION,
    }
