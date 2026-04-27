#Requires -Version 5.1
<#
  Close GitHub issues by number (PATCH state=closed). Posts an optional closing comment first.

  Needs a token with Issues: read and write (same as publish script).
  $env:GH_TOKEN or $env:GITHUB_TOKEN or -Token

  IMPORTANT: When invoking via **powershell -File ...**, use **-IssueNumbers '4,5'** (quoted string).
  Bare **-IssueNumber 4,5** can bind incorrectly (e.g. as 45) depending on argument parsing.

  Examples:
    $env:GH_TOKEN = "ghp_..."
    powershell -ExecutionPolicy Bypass -File .\scripts\close_github_issues.ps1 -IssueNumbers "4,5" -SkipClosingComment

    .\scripts\close_github_issues.ps1 -IssueNumber @(4,5) -SkipClosingComment
#>
param(
    [int[]] $IssueNumber = @(),
    [string] $IssueNumbers,
    [string] $Token,
    [string] $Owner = "liu-hui-ming",
    [string] $Repo = "hundred-crayfish-legion",
    [string] $Comment = "Closed as duplicate: same roadmap content was posted again by a second publish run. Keeping the newer [P1-Roadmap] pair (and Axium cross-links) as canonical.",
    [switch] $SkipClosingComment
)

$ErrorActionPreference = "Stop"
if (-not $Token) { $Token = $env:GH_TOKEN }
if (-not $Token) { $Token = $env:GITHUB_TOKEN }
if (-not $Token) {
    Write-Host "Set GH_TOKEN (or GITHUB_TOKEN, or -Token) with issues: write." -ForegroundColor Yellow
    exit 1
}

$issueIds = @()
if (-not [string]::IsNullOrWhiteSpace($IssueNumbers)) {
    $issueIds = @(
        $IssueNumbers -split '[,\s;]+' |
            ForEach-Object { $_.Trim() } |
            Where-Object { $_ -match '^\d+$' } |
            ForEach-Object { [int]$_ }
    ) | Sort-Object -Unique
} elseif ($IssueNumber -and $IssueNumber.Count -gt 0) {
    $issueIds = @($IssueNumber | Sort-Object -Unique)
} else {
    Write-Host "Specify -IssueNumbers '4,5' (recommended with powershell -File) or -IssueNumber @(4,5)." -ForegroundColor Yellow
    exit 2
}

$api = "https://api.github.com"
$headers = @{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent"           = "HCL-close-issues-ps1"
}

function Get-IssueMeta {
    param([int] $Number)
    $issueUri = "$api/repos/$Owner/$Repo/issues/${Number}"
    try {
        return Invoke-RestMethod -Uri $issueUri -Method Get -Headers $headers
    } catch {
        return $null
    }
}

function Close-OneIssue {
    param([int] $Number, [string] $ClosingComment, [bool] $SkipComment)

    $meta = Get-IssueMeta -Number $Number
    if (-not $meta) {
        Write-Host "Issue #$Number : GET failed (404). Repo https://github.com/$Owner/$Repo/issues/$Number - wrong -Owner/-Repo, issue deleted, or token cannot access this repository." -ForegroundColor Yellow
        return
    }
    Write-Host "Issue #$Number : found (state=$($meta.state))."
    if ($meta.state -eq "closed") {
        Write-Host "Issue #$Number : already closed - skipping." -ForegroundColor DarkGray
        return
    }

    if ((-not $SkipComment) -and $ClosingComment) {
        try {
            $json = ( [ordered]@{ body = $ClosingComment } | ConvertTo-Json -Depth 5 )
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
            $uri = "$api/repos/$Owner/$Repo/issues/${Number}/comments"
            Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -ContentType "application/json; charset=utf-8" -Body $bytes | Out-Null
            Write-Host "Issue #$Number : closing comment posted."
        } catch {
            Write-Warning "Issue #$Number : could not post closing comment ($($_.Exception.Message)). Retry with -SkipClosingComment or check token Issues permission."
        }
    }

    try {
        $patchJson = ( [ordered]@{ state = "closed" } | ConvertTo-Json )
        $patchBytes = [System.Text.Encoding]::UTF8.GetBytes($patchJson)
        $issueUri = "$api/repos/$Owner/$Repo/issues/${Number}"
        Invoke-RestMethod -Uri $issueUri -Method Patch -Headers $headers -ContentType "application/json; charset=utf-8" -Body $patchBytes | Out-Null
        Write-Host "Issue #$Number : closed." -ForegroundColor Green
    } catch {
        Write-Host "Issue #$Number : PATCH close failed - $($_.Exception.Message)" -ForegroundColor Red
    }
}

foreach ($n in $issueIds) {
    Close-OneIssue -Number $n -ClosingComment $Comment -SkipComment ([bool]$SkipClosingComment.IsPresent)
}

Write-Host "Done."
