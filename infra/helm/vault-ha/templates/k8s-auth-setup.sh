#!/usr/bin/env bash
set -euo pipefail
# Use this script after deploying Vault to enable Kubernetes auth and create a role for cert-manager / external-secrets
VAULT_ADDR=${VAULT_ADDR:-http://vault.vault.svc:8200}
kubectl -n vault exec deploy/vault -- vault auth enable kubernetes || true
kubectl -n vault exec deploy/vault -- sh -c "vault write auth/kubernetes/config token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token kubernetes_host=https://kubernetes.default.svc && echo 'k8s auth configured'"
kubectl -n vault exec deploy/vault -- vault write auth/kubernetes/role/cert-manager bound_service_account_names=cert-manager bound_service_account_namespaces=cert-manager policies=cert-manager-pki ttl=24h || true
echo "Kubernetes auth role 'cert-manager' created in Vault."
