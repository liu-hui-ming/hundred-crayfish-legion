# Session + approval exec E2E probe (v2test only; production NOT touched)
$ErrorActionPreference = "Continue"
$node = "E:\hundred-crayfish-legion\openclaw-test-v2\node-portable\node-v24.19.0-win-x64\node.exe"
$oc = "E:\hundred-crayfish-legion\openclaw-test-v2\cli-v2\node_modules\openclaw\openclaw.mjs"
$log = "E:\hundred-crayfish-legion\openclaw-test-v2\logs\session-approval-e2e-$(Get-Date -Format yyyyMMdd-HHmmss).log"
$lines = @(
  "Session + Approval E2E — $(Get-Date -Format o)",
  "profile: v2test · production: NOT TOUCHED",
  ""
)

function Add-Block([string]$title, [scriptblock]$cmd) {
  $script:lines += "=== $title ==="
  $out = & $cmd 2>&1 | Out-String
  $script:lines += $out.TrimEnd()
  $script:lines += ""
}

Add-Block "gateway status" { & $node $oc --profile v2test gateway status }
Add-Block "health" { & $node $oc --profile v2test health }
Add-Block "approvals get (exec policy)" { & $node $oc --profile v2test approvals get }
Add-Block "approvals pending" { & $node $oc --profile v2test approvals pending }
Add-Block "memory status --deep --json (session sources)" {
  & $node $oc --profile v2test memory status --deep --json
}

$storeDir = "E:\hundred-crayfish-legion\openclaw-test-v2\workspace\memory\.dreams"
if (Test-Path $storeDir) {
  $jsonFiles = Get-ChildItem -Path $storeDir -Recurse -Filter "*.json" -ErrorAction SilentlyContinue
  $lines += "=== session store file probe ==="
  $lines += "dreams_dir: $storeDir"
  $lines += "json_count: $($jsonFiles.Count)"
  $lines += ""
}

$lines += "=== E2E verdict ==="
$approvalsOut = & $node $oc --profile v2test approvals get 2>&1 | Out-String
if ($approvalsOut -match "exec policy" -or $approvalsOut -match "security=") {
  $lines += "RESULT: PASS — approvals get readable (exec policy surface OK)"
} else {
  $lines += "RESULT: PARTIAL — approvals get returned but exec policy string not matched"
}
$statusOut = & $node $oc --profile v2test memory status --deep --json 2>&1 | Out-String
if ($statusOut -match '"sessions"' -or $statusOut -match "sessionCorpus") {
  $lines += "RESULT: PASS — session source registered in memory status"
} else {
  $lines += "RESULT: PARTIAL — session block not found in memory status JSON"
}
$lines += ""

$lines | Set-Content $log -Encoding UTF8
Write-Host "Wrote $log"
