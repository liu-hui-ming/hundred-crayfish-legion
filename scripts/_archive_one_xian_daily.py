# -*- coding: utf-8 -*-
"""Archive one XIAN daily: folder export + publish script + gh issue + registry + CHANGELOG snippet."""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


def write_publish_script(day: date) -> Path:
    ds = day.strftime("%Y-%m-%d")
    ds_us = day.strftime("%Y_%m_%d")
    ymd_compact = day.strftime("%Y%m%d")
    script_path = ROOT / "scripts" / f"publish_xian_daily_issue_{ds_us}.ps1"
    rel_title = f"docs\\issue-exports\\xian-daily-{ds}\\title.txt"
    rel_body = f"docs\\issue-exports\\xian-daily-{ds}\\body.md"
    text = f"""#Requires -Version 5.1
<#
  XIAN one-post-per-day ({ds}). Folder export per XIAN-ARCHIVE-HARD-RULES.md.
  Labels: P1-Roadmap, documentation

  $env:GH_TOKEN = "ghp_..."
  powershell -ExecutionPolicy Bypass -File .\\scripts\\publish_xian_daily_issue_{ds_us}.ps1
#>
param(
    [string] $Token,
    [string] $Owner = "liu-hui-ming",
    [string] $Repo = "hundred-crayfish-legion",
    [switch] $WhatIf
)

$ErrorActionPreference = "Stop"
$enc = [System.Text.UTF8Encoding]::new($false)
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$titlePath = Join-Path $root "{rel_title}"
$bodyPath = Join-Path $root "{rel_body}"
$registryPath = Join-Path $root "docs\\issue-registry\\2026-04-24-p1-p2-axium.md"
foreach ($p in @($titlePath, $bodyPath)) {{
    if (-not (Test-Path $p)) {{ throw "Missing $p" }}
}}

if (-not $Token) {{ $Token = $env:GH_TOKEN }}
if (-not $Token) {{ $Token = $env:GITHUB_TOKEN }}
if (-not $Token) {{
    Write-Host "Set GH_TOKEN with issues: write." -ForegroundColor Yellow
    exit 1
}}

$Token = ($Token -replace "[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F]", "").Trim()

function Remove-LeadingBom([string]$s) {{
    if ([string]::IsNullOrEmpty($s)) {{ return $s }}
    if ([int][char]$s[0] -eq 0xFEFF) {{ return $s.Substring(1) }}
    return $s
}}

$title = Remove-LeadingBom([System.IO.File]::ReadAllText($titlePath, $enc)).Trim()
$bodyText = Remove-LeadingBom([System.IO.File]::ReadAllText($bodyPath, $enc))
if (-not $title) {{ throw "Empty title file" }}

$api = "https://api.github.com"
$headers = @{{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent"           = "HCL-publish-xian-daily-{ymd_compact}-ps1"
}}

function Invoke-Gh {{
    param([string]$Uri, [string]$Method, [string]$BodyJson = $null)
    $p = @{{ Uri = $Uri; Method = $Method; Headers = $headers }}
    if ($null -ne $BodyJson -and $BodyJson.Length -gt 0) {{
        $p["ContentType"] = "application/json; charset=utf-8"
        $p["Body"] = $BodyJson
    }}
    Invoke-RestMethod @p
}}

$labels = @("P1-Roadmap", "documentation")

if ($WhatIf) {{
    Write-Host "WhatIf: POST issue ({ds} XIAN daily folder export)"
    exit 0
}}

$payload = [ordered]@{{ title = $title; body = $bodyText }}
$json = $payload | ConvertTo-Json -Depth 20 -Compress
Write-Host "Creating issue..."
$issue = Invoke-Gh -Uri "$api/repos/$Owner/$Repo/issues" -Method Post -BodyJson $json
$n = [int]$issue.number
$url = $issue.html_url
Write-Host "Created #$n : $url"

$labObj = [ordered]@{{ labels = @($labels) }}
$labJson = $labObj | ConvertTo-Json -Depth 5 -Compress
try {{
    Invoke-Gh -Uri "$api/repos/$Owner/$Repo/issues/$n/labels" -Method Put -BodyJson $labJson | Out-Null
    Write-Host "Labels applied: $($labels -join ', ')"
}} catch {{
    Write-Warning "Labels failed: $($_.Exception.Message)"
}}

$marker = "## REGISTRY_XIAN_DAILY_{day.strftime('%Y_%m_%d')}"
$regFull = [System.IO.File]::ReadAllText($registryPath, $enc)
$issueNeedle = "https://github.com/$Owner/$Repo/issues/$n"
if ($regFull -notmatch [regex]::Escape($marker)) {{
    $nl = [Environment]::NewLine
    $row = '| #' + $n + ' | XIAN daily + P2 archive + four-module observation + three-ledger sync ({ds}) | ' + $url + ' |'
    $append =
        $nl + $nl + '---' + $nl + $nl +
        $marker + $nl + $nl +
        '**Posted:** {ds}' + $nl + $nl +
        '| Issue | Role | Link |' + $nl +
        '|-------|------|------|' + $nl +
        $row + $nl + $nl +
        'Title file: `docs/issue-exports/xian-daily-{ds}/title.txt`' + $nl +
        'Body file: `docs/issue-exports/xian-daily-{ds}/body.md`' + $nl +
        'Labels: `P1-Roadmap`, `documentation`' + $nl +
        'Script: `scripts/publish_xian_daily_issue_{ds_us}.ps1`' + $nl
    Add-Content -Path $registryPath -Value $append -Encoding utf8
    Write-Host "Registry updated: $registryPath"
}} else {{
    if ($regFull -notmatch [regex]::Escape($issueNeedle)) {{
        $nl = [Environment]::NewLine
        $row = '- Follow-up entry: #' + $n + '  ' + $url + '  (Posted: {ds})'
        Add-Content -Path $registryPath -Value ($nl + $row + $nl) -Encoding utf8
        Write-Host "Registry section exists; follow-up entry appended."
    }} else {{
        Write-Host "Registry already contains this issue link; append skipped."
    }}
}}

Write-Host ""
Write-Host $url -ForegroundColor Green
"""
    script_path.write_text(text, encoding="utf-8", newline="\n")
    return script_path


def ensure_export_folder(day: date) -> tuple[Path, Path]:
    ds = day.strftime("%Y-%m-%d")
    folder = EXPORTS / f"xian-daily-{ds}"
    folder.mkdir(parents=True, exist_ok=True)
    title_path = folder / "title.txt"
    body_path = folder / "body.md"
    title_path.write_text(TITLE_TEMPLATE.format(d=ds) + "\n", encoding="utf-8", newline="\n")
    body_path.write_text(STANDARD_BODY, encoding="utf-8", newline="\n")
    return title_path, body_path


def gh_create(day: date) -> tuple[int, str]:
    ds = day.strftime("%Y-%m-%d")
    folder = EXPORTS / f"xian-daily-{ds}"
    title = (folder / "title.txt").read_text(encoding="utf-8").strip()
    body = (folder / "body.md").read_text(encoding="utf-8")
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
    num = int(out.rstrip("/").split("/")[-1])
    url = out if out.startswith("http") else f"https://github.com/{REPO}/issues/{num}"
    return num, url


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
        f"Title file: `docs/issue-exports/xian-daily-{ds}/title.txt`\n"
        f"Body file: `docs/issue-exports/xian-daily-{ds}/body.md`\n"
        f"Labels: `P1-Roadmap`, `documentation`\n"
        f"Script: `scripts/publish_xian_daily_issue_{ds_us}.ps1`\n"
    )
    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(append)


def append_issue_ledger(issue_num: int, day: date, url: str) -> None:
    ds = day.strftime("%Y-%m-%d")
    line = (
        f"| #{issue_num} | POSTED | [P1-Roadmap] {ds} XIAN项目日报 | "
        f"{url} · #79回执已纳入 |"
    )
    text = ISSUE_LEDGER.read_text(encoding="utf-8")
    if f"| #{issue_num} |" in text:
        return
    anchor = "## 低优先级（P-Low）"
    if anchor not in text:
        ISSUE_LEDGER.write_text(text + "\n" + line + "\n", encoding="utf-8")
        return
    head, tail = text.split(anchor, 1)
    ISSUE_LEDGER.write_text(head.rstrip() + "\n" + line + "\n\n" + anchor + tail, encoding="utf-8")


def append_changelog(issue_num: int, day: date, url: str) -> None:
    ds = day.strftime("%Y-%m-%d")
    block = (
        f"[{ds}] XIAN一日一发归档 #{issue_num}（docs/issue-exports/xian-daily-{ds}/ · backlog）\n\n"
        f"• Issue：{url}\n"
        f"• 稿件：`docs/issue-exports/xian-daily-{ds}/title.txt` + `body.md`\n"
        f"• 脚本：`scripts/publish_xian_daily_issue_{day.strftime('%Y_%m_%d')}.ps1`\n"
        f"• 台账：`docs/issue-registry/` REGISTRY + dt188 ledger\n\n"
    )
    text = CHANGELOG.read_text(encoding="utf-8")
    if f"#{issue_num}" in text and f"xian-daily-{ds}" in text:
        return
    if text.startswith("# CHANGELOG\n\n"):
        CHANGELOG.write_text("# CHANGELOG\n\n" + block + text[len("# CHANGELOG\n\n") :], encoding="utf-8")
    else:
        CHANGELOG.write_text(block + text, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--day", required=True, help="YYYY-MM-DD")
    p.add_argument("--skip-create", action="store_true", help="Skip gh issue create")
    args = p.parse_args()
    y, m, d = map(int, args.day.split("-"))
    day = date(y, m, d)
    ensure_export_folder(day)
    write_publish_script(day)
    if args.skip_create:
        print(f"OK scaffold {day} (no gh create)")
        return 0
    num, url = gh_create(day)
    print(f"created #{num} {url}")
    append_registry(num, day, url)
    append_issue_ledger(num, day, url)
    append_changelog(num, day, url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
