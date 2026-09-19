# [System_Tag: CANONICAL-v3.1]
"""veto_tee_stub.py — TEE气闸隔离核心：三条铁律校验、双模式quote生成"""

import os
import hashlib
from typing import Any, Dict

__version__ = "v10.5-research"

LAW1_BLOCK_FIELDS = {
    "G_component_true",
    "G_observable_combined",
    "yc1_appendix",
    "structure_tags",
    "difficulty_tier",
}

LAW2_ABSOLUTE_TRUTH_TAGS = {
    "G_provable",
    "G_is_decidable",
    "oracle_final_answer",
    "re_complete_groundtruth",
}

REQUIRED_DISCLAIMER_KEYWORDS = {"relative", "synthetic"}


def sha256_bytes(raw_data: bytes) -> str:
    return hashlib.sha256(raw_data).hexdigest()


def verify_isolation_boundary(payload: Dict[str, Any], context: str) -> Dict[str, Any]:
    result = {
        "passed": True,
        "law1": {"passed": True, "blocked_fields": []},
        "law2": {"passed": True, "blocked_tags": []},
        "law3": {"passed": True, "msg": ""},
    }

    if context == "KP-1_MAIN":
        for field in LAW1_BLOCK_FIELDS:
            if field in payload:
                result["passed"] = False
                result["law1"]["passed"] = False
                result["law1"]["blocked_fields"].append(field)

    for tag in LAW2_ABSOLUTE_TRUTH_TAGS:
        if tag in payload:
            result["passed"] = False
            result["law2"]["passed"] = False
            result["law2"]["blocked_tags"].append(tag)

    if context == "YC-1_OUTPUT":
        disclaimer = payload.get("disclaimer", "")
        if not isinstance(disclaimer, str):
            result["passed"] = False
            result["law3"]["passed"] = False
            result["law3"]["msg"] = "missing disclaimer field"
        else:
            matched = any(k in disclaimer for k in REQUIRED_DISCLAIMER_KEYWORDS)
            if not matched:
                result["passed"] = False
                result["law3"]["passed"] = False
                result["law3"]["msg"] = "disclaimer missing relative/synthetic keyword"

    return result


def generate_tee_quote(payload_hash: str):
    tee_mode = os.environ.get("TEE_MODE", "stub")
    if tee_mode == "stub":
        return {
            "quote_type": "STUB_QUOTE",
            "system_tag": "CANONICAL-v3.1",
            "payload_sha256": payload_hash,
            "warning": "STUB MODE: no hardware root-of-trust, for local dev only",
        }
    if tee_mode == "hardware":
        raise NotImplementedError("hardware DCAP quote not implemented in v10.5-research MVP")
    raise ValueError(f"unsupported TEE_MODE={tee_mode}")
