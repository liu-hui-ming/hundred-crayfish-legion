#Requires -Version 5.1
<#
  Close GitHub issues by number (PATCH state=closed). Posts an optional closing comment first.

  Needs a token with Issues: read and write (same as publish script).
  $env:GH_TOKEN or $env:GITHUB_TOKEN or -Token

  Example — remove duplicate older P1/P2 after re-running publish (adjust numbers if yours differ):
    $env:GH_TOKEN = "ghp_..."
    powershell -ExecutionPolicy Bypass -File .\scripts\close_github_issues.ps1 -IssueNumber 4,5
#>
param(
    [Parameter(Mandatory = $true)]
    [int[]] $IssueNumber,
    [string] $Token,
    [string] $Owner = "liu-hui-ming",
    [string] $Repo = "hundred-crayfish-legion",
    [string] $Comment = "Closed as duplicate: same roadmap content was posted again by a second publish run. Keeping the newer [P1-Roadmap] pair (and Axium cross-links) as canonical."
)

$ErrorActionPreference = "Stop"
if (-not $Token) { $Token = $env:GH_TOKEN }
if (-not $Token) { $Token = $env:GITHUB_TOKEN }
if (-not $Token) {
    Write-Host "Set GH_TOKEN (or GITHUB_TOKEN, or -Token) with issues: write." -ForegroundColor Yellow
    exit 1
}

$api = "https://api.github.com"
$headers = @{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent"           = "HCL-close-issues-ps1"
}

function Close-OneIssue {
    param([int] $Number, [string] $ClosingComment)
    if ($ClosingComment) {
        $json = ( [ordered]@{ body = $ClosingComment } | ConvertTo-Json -Depth 5 )
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
        $uri = "$api/repos/$Owner/$Repo/issues/${Number}/comments"
        Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -ContentType "application/json; charset=utf-8" -Body $bytes | Out-Null
        Write-Host "Issue #$Number : closing comment posted."
    }
    $patchJson = ( [ordered]@{ state = "closed" } | ConvertTo-Json )
    $patchBytes = [System.Text.Encoding]::UTF8.GetBytes($patchJson)
    $issueUri = "$api/repos/$Owner/$Repo/issues/${Number}"
    Invoke-RestMethod -Uri $issueUri -Method Patch -Headers $headers -ContentType "application/json; charset=utf-8" -Body $patchBytes | Out-Null
    Write-Host "Issue #$Number : closed." -ForegroundColor Green
}

foreach ($n in ($IssueNumber | Sort-Object -Unique)) {
    Close-OneIssue -Number $n -ClosingComment $Comment
}

Write-Host "Done."
