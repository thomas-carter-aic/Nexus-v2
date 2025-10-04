# Setup Guide

## Prerequisites
- Docker, Docker Compose
- Node.js 20, pnpm, Rush
- Python 3.11, Go 1.22, Java 21
- Kubernetes cluster (e.g., Minikube)
- ArgoCD, Vault

## Installation
1. Run setup script: \`bash tools/scripts/setup-dev.sh\`
2. Install ArgoCD: \`bash tools/scripts/install-argocd.sh\`
3. Install Vault: \`bash tools/scripts/vault-init.sh\`
4. Install dependencies: \`rush update\`
5. Build: \`pnpm turbo run build\`, \`cd services/analytics-service && ./gradlew build\`, \`cd services/payment-service && go build\`, \`cd services/auth-service && pip install -r requirements.txt\`

## Local Development
- Start services: \`docker-compose -f docker-compose.dev.yml up\`
- Run web app: \`pnpm --filter web dev\`
- Access ArgoCD: \`kubectl port-forward svc/argocd-server -n argocd 9000:443\`

## Environment Variables
- Set \`KAFKA_BOOTSTRAP_SERVERS=kafka:9092\` in \`.env\`.
- Configure xAI API key in \`tools/ai-analyzer/analyze.py\` and \`tools/codegen/generate.py\`.

