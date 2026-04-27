#!/usr/bin/env bash
# 「少轮次 + 探活为主」常规回归（10 轮可改）
# 用法: bash scripts/run-genesis-n-rounds.sh [轮次，默认 10]
# 环境:
#   OPENCLAW_URL   — 若设置，则每轮对 GET $OPENCLAW_URL/health 或根路径探活（-f 失败即非 0 退出）
#   HCL_BASE_URL   — 可选，默认 http://127.0.0.1:8765 ，对 /api/health/live 探活（本仓同盟服务）
# 说明: 完整 Genesis 长链路在独立仓；此处为 HCL 仓内「轻量轮次 + 探活」脚本，满足 P1 回归形态。

set -euo pipefail

ROUNDS="${1:-10}"
if ! [[ "$ROUNDS" =~ ^[0-9]+$ ]] || [[ "$ROUNDS" -lt 1 ]]; then
  echo "usage: $0 [rounds>=1]" >&2
  exit 2
fi

HCL_BASE_URL="${HCL_BASE_URL:-http://127.0.0.1:8765}"

probe() {
  local name="$1" url="$2"
  if curl -sfS "$url" >/dev/null; then
    echo "  ok $name"
    return 0
  fi
  echo "  FAIL $name ($url)" >&2
  return 1
}

echo "[run-genesis-n-rounds] rounds=$ROUNDS (probe-only mode)"

for ((r = 1; r <= ROUNDS; r++)); do
  echo "--- round $r / $ROUNDS ---"
  probe hcl-live "${HCL_BASE_URL}/api/health/live" || exit 1
  if [[ -n "${OPENCLAW_URL:-}" ]]; then
    gh="${OPENCLAW_URL%/}"
    if curl -sfS "${gh}/health" >/dev/null 2>&1; then
      echo "  ok openclaw /health"
    elif curl -sfS "$gh" >/dev/null 2>&1; then
      echo "  ok openclaw root"
    else
      echo "  FAIL openclaw (${gh})" >&2
      exit 1
    fi
  else
    echo "  (skip openclaw: OPENCLAW_URL unset)"
  fi
  sleep 0.2
done

echo "[run-genesis-n-rounds] done: $ROUNDS rounds, all probes passed."
exit 0
