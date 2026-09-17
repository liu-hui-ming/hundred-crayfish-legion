#Requires -Version 5.1
<#
  XIAN one-post-per-day (2026-09-16). Folder export per XIAN-ARCHIVE-HARD-RULES.md.
  Labels: P1-Roadmap, documentation

  Issue #128 already created; script retained for re-post / label sync only.

  $env:GH_TOKEN = "ghp_..."
  powershell -ExecutionPolicy Bypass -File .\scripts\publish_xian_daily_issue_2026_09_16.ps1
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
$titlePath = Join-Path $root "docs\issue-exports\xian-daily-2026-09-16\title.txt"
$bodyPath = Join-Path $root "docs\issue-exports\xian-daily-2026-09-16\body.md"
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
    "User-Agent"           = "HCL-publish-xian-daily-20260916-ps1"
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
    Write-Host "WhatIf: POST issue (2026-09-16 XIAN daily folder export)"
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

Write-Host ""
Write-Host $url -ForegroundColor Green
