#Requires -Version 5.1
<#
  Publishes one GitHub Issue: [P2-Roadmap] Easter egg live validation (ASCII title).
  Body: docs/issue-exports/p2-easter-live-validation-2026-04-28-body.md
  Labels: P2-Roadmap, documentation (-CreateLabels if missing)

  After POST: PATCH body section 3 "Issue编号" with real number; append row to docs/issue-registry/2026-04-24-p1-p2-axium.md

  $env:GH_TOKEN = "ghp_..."
  powershell -ExecutionPolicy Bypass -File .\scripts\publish_p2_easter_validation_issue.ps1 -CreateLabels
#>
param(
    [string] $Token,
    [string] $Owner = "liu-hui-ming",
    [string] $Repo = "hundred-crayfish-legion",
    [switch] $CreateLabels,
    [switch] $WhatIf
)

$ErrorActionPreference = "Stop"
$title = "[P2-Roadmap] HCL: P2 Easter Egg Live Validation & Runtime Contract"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$bodyPath = Join-Path $root "docs\issue-exports\p2-easter-live-validation-2026-04-28-body.md"
$registryPath = Join-Path $root "docs\issue-registry\2026-04-24-p1-p2-axium.md"
if (-not (Test-Path $bodyPath)) { throw "Missing $bodyPath" }

if (-not $Token) { $Token = $env:GH_TOKEN }
if (-not $Token) { $Token = $env:GITHUB_TOKEN }
if (-not $Token) {
    Write-Host "Set GH_TOKEN with issues: write." -ForegroundColor Yellow
    exit 1
}

$bodyTemplate = [System.IO.File]::ReadAllText($bodyPath, [System.Text.UTF8Encoding]::new($false))

$api = "https://api.github.com"
$headers = @{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent"           = "HCL-publish-p2-easter-ps1"
}

function Invoke-Gh {
    param([string]$Uri, [string]$Method, [byte[]]$Body = $null)
    $p = @{ Uri = $Uri; Method = $Method; Headers = $headers }
    if ($null -ne $Body -and $Body.Length -gt 0) {
        $p["ContentType"] = "application/json; charset=utf-8"
        $p["Body"] = $Body
    }
    Invoke-RestMethod @p
}

$labels = @("P2-Roadmap", "documentation")
if ($CreateLabels) {
    foreach ($name in $labels) {
        try {
            $lo = [ordered]@{ name = $name; color = "5319E7"; description = "HCL P2 roadmap / docs" }
            $lb = [System.Text.Encoding]::UTF8.GetBytes(($lo | ConvertTo-Json -Depth 5))
            Invoke-Gh -Uri "$api/repos/$Owner/$Repo/labels" -Method Post -Body $lb | Out-Null
            Write-Host "Created label: $name"
        } catch {
            Write-Host "Label $name : $($_.Exception.Message)"
        }
    }
}

if ($WhatIf) {
    Write-Host "WhatIf: would POST issue with title=$title"
    exit 0
}

$payload = [ordered]@{ title = $title; body = $bodyTemplate }
$json = $payload | ConvertTo-Json -Depth 15
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
Write-Host "Creating issue..."
$issue = Invoke-Gh -Uri "$api/repos/$Owner/$Repo/issues" -Method Post -Body $bytes
$n = [int]$issue.number
$url = $issue.html_url
Write-Host "Created #$n : $url"

# Fix body: Issue编号 line
$bodyFinal = $bodyTemplate -replace "Issue编号：（发布后由脚本填入实际编号）", "Issue编号：#$n"
$patch = [ordered]@{ body = $bodyFinal }
$pb = [System.Text.Encoding]::UTF8.GetBytes(($patch | ConvertTo-Json -Depth 15))
Invoke-Gh -Uri "$api/repos/$Owner/$Repo/issues/$n" -Method Patch -Body $pb | Out-Null
Write-Host "PATCH body with Issue编号 #$n"

# Labels
$labObj = [ordered]@{ labels = @($labels) }
$labBytes = [System.Text.Encoding]::UTF8.GetBytes(($labObj | ConvertTo-Json -Depth 5))
try {
    Invoke-Gh -Uri "$api/repos/$Owner/$Repo/issues/$n/labels" -Method Put -Body $labBytes | Out-Null
    Write-Host "Labels applied: $($labels -join ', ')"
} catch {
    Write-Warning "Labels failed: $($_.Exception.Message). Retry with -CreateLabels."
}

# Append registry section if not already present
$regFull = [System.IO.File]::ReadAllText($registryPath, [System.Text.UTF8Encoding]::new($false))
$marker = "## P2 一日一发 · 彩蛋运行时验证（2026-04-28）"
if ($regFull -notmatch [regex]::Escape($marker)) {
    $append = @"

---

$marker

**发布日期：** 2026-04-28

| Issue | 角色 | 链接 |
|-------|------|------|
| #$n | P2 Easter live validation（verify-p2-easter 闭环） | $url |

**稿件路径：** ``docs/issue-exports/p2-easter-live-validation-2026-04-28-body.md``  
**标签：** ``P2-Roadmap``，``documentation``

**发布脚本：** ``scripts/publish_p2_easter_validation_issue.ps1``
"@
    Add-Content -Path $registryPath -Value $append -Encoding utf8
    Write-Host "Registry updated: $registryPath"
} else {
    Write-Host "Registry already contains P2 daily section; append skipped."
}

Write-Host ""
Write-Host $url -ForegroundColor Green
