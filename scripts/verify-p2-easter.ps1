# P2 彩蛋短验证（无长时压测）
# 用法: $env:HCL_BASE_URL="http://127.0.0.1:8765"; .\scripts\verify-p2-easter.ps1
# 服务须已用 $env:HCL_P2_EASTER="1" 启动。
param([string]$Base = $env:HCL_BASE_URL)
if (-not $Base) { $Base = "http://127.0.0.1:8765" }
$Base = $Base.TrimEnd("/")
Write-Host "GET $Base/api/health/live"
$live = Invoke-RestMethod "$Base/api/health/live"
if (-not $live.PSObject.Properties["hcl_p2_easter"]) {
    Write-Warning "No hcl_p2_easter in response — server may be old build."
} else {
    Write-Host "hcl_p2_easter =" $live.hcl_p2_easter
}
Write-Host "GET $Base/api/p2/easter-egg"
try {
    $egg = Invoke-RestMethod "$Base/api/p2/easter-egg"
    Write-Host "OK p2 =" $egg.p2
} catch {
    Write-Warning "easter-egg not available (404 expected if HCL_P2_EASTER not set on server process)."
    exit 1
}
Write-Host "P2 easter short check done."
