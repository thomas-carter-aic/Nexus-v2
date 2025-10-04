#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.."; pwd)"
OUT="$ROOT/all-manifests.yml"
> "$OUT"
services=("workspace-service" "orchestration-service" "user-service" "infra-service" "ai-service")
for svc in "${services[@]}"; do
  CHART_DIR="$ROOT/services/$svc/helm/$svc"
  echo "Rendering chart for $svc"
  helm template "$svc" "$CHART_DIR" --values "$CHART_DIR/values.yaml" >> "$OUT"
done
echo "Applying manifests"
kubectl apply -f "$OUT"
echo "Deployed. Manifests file: $OUT"
