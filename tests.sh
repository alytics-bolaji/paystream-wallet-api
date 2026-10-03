#!/usr/bin/env bash
set -euo pipefail
 
echo "1/2 syntax check"
node --check wallet-api.js
 
echo "2/2 smoke test: /health says ok"
node wallet-api.js &
PID=$!
sleep 1
body=$(curl -fs http://localhost:3000/health)
echo "response: $body"
kill "$PID" 2>/dev/null || true
echo "$body" | grep -q '\"status\":\"ok\"'
echo "ALL TESTS PASSED"

