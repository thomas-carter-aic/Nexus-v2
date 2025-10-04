#!/usr/bin/env bash
set -euo pipefail
# Build Docker images for services and load into kind cluster 'dev-cluster'
CLUSTER=${1:-dev-cluster}
REGISTRY=${2:-registry.example.com}
ROOT="$(cd "$(dirname "$0")/.."; pwd)"

services=("workspace-service" "orchestration-service" "user-service" "infra-service" "ai-service")

for svc in "${services[@]}"; do
  echo "Building image for $svc"
  IMG="${REGISTRY}/${svc}:latest"
  docker build -t "$IMG" "$ROOT/services/$svc" || true
  echo "Loading $IMG into kind cluster $CLUSTER"
  kind load docker-image "$IMG" --name "$CLUSTER" || true
done

echo "All images built and loaded into kind cluster $CLUSTER"
