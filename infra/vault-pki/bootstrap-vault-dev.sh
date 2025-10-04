#!/usr/bin/env bash
set -euo pipefail
helm repo add bitnami https://charts.bitnami.com/bitnami || true
helm repo update
kubectl create namespace vault || true
helm install vault bitnami/vault -n vault --set "server.dev.enabled=true" || true
kubectl -n vault port-forward svc/vault 8200:8200 &
echo "Vault dev started; port-forwarded to 8200"
