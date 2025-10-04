#!/usr/bin/env bash
# operator-run.sh
set -euo pipefail

function confirm() {
  read -p "$1 [y/N]: " -r REPLY
  case "$REPLY" in
    [yY][eE][sS]|[yY]) return 0 ;;
    *) return 1 ;;
  esac
}

ROOT="$(cd "$(dirname "$0")/.."; pwd)"
echo "Operator-run starting from $ROOT"

read -p "Kind cluster name (default: dev-cluster): " CLUSTER
CLUSTER=${CLUSTER:-dev-cluster}

read -p "Container registry prefix (default: registry.example.com): " REGISTRY
REGISTRY=${REGISTRY:-registry.example.com}

read -p "Vault address (for External Secrets) (default: https://vault.example.internal): " VAULT_ADDR
VAULT_ADDR=${VAULT_ADDR:-https://vault.example.internal}

echo
echo "You entered:"
echo "  Cluster: $CLUSTER"
echo "  Registry: $REGISTRY"
echo "  Vault Address: $VAULT_ADDR"
echo

if ! confirm "Proceed with these settings?"; then
  echo "Aborted by user."
  exit 1
fi

export KIND_CLUSTER_NAME="$CLUSTER"
export REGISTRY_PREFIX="$REGISTRY"
export VAULT_ADDR="$VAULT_ADDR"

echo "Creating kind cluster (if not exists)..."
if kind get clusters | grep -q "^$CLUSTER$"; then
  echo "Kind cluster $CLUSTER already exists — skipping creation."
else
  kind create cluster --name "$CLUSTER" --config "$ROOT/infra/kind-config.yaml"
fi

echo "Installing base infra and k8s addons..."
bash "$ROOT/scripts/make-dev-up.sh" "$CLUSTER" || true

echo "Building and loading images into kind..."
bash "$ROOT/scripts/build-and-load-images.sh" "$CLUSTER" "$REGISTRY" || true

echo "Rendering and applying Helm charts for platform services..."
bash "$ROOT/scripts/deploy-kind.sh" || true

echo "Creating Kafka topic 'platform-events'..."
bash "$ROOT/scripts/create-kafka-topic.sh" kafka my-cluster platform-events || true

echo "Applying Istio mTLS helper..."
kubectl apply -f "$ROOT/infra/k8s/istio-mtls-default.yaml" || true

echo "Apply Prometheus alerting rules for SLOs and DLQ..."
kubectl apply -f "$ROOT/infra/monitoring/prometheus-rules/platform-alerts.yaml" || true

echo "Apply Grafana dashboards..."
kubectl apply -f "$ROOT/observability/grafana/dashboards/platform-overview-grafana.yaml" || true

if confirm "Run a quick k6 load test?"; then
  bash "$ROOT/scripts/run-loadtest.sh" || true
fi

echo "Operator-run completed."
