#Requires -Version 5.1
<#
  1) PATCH Issue #8 (default) title to ASCII, body from docs/issue-exports/axium-daily-body-en.md
  2) POST Chinese comment from axium-daily-comment-zh.md if not already present (heuristic)
  3) PUT labels (must exist on repo, or create with -CreateLabels)

  Needs: GH_TOKEN / GITHUB_TOKEN with Issues: write; Contents: read.

  Example:
    $env:GH_TOKEN = "ghp_..."
    powershell -ExecutionPolicy Bypass -File .\scripts\finalize_axium_github_issue.ps1
#>
param(
    [int] $IssueNumber = 8,
    [string] $Token,
    [string] $Owner = "liu-hui-ming",
    [string] $Repo = "hundred-crayfish-legion",
    [string[]] $Labels = @("P1-Roadmap", "documentation"),
    [switch] $CreateLabels
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not $Token) { $Token = $env:GH_TOKEN }
if (-not $Token) { $Token = $env:GITHUB_TOKEN }
if (-not $Token) {
    Write-Host "Set GH_TOKEN with issues: write." -ForegroundColor Yellow
    exit 1
}

$asciiTitle = "[P1-Roadmap] HCL: Axium daily track - Carbon-Silicon alignment (SSOT hooks)"
$exp = Join-Path $root "docs\issue-exports"
$bodyPath = Join-Path $exp "axium-daily-body-en.md"
$zhPath = Join-Path $exp "axium-daily-comment-zh.md"
if (-not (Test-Path $bodyPath)) { throw "Missing $bodyPath" }
if (-not (Test-Path $zhPath)) { throw "Missing $zhPath" }

$bodyText = [System.IO.File]::ReadAllText($bodyPath, [System.Text.UTF8Encoding]::new($false))
$zhText = [System.IO.File]::ReadAllText($zhPath, [System.Text.UTF8Encoding]::new($false))

$api = "https://api.github.com"
$headers = @{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent"           = "HCL-finalize-axium-ps1"
}

function Invoke-GitHubJson {
    param(
        [string] $Uri,
        [ValidateSet("Get", "Post", "Patch", "Put")]
        [string] $Method,
        [byte[]] $Body = $null
    )
    $params = @{ Uri = $Uri; Method = $Method; Headers = $headers }
    if ($null -ne $Body -and $Body.Length -gt 0) {
        $params["ContentType"] = "application/json; charset=utf-8"
        $params["Body"] = $Body
    }
    return Invoke-RestMethod @params
}

# --- PATCH issue (title + body) ---
$patchObj = [ordered]@{ title = $asciiTitle; body = $bodyText }
$patchJson = $patchObj | ConvertTo-Json -Depth 12
$patchBytes = [System.Text.Encoding]::UTF8.GetBytes($patchJson)
$issueUri = "$api/repos/$Owner/$Repo/issues/$IssueNumber"
Write-Host "PATCH $issueUri (ASCII title + EN body from template)..."
$issue = Invoke-GitHubJson -Uri $issueUri -Method Patch -Body $patchBytes
Write-Host "OK #$($issue.number): $($issue.html_url)"

# --- Comment ZH if missing ---
$commentsUri = "$api/repos/$Owner/$Repo/issues/$IssueNumber/comments"
$comments = @((Invoke-GitHubJson -Uri $commentsUri -Method Get))
$marker = "Axium 主题"
$hasZh = $false
foreach ($c in $comments) {
    if ($c.body -and ($c.body -match [regex]::Escape($marker))) {
        $hasZh = $true
        break
    }
}
if (-not $hasZh) {
    $cj = ( [ordered]@{ body = $zhText } | ConvertTo-Json -Depth 5 )
    $cb = [System.Text.Encoding]::UTF8.GetBytes($cj)
    Write-Host "POST Chinese comment..."
    Invoke-GitHubJson -Uri $commentsUri -Method Post -Body $cb | Out-Null
    Write-Host "OK Chinese comment added."
} else {
    Write-Host "Skip: Chinese comment already present (matched '$marker')."
}

# --- Labels ---
if ($CreateLabels) {
    foreach ($name in $Labels) {
        $labelUri = "$api/repos/$Owner/$Repo/labels"
        try {
            $lo = [ordered]@{ name = $name; color = "0e8a16"; description = "HCL roadmap / docs" }
            $lb = [System.Text.Encoding]::UTF8.GetBytes(($lo | ConvertTo-Json -Depth 5))
            Invoke-GitHubJson -Uri $labelUri -Method Post -Body $lb | Out-Null
            Write-Host "Created label: $name"
        } catch {
            Write-Host "Label $name : $($_.Exception.Message) (may already exist)"
        }
    }
}

$labelsUri = "$api/repos/$Owner/$Repo/issues/$IssueNumber/labels"
$labObj = [ordered]@{ labels = @($Labels) }
$labJson = $labObj | ConvertTo-Json -Depth 5
$labBytes = [System.Text.Encoding]::UTF8.GetBytes($labJson)
Write-Host "PUT labels: $($Labels -join ', ')..."
try {
    Invoke-GitHubJson -Uri $labelsUri -Method Put -Body $labBytes | Out-Null
    Write-Host "OK labels applied."
} catch {
    Write-Warning "Labels failed ($($_.Exception.Message)). Ensure labels exist on repo or run with -CreateLabels once."
}

Write-Host ""
Write-Host $issue.html_url -ForegroundColor Green
