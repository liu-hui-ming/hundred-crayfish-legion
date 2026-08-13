# tests/test_source_identity.py — real GitHub API checks (sealed RTT CI).
"""Three live checks: twin MD5, remote protection, e2e intercept."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "interfaces" / "observation" / "reverse-turing-test") not in sys.path:
    sys.path.insert(0, str(ROOT / "interfaces" / "observation" / "reverse-turing-test"))

from rtt.gates import GateBlocked, SceneCounts, assert_scene_quota  # noqa: E402

REPO = "liu-hui-ming/hundred-crayfish-legion"
TWIN_A = ROOT / "interfaces" / "observation" / "reverse-turing-test" / "scripts" / "pre-commit-gate.py"
TWIN_B = ROOT / ".github" / "scripts" / "rtt-ci-gate.py"
API = "https://api.github.com"


def _md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def _gh(path: str) -> object:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    req = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "rtt-source-identity",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


class TestSourceIdentity(unittest.TestCase):
    def test_precommit_ci_md5_lock(self) -> None:
        self.assertTrue(TWIN_A.exists())
        self.assertTrue(TWIN_B.exists())
        self.assertEqual(_md5(TWIN_A), _md5(TWIN_B), "pre-commit 与 CI 脚本 MD5 必须完全同源")

    def test_remote_repo_protection_api(self) -> None:
        rulesets = _gh(f"/repos/{REPO}/rulesets")
        self.assertIsInstance(rulesets, list)
        names = [r.get("name") for r in rulesets]
        self.assertTrue(rulesets, "rulesets empty")
        detail = None
        for r in rulesets:
            d = _gh(f"/repos/{REPO}/rulesets/{r['id']}")
            types = [x.get("type") for x in d.get("rules") or []]
            if "pull_request" in types or "non_fast_forward" in types:
                detail = d
                break
        self.assertIsNotNone(detail, f"no matching ruleset in {names}")
        types = [x.get("type") for x in detail.get("rules") or []]
        self.assertIn("non_fast_forward", types, "Force push 必须完全禁用")
        self.assertIn("pull_request", types, "必须PR才可合并")
        bypass = detail.get("bypass_actors") or []
        self.assertEqual(bypass, [], "禁止管理员绕过分支保护 (Include administrators / no bypass)")
        self.assertIn("required_status_checks", types, "Require status checks 强制开启")
        pr = next(x for x in detail["rules"] if x["type"] == "pull_request")
        params = pr.get("parameters") or {}
        self.assertGreaterEqual(int(params.get("required_approving_review_count") or 0), 1)

        # classic protection if visible
        try:
            prot = _gh(f"/repos/{REPO}/branches/main/protection")
        except urllib.error.HTTPError:
            prot = None
        if isinstance(prot, dict):
            admins = prot.get("enforce_admins") or {}
            self.assertTrue(admins.get("enabled") is True or admins is True, "Include administrators 开启")
            self.assertFalse((prot.get("allow_force_pushes") or {}).get("enabled", True))

    def test_e2e_unqualified_intercept(self) -> None:
        with self.assertRaises(GateBlocked):
            assert_scene_quota(SceneCounts(qa=1, reason=1, tool=1))
        # protection + required checks imply merge of failing CI is forbidden
        rulesets = _gh(f"/repos/{REPO}/rulesets")
        found_pr = False
        found_checks = False
        for r in rulesets:
            d = _gh(f"/repos/{REPO}/rulesets/{r['id']}")
            types = [x.get("type") for x in d.get("rules") or []]
            if "pull_request" in types:
                found_pr = True
            if "required_status_checks" in types:
                found_checks = True
        self.assertTrue(found_pr and found_checks, "流水线必须真实拦截不合格合入：PR + required status checks")


if __name__ == "__main__":
    unittest.main()
