# Technical documentation

Design notes, runbooks, and API references for Hundred Crayfish Legion will
be added here. See the repository `README.md` for quick start.

- P1: [GitHub issue draft (baseline only)](./github-issue-p1-baseline-2026-04-24.md)
- P2: [Axium uplift prerequisite checklist (template)](./AXIUM_UPLIFT_PREREQUISITES.md) — optional, non-blocking.
- P2: [GitHub issue draft (elastic only — easter + Axium handoff)](./github-issue-p2-elastic-2026-04-24.md)
- **发布到 GitHub Issues（API）：** `scripts/publish_p1_p2_github_issues.ps1`（`$env:GH_TOKEN`）；正文/中文见 `docs/issue-exports/`。可选 **同日发第三条** Axium：`.\scripts\publish_p1_p2_github_issues.ps1 -IncludeAxiumDaily`。
- **关闭重复 Issue：** `.\scripts\close_github_issues.ps1 -IssueNumbers "4,5"`（`powershell -File` 时务必用引号，避免 `4,5` 被解析成 45）。可加 `-SkipClosingComment`。
- **P1 少轮次探活：** `scripts/run-genesis-n-rounds.sh`（Git Bash / WSL）；**P2 彩蛋烟测：** `scripts/verify-p2-easter.ps1`。
- **路线图 Issue 台账（#6/#7/#8）：** [`issue-registry/2026-04-24-p1-p2-axium.md`](./issue-registry/2026-04-24-p1-p2-axium.md)；Axium 标题/正文/标签对齐脚本：`scripts/finalize_axium_github_issue.ps1`。
