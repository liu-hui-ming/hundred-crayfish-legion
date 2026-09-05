# RAG hit verification for P1 synced documents (v2test only)
$ErrorActionPreference = "Continue"
$oc = "E:\hundred-crayfish-legion\openclaw-test-v2\cli-v2\node_modules\.bin\openclaw.cmd"
$env:PATH = "E:\hundred-crayfish-legion\openclaw-test-v2\node-portable\node-v24.19.0-win-x64;" + $env:PATH
$log = "E:\hundred-crayfish-legion\openclaw-test-v2\logs\rag-hit-verification-20260905.log"
$queries = @(
  @{ q = "Why Are We V1.0 T-02 Y-04"; expect = "Why-Are-We-V1.0" },
  @{ q = "zero power axiom manifesto"; expect = "00-zero-power-axiom" },
  @{ q = "100 open AI industry inquiries"; expect = "100-open-inquiries" },
  @{ q = "Lin Qingxiang 10 questions"; expect = "10-questions" },
  @{ q = "0⁰=1=∞=0 本源公理"; expect = "Ch1_本源公理" }
)
$lines = @("RAG Hit Verification — $(Get-Date -Format o)", "")
foreach ($item in $queries) {
  $lines += "=== QUERY: $($item.q) (expect: $($item.expect)) ==="
  $raw = & $oc --profile v2test memory search --query $item.q --max-results 3 2>&1 | Out-String
  $hits = ($raw -split "`n") | Where-Object { $_ -match "memory/" -or $_ -match "^\d\.\d{3}" }
  $match = $hits | Where-Object { $_ -match [regex]::Escape($item.expect) }
  if ($match) { $lines += "RESULT: PASS — $($match | Select-Object -First 1)" }
  else {
    $lines += "RESULT: PARTIAL — top hits:"
    $lines += ($hits | Select-Object -First 3)
  }
  $lines += ""
}
$lines | Set-Content $log -Encoding UTF8
Write-Host "Wrote $log"
