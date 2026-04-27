#Requires -Version 5.1
<#
  Publishes GitHub Issues: P1 + P2 (always); optional third Axium daily thread.

  Prereq: personal access token with "Issues: read and write" for liu-hui-ming/hundred-crayfish-legion.
  $env:GH_TOKEN = "ghp_..."  or  $env:GITHUB_TOKEN
  (Optional) -Token "ghp_..."

  From repo root:
    cd E:\hundred-crayfish-legion
    $env:GH_TOKEN = "YOUR_TOKEN"
    powershell -ExecutionPolicy Bypass -File .\scripts\publish_p1_p2_github_issues.ps1

  Also create Axium one-post-per-day issue (docs/issue-exports/axium-daily-*.md):
    ... -IncludeAxiumDaily
#>
param(
    [string] $Token,
    [string] $Owner = "liu-hui-ming",
    [string] $Repo = "hundred-crayfish-legion",
    [switch] $IncludeAxiumDaily
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not $Token) { $Token = $env:GH_TOKEN }
if (-not $Token) { $Token = $env:GITHUB_TOKEN }
if (-not $Token) {
    Write-Host "Set GH_TOKEN (or GITHUB_TOKEN, or -Token) with issues: write." -ForegroundColor Yellow
    Write-Host "Manual: https://github.com/$Owner/$Repo/issues/new"
    exit 1
}

$api = "https://api.github.com"
$headers = @{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent"           = "HCL-publish-issues-ps1"
}

function New-Issue {
    param([string]$Title, [string]$BodyPath)
    $text = [System.IO.File]::ReadAllText($BodyPath, [System.Text.UTF8Encoding]::new($false))
    $payloadObject = [ordered]@{ title = $Title; body = $text }
    $json = $payloadObject | ConvertTo-Json -Depth 10
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $uri = "$api/repos/$Owner/$Repo/issues"
    return Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -ContentType "application/json; charset=utf-8" -Body $bytes
}

function Add-Comment-FromFile {
    param([int]$Number, [string]$Path)
    $t = [System.IO.File]::ReadAllText($Path, [System.Text.UTF8Encoding]::new($false))
    Add-Comment-Text -Number $Number -Text $t
}

function Add-Comment-Text {
    param([int]$Number, [string]$Text)
    $json = ( [ordered]@{ body = $Text } | ConvertTo-Json -Depth 5 )
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $uri = "$api/repos/$Owner/$Repo/issues/${Number}/comments"
    return Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -ContentType "application/json; charset=utf-8" -Body $bytes
}

$exp = Join-Path $root "docs\issue-exports"
if (-not (Test-Path (Join-Path $exp "p1-body-en.md"))) { throw "Missing $exp – run from repo with docs/issue-exports" }

$title1 = "[P1-Roadmap] HCL: P1 foundation baseline - kernel, service, P1 web, health, deploy, CI"
$title2 = "[P1-Roadmap] HCL: P2 elastic - easter-egg (short check) + Axium uplift prerequisite list"

Write-Host "Creating P1 issue..."
$i1 = New-Issue -Title $title1 -BodyPath (Join-Path $exp "p1-body-en.md")
Write-Host "P1 #$($i1.number): $($i1.html_url)"

Add-Comment-FromFile -Number $i1.number -Path (Join-Path $exp "p1-comment-zh.md")
Write-Host "P1: Chinese comment OK."

Write-Host "Creating P2 issue..."
$i2 = New-Issue -Title $title2 -BodyPath (Join-Path $exp "p2-body-en.md")
Write-Host "P2 #$($i2.number): $($i2.html_url)"

Add-Comment-FromFile -Number $i2.number -Path (Join-Path $exp "p2-comment-zh.md")
Write-Host "P2: Chinese comment OK."

Add-Comment-Text -Number $i1.number -Text "Cross-link (EN): P2 post — $($i2.html_url)"
Add-Comment-Text -Number $i2.number -Text "Cross-link (EN): P1 post — $($i1.html_url)"
Write-Host "Cross-links added."

$i3 = $null
if ($IncludeAxiumDaily) {
    $axBody = Join-Path $exp "axium-daily-body-en.md"
    $axZh = Join-Path $exp "axium-daily-comment-zh.md"
    if (-not (Test-Path $axBody)) { throw "Missing $axBody (required with -IncludeAxiumDaily)" }
    if (-not (Test-Path $axZh)) { throw "Missing $axZh (required with -IncludeAxiumDaily)" }
    # ASCII title avoids mojibake in some API/Windows code paths (GitHub accepts UTF-8 body separately).
    $title3 = "[P1-Roadmap] HCL: Axium daily track - Carbon-Silicon alignment (SSOT hooks)"
    Write-Host "Creating Axium daily issue..."
    $i3 = New-Issue -Title $title3 -BodyPath $axBody
    Write-Host "Axium #$($i3.number): $($i3.html_url)"
    Add-Comment-FromFile -Number $i3.number -Path $axZh
    Write-Host "Axium: Chinese comment OK."
    Add-Comment-Text -Number $i1.number -Text "Cross-link (EN): Axium daily — $($i3.html_url)"
    Add-Comment-Text -Number $i2.number -Text "Cross-link (EN): Axium daily — $($i3.html_url)"
    Add-Comment-Text -Number $i3.number -Text "Cross-link (EN): P1 post — $($i1.html_url)`nCross-link (EN): P2 post — $($i2.html_url)"
    Write-Host "Axium cross-links added."
}

Write-Host ""
Write-Host "P1: $($i1.html_url)" -ForegroundColor Green
Write-Host "P2: $($i2.html_url)" -ForegroundColor Green
if ($i3) {
    Write-Host "Axium daily: $($i3.html_url)" -ForegroundColor Green
}
