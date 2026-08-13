"""RTT operator and gate unit tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rtt.accounts import Sample, disc, w_si_global
from rtt.dedup import dedup_samples, pair_sha1
from rtt.gates import GateBlocked, SceneCounts, assert_monthly_ratio, assert_scene_quota, assert_se_gate
from rtt.identity import PINNED_DISCLAIMER, assert_not_core_axioms
from rtt.nlp_guard import intercept, is_high_risk
from rtt.operators import dual_admit, p_pure, readscore_final, thousand_entity_density
from rtt.report import bind_footer, fingerprint16
from rtt.window import apply_peak_rules, round_weight, window_ok, WindowState


class TestOperators(unittest.TestCase):
    def test_d_info_and_purity_isolation(self) -> None:
        d = thousand_entity_density("RTT SHA-256 CI API 实体密度测试样本")
        self.assertGreater(d, 0)
        p = p_pure(0.1, 0.2, 0.3)
        self.assertTrue(0 <= p <= 1)
        # ReadScore must not be an argument of p_pure
        self.assertEqual(p_pure.__code__.co_argcount, 3)

    def test_dual_admit_and_final(self) -> None:
        text = "结构化观测样本。包含 RTT CI API SE 术语。\n## 层\n- a\n- b"
        ok, detail = dual_admit(10.0, 10.5, text)
        self.assertIn("ReadScore_final", detail)
        self.assertGreaterEqual(readscore_final(text), 0.0)

    def test_core_axioms_denied(self) -> None:
        with self.assertRaises(PermissionError):
            assert_not_core_axioms("foo/core-axioms/bar")

    def test_scene_and_se_block(self) -> None:
        with self.assertRaises(GateBlocked):
            assert_scene_quota(SceneCounts(10, 10, 10))
        assert_scene_quota(SceneCounts(67, 67, 50))
        with self.assertRaises(GateBlocked):
            assert_se_gate({"omega": 0.2})
        assert_monthly_ratio(SceneCounts(4, 4, 2))

    def test_window_peak_dedup_disc(self) -> None:
        self.assertAlmostEqual(round_weight([0.1] * 10), 0.1)
        self.assertTrue(window_ok([0.40, 0.41, 0.40, 0.42, 0.41]))
        st = apply_peak_rules(0.71, 0.60, WindowState())
        self.assertTrue(st.frozen and st.weak_confidence)
        st2 = apply_peak_rules(0.50, 0.70, WindowState())
        self.assertTrue(st2.baseline_review)
        self.assertEqual(disc(3, 0.10), 0.5 * 0.6)
        rows = [{"prompt": "p", "response": "r"}] * 5
        self.assertEqual(len(dedup_samples(rows)), 1)
        self.assertEqual(pair_sha1("p", "r"), pair_sha1("p", "r"))
        w = w_si_global([Sample("a", 0.4, "b1")] * 12 + [Sample("c", 0.2, "b1")])
        self.assertGreater(w, 0)

    def test_nlp_and_footer(self) -> None:
        self.assertTrue(is_high_risk("该模型 RTT分数 达到认证 等级"))
        self.assertFalse(is_high_risk("仅输出微调数据"))
        out = bind_footer("hello")
        self.assertIn("DOC_FP16=", out)
        self.assertEqual(len(fingerprint16("hello")), 16)
        self.assertIn("接口层量化观测", PINNED_DISCLAIMER)

    def test_intercept_combo(self) -> None:
        r = intercept("普通观测文本")
        self.assertFalse(r["flagged"])


if __name__ == "__main__":
    unittest.main()
