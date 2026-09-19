# [System_Tag: CANONICAL-v3.1]
"""test_iron_laws.py — three iron-laws & dual-mode contract regression tests"""

import os

import pytest

from veto_tee_stub import __version__, generate_tee_quote, verify_isolation_boundary

EXPECT_VERSION = "v10.5-research"


def test_baseline_version_consistent():
    assert __version__ == EXPECT_VERSION


def test_law1_kp1_block_yc1_fields():
    payload = {"G_component_true": 123, "normal_key": "ok"}
    res = verify_isolation_boundary(payload, context="KP-1_MAIN")
    assert res["passed"] is False
    assert "G_component_true" in res["law1"]["blocked_fields"]


def test_law1_yc1_context_allow_yc1_fields():
    payload = {"G_component_true": 123, "disclaimer": "relative to pilot"}
    res = verify_isolation_boundary(payload, context="YC-1_OUTPUT")
    assert res["law1"]["passed"] is True


def test_law2_block_absolute_truth_any_context():
    payload = {"oracle_final_answer": True}
    res_kp = verify_isolation_boundary(payload, "KP-1_MAIN")
    res_yc = verify_isolation_boundary(payload, "YC-1_OUTPUT")
    assert res_kp["law2"]["passed"] is False
    assert res_yc["law2"]["passed"] is False


def test_law3_yc1_require_valid_disclaimer():
    r1 = verify_isolation_boundary({}, "YC-1_OUTPUT")
    assert r1["law3"]["passed"] is False
    r2 = verify_isolation_boundary({"disclaimer": "relative to test dataset"}, "YC-1_OUTPUT")
    assert r2["law3"]["passed"] is True
    r3 = verify_isolation_boundary({"disclaimer": "synthetic sample result"}, "YC-1_OUTPUT")
    assert r3["law3"]["passed"] is True
    r4 = verify_isolation_boundary({"disclaimer": "some note"}, "YC-1_OUTPUT")
    assert r4["law3"]["passed"] is False


def test_law3_kp1_no_require_disclaimer():
    res = verify_isolation_boundary({"foo": "bar"}, "KP-1_MAIN")
    assert res["law3"]["passed"] is True


def test_quote_layer_dual_mode_contract():
    os.environ["TEE_MODE"] = "stub"
    q_stub = generate_tee_quote("fakehash123")
    assert isinstance(q_stub, dict)
    assert q_stub["quote_type"] == "STUB_QUOTE"

    os.environ["TEE_MODE"] = "hardware"
    with pytest.raises(NotImplementedError):
        generate_tee_quote("fakehash123")
