#!/usr/bin/env sh
# P1: liveness + readiness
set -e
BASE="${1:-http://127.0.0.1:8765}"
echo "GET $BASE/api/health/live"
curl -sSf "$BASE/api/health/live" | cat
echo ""
echo "GET $BASE/api/health/ready"
curl -sS -f "$BASE/api/health/ready" | cat || true
echo ""
