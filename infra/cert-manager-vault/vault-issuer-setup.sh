#!/usr/bin/env bash
set -euo pipefail
vault secrets enable -path=pki pki || true
vault write pki/roles/cert-manager-otel allow_any_name=true allowed_domains="cluster.local" allow_subdomains=true max_ttl="72h" || true
cat > /tmp/cm-policy.hcl <<'HCL'
path "pki/issue/cert-manager-otel" { capabilities = ["create", "update"] }
HCL
vault policy write cert-manager-pki /tmp/cm-policy.hcl || true
echo "Created policy cert-manager-pki; create token and store in secret vault-token in namespace cert-manager."
