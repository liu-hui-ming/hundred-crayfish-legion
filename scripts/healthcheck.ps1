# P1: readiness/liveness (PowerShell) — 默认 http://127.0.0.1:8765
param(
    [string] $Base = "http://127.0.0.1:8765"
)
$ErrorActionPreference = "Stop"
$live = Invoke-RestMethod -Uri "$Base/api/health/live" -Method Get
Write-Host "live:" ($live | ConvertTo-Json -Compress)
$code = 0
try {
    $ready = Invoke-RestMethod -Uri "$Base/api/health/ready" -Method Get
    Write-Host "ready:" ($ready | ConvertTo-Json -Compress)
} catch {
    $code = 1
    Write-Warning "ready: $_"
}
exit $code
