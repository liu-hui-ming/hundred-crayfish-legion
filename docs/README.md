# Technical documentation

Design notes, runbooks, and API references for Hundred Crayfish Legion will
be added here. See the repository `README.md` for quick start.

- P1: [GitHub issue draft (baseline only)](./github-issue-p1-baseline-2026-04-24.md)
- P2: [Axium uplift prerequisite checklist (template)](./AXIUM_UPLIFT_PREREQUISITES.md) — optional, non-blocking.
- P2: [GitHub issue draft (elastic only — easter + Axium handoff)](./github-issue-p2-elastic-2026-04-24.md)
- **发布到 GitHub Issues（API）：** 根目录 `scripts/publish_p1_p2_github_issues.ps1`（`$env:GH_TOKEN`）；正文/中文见 `docs/issue-exports/`（含 Axium 一日一发：`axium-daily-body-en.md`、`axium-daily-comment-zh.md`）。
- **P1 少轮次探活：** `scripts/run-genesis-n-rounds.sh`（Git Bash / WSL）；**P2 彩蛋烟测：** `scripts/verify-p2-easter.ps1`。
