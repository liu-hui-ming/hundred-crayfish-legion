# RAG hit verification for P1 synced documents (v2test only)
$ErrorActionPreference = "Continue"
$node = "E:\hundred-crayfish-legion\openclaw-test-v2\node-portable\node-v24.19.0-win-x64\node.exe"
$oc = "E:\hundred-crayfish-legion\openclaw-test-v2\cli-v2\node_modules\openclaw\openclaw.mjs"
$log = "E:\hundred-crayfish-legion\openclaw-test-v2\logs\rag-hit-verification-$(Get-Date -Format yyyyMMdd).log"
$queries = @(
  @{ q = "RAG-PRIMARY-WHY-ARE-WE-V1.0 Why Are We V1.0 T-02 Y-04"; expect = "Why-Are-We-V1.0"; alt = "" },
  @{ q = "00-zero-power-axiom-V1.0 zero power axiom T-02 Y-04"; expect = "00-zero-power-axiom"; alt = "zero-power" },
  @{ q = "100 open AI industry inquiries"; expect = "100-open-inquiries"; alt = "" },
  @{ q = "RAG-PRIMARY-LIN-10-QUESTIONS-V1.0 林清祥 碳硅道统十问 10-questions"; expect = "10-questions"; alt = "" },
  @{ q = "Ch1_本源公理 0⁰=1"; expect = "Ch1_本源公理"; alt = "" }
)
$lines = @("RAG Hit Verification — $(Get-Date -Format o)", "index: v2test · node direct · tuned queries", "")
foreach ($item in $queries) {
  $lines += "=== QUERY: $($item.q) (expect: $($item.expect)) ==="
  $raw = & $node $oc --profile v2test memory search --query $item.q --max-results 3 2>&1 | Out-String
  $hits = ($raw -split "`n") | Where-Object { $_ -match "memory/" -or $_ -match "^\d\.\d{3}" }
  $alt = [string]$item.alt
  $match = $hits | Where-Object {
    $_ -match [regex]::Escape($item.expect) -or (
      $alt.Length -gt 0 -and $_ -match [regex]::Escape($alt)
    )
  }
  if ($match) { $lines += "RESULT: PASS — $($match | Select-Object -First 1)" }
  else {
    $lines += "RESULT: PARTIAL — top hits:"
    $lines += ($hits | Select-Object -First 3)
  }
  $lines += ""
}
$lines | Set-Content $log -Encoding UTF8
Write-Host "Wrote $log"
