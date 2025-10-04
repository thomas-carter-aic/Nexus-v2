#!/usr/bin/env bash
set -euo pipefail
export VAULT_ADDR=${VAULT_ADDR:-http://127.0.0.1:8200}
vault secrets enable -path=pki pki || true
vault write -field=certificate pki/root/generate/internal common_name="dev.local" ttl=87600h > CA_cert.crt || true
vault write pki/config/urls issuing_certificates="${VAULT_ADDR}/v1/pki/ca" crl_distribution_points="${VAULT_ADDR}/v1/pki/crl" || true
vault write pki/roles/otel-collector allowed_domains="cluster.local" allow_subdomains=true max_ttl="72h" || true
echo "PKI role created: pki/roles/otel-collector"
