# P0 acceptance: v2test Gateway + memory index + semantic/FTS/RAG/session/approval/weixin
# Production (~\.openclaw) MUST NOT be touched.
$ErrorActionPreference = "Continue"
$node = "E:\hundred-crayfish-legion\openclaw-test-v2\node-portable\node-v24.19.0-win-x64\node.exe"
$oc = "E:\hundred-crayfish-legion\openclaw-test-v2\cli-v2\node_modules\openclaw\openclaw.mjs"
$logDir = "E:\hundred-crayfish-legion\openclaw-test-v2\logs"
$ts = Get-Date -Format "yyyy-MM-ddTHH-mm-ss"
$log = Join-Path $logDir "P0-ACCEPTANCE-$ts.log"
$lines = @("P0 v2test Acceptance 鈥?$(Get-Date -Format o)", "profile: v2test 路 production: NOT TOUCHED", "")

function Add-Block([string]$title, [scriptblock]$cmd) {
  $script:lines += "=== $title ==="
  $out = & $cmd 2>&1 | Out-String
  $script:lines += $out.TrimEnd()
  $script:lines += ""
}

Add-Block "gateway status" { & $node $oc --profile v2test gateway status }
Add-Block "health" { & $node $oc --profile v2test health }
Add-Block "memory index --force" { & $node $oc --profile v2test memory index --force }
Add-Block "memory status --deep --json" { & $node $oc --profile v2test memory status --deep --json }
Add-Block "semantic search (RAG-PRIMARY-ZERO-POWER)" {
  & $node $oc --profile v2test memory search --query "RAG-PRIMARY-ZERO-POWER-AXIOM-V1.0" --max-results 2
}
Add-Block "semantic search (100-open-inquiries)" {
  & $node $oc --profile v2test memory search --query "100 open AI industry inquiries" --max-results 2
}
Add-Block "FTS keyword search (Ch1_鏈簮鍏悊 filename token)" {
  & $node $oc --profile v2test memory search --query "Ch1_鏈簮鍏悊" --max-results 2
}
Add-Block "plugins inspect openclaw-weixin" { & $node $oc --profile v2test plugins inspect openclaw-weixin }
Add-Block "approvals get" { & $node $oc --profile v2test approvals get }
Add-Block "approvals pending" { & $node $oc --profile v2test approvals pending }

$lines += "=== semantic/FTS no-degradation check ==="
$statusJson = & $node $oc --profile v2test memory status --deep --json 2>$null | Out-String
if ($statusJson -match '"semanticAvailable"\s*:\s*true' -and $statusJson -match '"state"\s*:\s*"complete"') {
  $lines += "RESULT: PASS 鈥?vector complete + semanticAvailable true (not FTS-only fallback)"
} elseif ($statusJson -match '"available"\s*:\s*true' -and $statusJson -match '"fts"') {
  $lines += "RESULT: PARTIAL 鈥?FTS available; verify vector block manually"
} else {
  $lines += "RESULT: FAIL 鈥?inspect memory status JSON above"
}
$lines += ""

$lines | Set-Content $log -Encoding UTF8
Write-Host "Wrote $log"
