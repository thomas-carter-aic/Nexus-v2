#!/bin/bash

# Script to automate aic-aipaas project tree setup using Amazon Q Developer
# Date: July 10, 2025
# Owner: DevOps Lead (Thomas Carter)
# SRD Mappings: FR1–FR4, NFR3, NFR13–NFR15, TR2, TR4, R1

# Configuration
REPO_URL="https://github.com/thomas-carter-aic/aic-aipaas"
AWS_REGION="us-east-1"
AMAZON_Q_ENDPOINT="https://q.developer.aws"  # Placeholder for Amazon Q Developer API
AWS_ACCESS_KEY="your-access-key"  # Replace with actual key (stored in Vault, NFR15)
AWS_SECRET_KEY="your-secret-key"  # Replace with actual key
GITHUB_TOKEN="your-github-token"  # Replace with actual token (NFR15)

# Amazon Q Developer prompt for project tree
Q_PROMPT="Generate a GitHub monorepo structure for the AIC AI Platform (AIC-AIPaaS), an AI-native PaaS, with the following:
- Directories: microservices/auth, microservices/app-management, ai/models/train, ai/models/infer, ai/pipelines/synthetic-data, data/catalog, data/schemas, infrastructure/terraform/aws, infrastructure/terraform/azure, infrastructure/kubernetes/istio, infrastructure/kubernetes/prometheus, docs/api-specs, ci/github/workflows, ci/scripts
- Files: .gitignore (exclude node_modules, .env, *.log), LICENSE (MIT), README.md (project overview, setup: 'make setup'), .snyk, .pre-commit-config.yaml
- Subfiles: auth/src/main.py, auth/src/requirements.txt, auth/tests/test_auth.py, auth/Dockerfile, auth/helm/Chart.yaml, auth/helm/values.yaml, app-management/src/AppController.java, app-management/src/pom.xml, app-management/tests/AppControllerTest.java, app-management/Dockerfile, app-management/helm/Chart.yaml, app-management/helm/values.yaml, data/schemas/finance.json, data/schemas/healthcare.json, infrastructure/terraform/aws/eks_cluster.tf, infrastructure/kubernetes/istio/mtls.yaml, infrastructure/kubernetes/prometheus/prometheus-config.yaml, docs/architecture.md, docs/developer-guide.md, docs/runbook.md, docs/api-specs/auth.yaml, ci/github/workflows/ci.yml, ci/scripts/test.sh
Output as a directory structure and file contents in Markdown."

# Step 1: Initialize Git repository
echo "Initializing Git repository..."
git init aic-aipaas
cd aic-aipaas

# Step 2: Call Amazon Q Developer to generate project tree
echo "Generating project tree with Amazon Q Developer..."
curl -X POST "$AMAZON_Q_ENDPOINT" \
  -H "Authorization: AWS4-HMAC-SHA256 Credential=$AWS_ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"$Q_PROMPT\", \"max_tokens\": 5000, \"format\": \"markdown\"}" \
  -o project_tree.md

# Step 3: Parse and create directory structure
echo "Creating directories and files..."
mkdir -p microservices/auth/src microservices/auth/tests microservices/auth/helm
mkdir -p microservices/app-management/src microservices/app-management/tests microservices/app-management/helm
mkdir -p ai/models/train ai/models/infer ai/pipelines/synthetic-data
mkdir -p data/catalog/src data/catalog/tests data/schemas
mkdir -p infrastructure/terraform/aws infrastructure/terraform/azure infrastructure/kubernetes/istio infrastructure/kubernetes/prometheus
mkdir -p docs/api-specs ci/github/workflows ci/scripts

# Step 4: Create initial files (simplified contents for brevity)
cat > .gitignore << EOL
node_modules/
.env
*.log
EOL

cat > LICENSE << EOL
MIT License
Copyright (c) 2026 Applied Innovation Corporation
...
EOL

cat > README.md << EOL
# AIC Platform (AIC-P)
AI-native PaaS for scalable, secure applications.
## Setup
Clone: \`git clone https://github.com/thomas-carter/aic-aipaas\`
Run: \`make setup\`
EOL

cat > .snyk << EOL
# Snyk configuration for vulnerability scanning
version: v1.2
EOL

cat > .pre-commit-config.yaml << EOL
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
EOL

cat > microservices/auth/src/main.py << EOL
from flask import Flask
app = Flask(__name__)
@app.route('/v1/auth/token', methods=['POST'])
def get_token():
    return {"accessToken": "xyz", "expiresIn": 3600}
EOL

cat > microservices/auth/src/requirements.txt << EOL
flask==2.0.1
pyjwt==2.4.0
EOL

cat > microservices/auth/tests/test_auth.py << EOL
def test_get_token():
    response = client.post('/v1/auth/token', json={"clientId": "123"})
    assert response.status_code == 200
EOL

cat > microservices/auth/Dockerfile << EOL
FROM python:3.9
COPY src/ /app
RUN pip install -r /app/requirements.txt
CMD ["python", "/app/main.py"]
EOL

cat > microservices/auth/helm/Chart.yaml << EOL
apiVersion: v2
name: auth
version: 0.1.0
EOL

# Additional files (simplified for brevity)
touch microservices/app-management/src/AppController.java
touch microservices/app-management/src/pom.xml
touch microservices/app-management/tests/AppControllerTest.java
touch microservices/app-management/Dockerfile
touch microservices/app-management/helm/Chart.yaml
touch data/schemas/finance.json
touch data/schemas/healthcare.json
touch infrastructure/terraform/aws/eks_cluster.tf
touch infrastructure/kubernetes/istio/mtls.yaml
touch infrastructure/kubernetes/prometheus/prometheus-config.yaml
touch docs/architecture.md
touch docs/developer-guide.md
touch docs/runbook.md
touch docs/api-specs/auth.yaml
touch ci/github/workflows/ci.yml
touch ci/scripts/test.sh

# Step 5: Commit and push to GitHub
echo "Committing and pushing to GitHub..."
git add .
git commit -m "init: create monorepo structure with Amazon Q"
git remote add origin $REPO_URL
git push -u origin main --force

# Step 6: Validate setup
echo "Validating project tree..."
ls -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'

echo "Project tree setup complete."
