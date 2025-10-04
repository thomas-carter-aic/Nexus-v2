#!/usr/bin/env bash
set -euo pipefail
IMAGE=$1
if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image>"
  exit 2
fi
which syft >/dev/null || curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
which trivy >/dev/null || curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
which cosign >/dev/null || curl -sSfL https://raw.githubusercontent.com/sigstore/cosign/main/install.sh | sh -s -- -b /usr/local/bin
syft $IMAGE -o json > sbom.json
trivy image --format json --output trivy-report.json $IMAGE || true
echo $COSIGN_PASSWORD | cosign generate-key-pair
cosign sign --key cosign.key $IMAGE
echo "SBOM and signature produced."
