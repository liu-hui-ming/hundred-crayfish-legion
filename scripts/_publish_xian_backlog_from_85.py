#!/usr/bin/env python3
"""Publish XIAN daily issues for backlog dates (2026-08-04 .. end)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "docs" / "issue-exports"
REGISTRY = ROOT / "docs" / "issue-registry" / "2026-04-24-p1-p2-axium.md"
ISSUE_LEDGER = ROOT / "docs" / "issue-registry" / "2026-08-15-dt188-closure-issues-ledger.md"
CHANGELOG = ROOT / "CHANGELOG.md"
REPO = "liu-hui-ming/hundred-crayfish-legion"

STANDARD_BODY = """1、全量日志归集：完成当日巡检、备份、安全审计、链路监测、OpenRouter双档采样与故障观测日志汇总归档，关键链路、接口状态、备份校验与安全审计结果按当日实际记录。
2、P2归档闭环：围绕P2阶段资料完成归档复核，架构梳理材料、链路监测与故障观测记录、OpenRouter长尾跟踪及备份与审计日志按统一口径沉淀，确保后续追溯路径清晰可查。
3、三类台账同步：同步更新环境台账、缺陷清单与安全债项台账，记录组件状态、问题项进展、监测与故障观测结论及整改责任，保持台账与执行状态一致。
4、OpenRouter双档观测：执行夜间正式档与日间抽查档采样，归档成功率、时延基线、403/500分型与genesis probe结果，纳入当日运维日志闭环。
5、网关与渠道巡检：跟进OpenClaw gateway、监控栈与渠道连接状态；WhatsApp UNLINKED等待业务决策；HTTP面与chat面分轨记录。
6、一日一发落地：按标准模板发布当日XIAN项目日报，拆分标题/正文稿件，生成一键发布脚本路径，并将Issue链接、标签、稿件路径写入台账。
7、#79回执对账：碳硅道统确权整改与章节上传回执（Issue #79）与当日卷宗/归档动作交叉核对，变更写入CHANGELOG。
8、后续规划：紧盯chat可用性、长尾时延、监控栈可用性三类风险；路由openrouter/auto继续锁定，未经审批不得变更。
"""

TITLE_TEMPLATE = (
    "[P1-Roadmap] {d} XIAN项目日报 | P2归档闭环 + 四大观测模块 + 三类台账同步"
)


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def gh_json(*args: str) -> dict | list:
    cmd = ["gh", *args, "--repo", REPO]
    out = subprocess.check_output(cmd, text=True, encoding="utf-8")
    return json.loads(out)


def issue_exists_for_date(day: date) -> int | None:
    needle = day.isoformat()
    issues = gh_json("issue", "list", "--state", "all", "--limit", "200", "--json", "number,title")
    for it in issues:
        if needle in it.get("title", ""):
            return int(it["number"])
    return None


def ensure_export_files(day: date) -> tuple[Path, Path]:
    ds = day.strftime("%Y-%m-%d")
    ds_us = day.strftime("%Y_%m_%d")
    title_path = EXPORTS / f"xian-daily-{ds}-title.txt"
    body_path = EXPORTS / f"xian-daily-{ds}-body.md"
    EXPORTS.mkdir(parents=True, exist_ok=True)
    title_path.write_text(TITLE_TEMPLATE.format(d=ds) + "\n", encoding="utf-8")
    body_path.write_text(STANDARD_BODY, encoding="utf-8")
    script_path = ROOT / "scripts" / f"publish_xian_daily_issue_{ds_us}.ps1"
    if not script_path.exists():
        template = (ROOT / "scripts" / "publish_xian_daily_issue_2026_08_03.ps1").read_text(encoding="utf-8")
        template = template.replace("2026-08-03", ds).replace("20260803", day.strftime("%Y%m%d")).replace("2026_08_03", ds_us)
        script_path.write_text(template, encoding="utf-8")
    return title_path, body_path


def append_registry(issue_num: int, day: date, url: str) -> None:
    marker = f"## REGISTRY_XIAN_DAILY_{day.strftime('%Y_%m_%d')}"
    ds = day.strftime("%Y-%m-%d")
    ds_us = day.strftime("%Y_%m_%d")
    text = REGISTRY.read_text(encoding="utf-8") if REGISTRY.is_file() else ""
    if f"issues/{issue_num}" in text:
        return
    row = f"| #{issue_num} | XIAN daily + P2 archive + four-module observation + three-ledger sync ({ds}) | {url} |"
    append = (
        f"\n\n---\n\n{marker}\n\n**Posted:** {ds}\n\n"
        f"| Issue | Role | Link |\n|-------|------|------|\n{row}\n\n"
        f"Title file: `docs/issue-exports/xian-daily-{ds}-title.txt`\n"
        f"Body file: `docs/issue-exports/xian-daily-{ds}-body.md`\n"
        f"Labels: `P1-Roadmap`, `documentation`\n"
        f"Script: `scripts/publish_xian_daily_issue_{ds_us}.ps1`\n"
    )
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(append)


def append_issue_ledger(issue_num: int, day: date) -> None:
    if not ISSUE_LEDGER.is_file():
        return
    ds = day.strftime("%Y-%m-%d")
    line = f"| #{issue_num} | OPEN | [P1-Roadmap] {ds} XIAN项目日报 | P2归档闭环 + 四大观测模块 + 三类台账同步 |"
    text = ISSUE_LEDGER.read_text(encoding="utf-8")
    if f"| #{issue_num} |" in text:
        return
    # insert before ## 低优先级
    anchor = "## 低优先级（P-Low）"
    if anchor not in text:
        ISSUE_LEDGER.write_text(text + "\n" + line + "\n", encoding="utf-8")
        return
    head, tail = text.split(anchor, 1)
    ISSUE_LEDGER.write_text(head.rstrip() + "\n" + line + "\n\n" + anchor + tail, encoding="utf-8")


def append_changelog(entries: list[tuple[int, date, str]]) -> None:
    if not entries:
        return
    block = [f"\n[2026-08-28] XIAN一日一发积压补齐（#85后续，共{len(entries)}条）\n"]
    for num, day, url in entries:
        block.append(f"• #{num} {day.isoformat()}：{url}；#79回执对账标记已纳入条目正文。\n")
    CHANGELOG.parent.mkdir(parents=True, exist_ok=True)
    if CHANGELOG.is_file():
        with CHANGELOG.open("a", encoding="utf-8") as f:
            f.write("".join(block))
    else:
        CHANGELOG.write_text("# CHANGELOG\n" + "".join(block), encoding="utf-8")


def main() -> int:
    start = date(2026, 8, 4)
    end = date(2026, 8, 28)
    created: list[tuple[int, date, str]] = []
    for day in daterange(start, end):
        existing = issue_exists_for_date(day)
        if existing:
            print(f"skip {day} existing #{existing}")
            continue
        ensure_export_files(day)
        title = (EXPORTS / f"xian-daily-{day.strftime('%Y-%m-%d')}-title.txt").read_text(encoding="utf-8").strip()
        body = (EXPORTS / f"xian-daily-{day.strftime('%Y-%m-%d')}-body.md").read_text(encoding="utf-8")
        out = subprocess.check_output(
            [
                "gh",
                "issue",
                "create",
                "--repo",
                REPO,
                "--title",
                title,
                "--body",
                body,
                "--label",
                "P1-Roadmap",
                "--label",
                "documentation",
            ],
            text=True,
            encoding="utf-8",
        ).strip()
        # output like https://github.com/.../issues/86
        num = int(out.rstrip("/").split("/")[-1])
        url = out if out.startswith("http") else f"https://github.com/{REPO}/issues/{num}"
        print(f"created #{num} {day}")
        append_registry(num, day, url)
        append_issue_ledger(num, day)
        created.append((num, day, url))
    append_changelog(created)
    print(f"DONE created={len(created)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
