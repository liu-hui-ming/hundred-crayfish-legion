#Requires -Version 5.1
<#
  XIAN one-post-per-day template (2026-05-07). Title/body from UTF-8 files (no Chinese in this .ps1).
  Labels: P1-Roadmap, documentation

  $env:GH_TOKEN = "ghp_..."
  powershell -ExecutionPolicy Bypass -File .\scripts\publish_xian_daily_issue_2026_05_07.ps1
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
$titlePath = Join-Path $root "docs\issue-exports\xian-daily-2026-05-07-title.txt"
$bodyPath = Join-Path $root "docs\issue-exports\xian-daily-2026-05-07-body.md"
$registryPath = Join-Path $root "docs\issue-registry\2026-04-24-p1-p2-axium.md"
foreach ($p in @($titlePath, $bodyPath)) {
    if (-not (Test-Path $p)) { throw "Missing $p" }
}

if (-not $Token) { $Token = $env:GH_TOKEN }
if (-not $Token) { $Token = $env:GITHUB_TOKEN }
if (-not $Token) {
    Write-Host "Set GH_TOKEN with issues: write." -ForegroundColor Yellow
    exit 1
}

$Token = ($Token -replace "[\x00-\x08\x0B\x0C\x0E-\x1F]", "").Trim()

function Remove-LeadingBom([string]$s) {
    if ([string]::IsNullOrEmpty($s)) { return $s }
    if ([int][char]$s[0] -eq 0xFEFF) { return $s.Substring(1) }
    return $s
}

$title = Remove-LeadingBom([System.IO.File]::ReadAllText($titlePath, $enc)).Trim()
$bodyText = Remove-LeadingBom([System.IO.File]::ReadAllText($bodyPath, $enc))
if (-not $title) { throw "Empty title file" }

$api = "https://api.github.com"
$headers = @{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent"           = "HCL-publish-xian-daily-20260507-ps1"
}

function Invoke-Gh {
    param([string]$Uri, [string]$Method, [string]$BodyJson = $null)
    $p = @{ Uri = $Uri; Method = $Method; Headers = $headers }
    if ($null -ne $BodyJson -and $BodyJson.Length -gt 0) {
        $p["ContentType"] = "application/json; charset=utf-8"
        $p["Body"] = $BodyJson
    }
    Invoke-RestMethod @p
}

$labels = @("P1-Roadmap", "documentation")

if ($WhatIf) {
    Write-Host "WhatIf: POST issue (2026-05-07 XIAN daily template)"
    exit 0
}

$payload = [ordered]@{ title = $title; body = $bodyText }
$json = $payload | ConvertTo-Json -Depth 20 -Compress
Write-Host "Creating issue..."
$issue = Invoke-Gh -Uri "$api/repos/$Owner/$Repo/issues" -Method Post -BodyJson $json
$n = [int]$issue.number
$url = $issue.html_url
Write-Host "Created #$n : $url"

$labObj = [ordered]@{ labels = @($labels) }
$labJson = $labObj | ConvertTo-Json -Depth 5 -Compress
try {
    Invoke-Gh -Uri "$api/repos/$Owner/$Repo/issues/$n/labels" -Method Put -BodyJson $labJson | Out-Null
    Write-Host "Labels applied: $($labels -join ', ')"
} catch {
    Write-Warning "Labels failed: $($_.Exception.Message)"
}

$marker = "## REGISTRY_XIAN_DAILY_2026_05_07"
$regFull = [System.IO.File]::ReadAllText($registryPath, $enc)
if ($regFull -notmatch [regex]::Escape($marker)) {
    $nl = [Environment]::NewLine
    $row = '| #' + $n + ' | XIAN daily + OpenClaw 5.4 rollout (2026-05-07) | ' + $url + ' |'
    $append =
        $nl + $nl + '---' + $nl + $nl +
        $marker + $nl + $nl +
        '**Posted:** 2026-05-07' + $nl + $nl +
        '| Issue | Role | Link |' + $nl +
        '|-------|------|------|' + $nl +
        $row + $nl + $nl +
        'Title file: `docs/issue-exports/xian-daily-2026-05-07-title.txt`' + $nl +
        'Body file: `docs/issue-exports/xian-daily-2026-05-07-body.md`' + $nl +
        'Labels: `P1-Roadmap`, `documentation`' + $nl +
        'Script: `scripts/publish_xian_daily_issue_2026_05_07.ps1`' + $nl
    Add-Content -Path $registryPath -Value $append -Encoding utf8
    Write-Host "Registry updated: $registryPath"
} else {
    Write-Host "Registry already contains this section; append skipped."
}

Write-Host ""
Write-Host $url -ForegroundColor Green
