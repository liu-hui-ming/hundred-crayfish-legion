# OpenClaw 2.0 隔离测试环境启动脚本
# 用法: powershell -ExecutionPolicy Bypass -File .\start-v2test-gateway.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Node = Join-Path $Root "node-portable\node-v24.19.0-win-x64"
$Oc   = Join-Path $Root "cli-v2\node_modules\.bin\openclaw.cmd"

if (-not (Test-Path $Oc)) {
  Write-Error "OpenClaw 2026.8.1 not installed. Run setup first."
}

$env:PATH = "$Node;" + $env:PATH
Write-Host "Starting OpenClaw v2test Gateway on http://127.0.0.1:19001/"
Write-Host "Token: openclaw-v2test-2026"
& $Oc --profile v2test gateway run --port 19001 --force
