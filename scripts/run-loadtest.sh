#!/usr/bin/env bash
set -euo pipefail
TARGET=${1:-http://localhost:18080/events}
DURATION=${2:-30s}
VUS=${3:-5}
echo "Running k6 load test against $TARGET for $DURATION with $VUS VUs"
if ! command -v k6 >/dev/null 2>&1; then
  echo "k6 not installed. Please install k6: https://k6.io/docs/getting-started/installation/"
  exit 1
fi
k6 run --vus $VUS --duration $DURATION -e TARGET_URL="$TARGET" infra/loadtests/saga-load-test.js
