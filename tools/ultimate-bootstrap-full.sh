#!/usr/bin/env bash
set -euo pipefail

# Ultimate One-Command Monorepo Bootstrap Script
# - Interactive polyglot scaffold (apps/services/packages)
# - Multi-env kind clusters (dev, staging, prod)
# - cert-manager (cluster-aware for Kind/minikube)
# - Ingress manifests generation with TLS (self-signed)
# - Helm chart scaffolding per app/service
# - GitOps manifests for FluxCD & ArgoCD
# - Install FluxCD & ArgoCD (local bootstrapping)
# - Env configmaps, feature-flags, secrets application
# - /etc/hosts patching for local subdomains
#
# WARNING: This script is intended for local development. Review before running.
# Dependencies you should have installed: kubectl, kind, helm, yq, flux (optional), curl, jq, git, entr (optional)
#
# Run: chmod +x ultimate-bootstrap-full.sh && ./ultimate-bootstrap-full.sh

echo "🚀 Ultimate Monorepo Bootstrap — starting..."

# ---------------------------
# 1) Interactive setup
# ---------------------------
read -p "Package manager (npm/yarn/pnpm) [pnpm]: " PKG_MANAGER
PKG_MANAGER=${PKG_MANAGER:-pnpm}

read -p "Languages (ts,go,py,java,rs) [ts]: " LANGUAGES
LANGUAGES=${LANGUAGES:-ts}

read -p "Web bundler (vite,webpack,rollup) [vite]: " WEB_BUNDLER
WEB_BUNDLER=${WEB_BUNDLER:-vite}

read -p "CI/CD tool (github-actions/gitlab-ci/jenkins) [github-actions]: " CICD_TOOL
CICD_TOOL=${CICD_TOOL:-github-actions}

read -p "Cluster environments (comma-separated) [dev,staging,prod]: " ENVIRONMENTS
ENVIRONMENTS=${ENVIRONMENTS:-dev,staging,prod}
IFS=',' read -ra ENV_ARRAY <<< "$ENVIRONMENTS"

CLUSTER_PREFIX="monorepo"
BASE_DOMAIN="local.monorepo"
OUTPUT_DIR="infra/k8s"
HELM_DIR="infra/helm"

echo "Preferences summary:"
echo "  Package manager: $PKG_MANAGER"
echo "  Languages: $LANGUAGES"
echo "  Web bundler: $WEB_BUNDLER"
echo "  CI/CD tool: $CICD_TOOL"
echo "  Environments: ${ENV_ARRAY[*]}"

# ---------------------------
# 2) Folder scaffolding
# ---------------------------
echo "📁 Creating repository folders..."
FOLDERS=(
  "apps/web" "apps/cli" "apps/mobile" "apps/admin" "apps/landing" "apps/desktop"
  "services"
  "packages/ui-react" "packages/ui-native" "packages/utils" "packages/config"
  "packages/logging" "packages/telemetry" "packages/errors" "packages/http" "packages/rpc"
  "packages/sdk" "packages/contracts" "packages/graphql" "packages/types" "packages/protos"
  "packages/openapi" "packages/db" "packages/db-migrations" "packages/auth"
  "packages/feature-flags" "packages/test-helpers" "packages/mock-server"
  "packages/ci-helpers" "packages/release" "packages/eslint-config"
  "packages/prettier-config" "packages/tsconfig" "packages/storybook-config"
  "packages/docsite" "packages/cli-helpers" "packages/i18n" "packages/feature"
  "packages/notifications" "packages/ci-images" "packages/templates" "packages/codegen"
  "packages/benchmarks"
  "infra/bootstrap" "infra/stacks" "infra/terraform" "infra/helm" "infra/k8s"
  "infra/kustomize" "infra/helmfile" "infra/argocd" "infra/flux" "infra/docker-compose"
  "infra/kind" "infra/minikube" "infra/localstack" "infra/cert-manager" "infra/ingress"
  "infra/secrets" "infra/monitoring" "infra/observability" "infra/service-mesh" "infra/network"
  "infra/database" "infra/storage" "infra/ci-cd" "infra/registry" "infra/runner"
  "infra/alerting" "infra/playbooks" "infra/vm-images" "infra/packer" "infra/ansible"
  "infra/policies" "infra/cost" "infra/backups" "docs"
)

for d in "${FOLDERS[@]}"; do
  mkdir -p "$d"
done
echo "✅ Folder scaffold created."

# ---------------------------
# 3) Bootstrap minimal files for apps/services/packages
# ---------------------------
echo "✨ Creating minimal bootstrap files (polyglot)..."
for dir in apps/* services packages/*; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")
  for lang in $(echo $LANGUAGES | tr ',' ' '); do
    case $lang in
      ts)
        mkdir -p "$dir/src"
        cat > "$dir/src/index.ts" <<TS
export const hello = () => "Hello from $name (ts)";
TS
        ;;
      go)
        cat > "$dir/main.go" <<GO
package main
import "fmt"
func main(){ fmt.Println("Hello from $name (go)") }
GO
        ;;
      py)
        cat > "$dir/main.py" <<PY
def main():
    print("Hello from $name (py)")

if __name__ == "__main__":
    main()
PY
        ;;
      rs)
        mkdir -p "$dir/src"
        cat > "$dir/src/main.rs" <<RS
fn main() {
    println!("Hello from $name (rs)");
}
RS
        ;;
      java)
        mkdir -p "$dir/src/main/java/com/example"
        cat > "$dir/src/main/java/com/example/Main.java" <<JAVA
package com.example;
public class Main {
  public static void main(String[] args){
    System.out.println("Hello from $name (java)");
  }
}
JAVA
        ;;
      *)
        echo "Unknown lang $lang — skipping"
        ;;
    esac
  done

  # Add a simple deployment/service stub for k8s (helps auto-detection)
  mkdir -p "$dir/k8s"
  cat > "$dir/k8s/deployment.yaml" <<DEP
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${name}
  template:
    metadata:
      labels:
        app: ${name}
    spec:
      containers:
      - name: ${name}
        image: nginx:stable
        ports:
        - containerPort: 80
DEP

  cat > "$dir/k8s/service.yaml" <<SVC
apiVersion: v1
kind: Service
metadata:
  name: ${name}
spec:
  type: ClusterIP
  selector:
    app: ${name}
  ports:
    - port: 80
      targetPort: 80
SVC

done
echo "✅ Bootstrap files added for apps/services/packages."

# ---------------------------
# 4) Create kind clusters for each environment
# ---------------------------
echo "🔧 Creating kind clusters for environments: ${ENV_ARRAY[*]}"

for env in "${ENV_ARRAY[@]}"; do
  CLUSTER_NAME="${CLUSTER_PREFIX}-${env}"
  if kind get clusters | grep -q "${CLUSTER_NAME}"; then
    echo "Cluster ${CLUSTER_NAME} already exists — skipping creation."
  else
    echo "Creating kind cluster ${CLUSTER_NAME}..."
    cat > /tmp/kind-config-${env}.yaml <<KINDCFG
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 8080
  - containerPort: 443
    hostPort: 8443
KINDCFG
    kind create cluster --name "${CLUSTER_NAME}" --config /tmp/kind-config-${env}.yaml
    rm -f /tmp/kind-config-${env}.yaml
  fi
done
echo "✅ Kind clusters created/available."

# ---------------------------
# helper: detect local cluster by context
# ---------------------------
is_local_cluster() {
  context="$1"
  # For kind contexts format is "kind-<name>"
  if [[ "$context" == kind-* ]]; then
    return 0
  fi
  # minikube context contains "minikube"
  if [[ "$context" == *minikube* ]]; then
    return 0
  fi
  return 1
}

# ---------------------------
# 5) Install cert-manager (cluster-aware)
# ---------------------------
echo "💉 Installing cert-manager (cluster-aware, local clusters will skip webhook validation)..."
CERT_MANAGER_YAML="https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml"

for env in "${ENV_ARRAY[@]}"; do
  CLUSTER="${CLUSTER_PREFIX}-${env}"
  CTX="kind-${CLUSTER}"
  echo "Installing cert-manager into context ${CTX}..."

  if is_local_cluster "${CTX}"; then
    echo "Detected local cluster (${CTX}) — applying cert-manager with --validate=false"
    kubectl --context "${CTX}" apply -f "${CERT_MANAGER_YAML}" --validate=false
    echo "Skipping webhook readiness checks for local cluster ${CTX}"
  else
    kubectl --context "${CTX}" apply -f "${CERT_MANAGER_YAML}"
    echo "Waiting for cert-manager deployments to be ready (with retries)..."
    DEPLOYS=(cert-manager cert-manager-webhook cert-manager-cainjector)
    for dep in "${DEPLOYS[@]}"; do
      echo "Waiting for ${dep}..."
      for i in {1..60}; do
        READY=$(kubectl --context "${CTX}" -n cert-manager get deploy "${dep}" -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo 0)
        DESIRED=$(kubectl --context "${CTX}" -n cert-manager get deploy "${dep}" -o jsonpath='{.status.replicas}' 2>/dev/null || echo 0)
        if [[ -n "${DESIRED}" && "${READY}" == "${DESIRED}" ]]; then
          echo "✅ ${dep} ready"
          break
        fi
        echo "⏳ ${dep} not ready (attempt ${i}/60). Sleeping 5s..."
        sleep 5
      done
    done
  fi

  # Create self-signed ClusterIssuer
  cat <<EOF | kubectl --context "${CTX}" apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
EOF

  echo "ClusterIssuer created in ${CTX}"
done
echo "✅ cert-manager installation finished for all clusters."

# ---------------------------
# 6) Generate Ingress manifests dynamically (per env)
# ---------------------------
echo "🌐 Generating Ingress manifests (infra/k8s)..."
mkdir -p "${OUTPUT_DIR}"

HOSTS=()
for env in "${ENV_ARRAY[@]}"; do
  for dir in apps/* services/*; do
    [ -d "$dir" ] || continue
    name=$(basename "$dir")
    host="${name}.${env}.${BASE_DOMAIN}"
    HOSTS+=("${host}")
    out="${OUTPUT_DIR}/${name}-ingress-${env}.yaml"

    # detect ports from k8s stubs (fallback to 80)
    PORTS=$(grep -E 'containerPort: ' "${dir}/k8s/deployment.yaml" 2>/dev/null | awk '{print $2}' || echo "80")
    PORTS=$(echo "${PORTS}" | tr '\n' ',' | sed 's/,$//')

    cat > "${out}" <<ING
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${name}-ingress-${env}
  annotations:
    cert-manager.io/cluster-issuer: "selfsigned-issuer"
spec:
  tls:
  - hosts:
    - ${host}
    secretName: ${host}-tls
  rules:
  - host: ${host}
    http:
      paths:
ING

    IFS=',' read -ra PARR <<< "${PORTS}"
    for p in "${PARR[@]}"; do
      cat >> "${out}" <<RULE
      - path: /port${p}
        pathType: Prefix
        backend:
          service:
            name: ${name}
            port:
              number: ${p}
RULE
    done

    echo "Generated ${out} (host=${host}, ports=${PORTS})"
  done
done
echo "✅ Ingress manifests generated."

# Apply generated ingresses to clusters
for env in "${ENV_ARRAY[@]}"; do
  CTX="kind-${CLUSTER_PREFIX}-${env}"
  echo "Applying ingress manifests to ${CTX}..."
  kubectl --context "${CTX}" apply -f "${OUTPUT_DIR}/"
done

# ---------------------------
# 7) Env configmaps, feature-flags, secrets
# ---------------------------
echo "🔐 Applying environment configmaps and secrets (if present)..."
for env in "${ENV_ARRAY[@]}"; do
  CTX="kind-${CLUSTER_PREFIX}-${env}"
  if [ -f "packages/config/${env}.yaml" ]; then
    kubectl --context "${CTX}" create configmap "${env}-config" --from-file=packages/config/${env}.yaml --dry-run=client -o yaml | kubectl apply -f -
    echo "Applied packages/config/${env}.yaml -> configmap ${env}-config"
  fi
  if [ -f "packages/feature-flags/${env}.yaml" ]; then
    kubectl --context "${CTX}" create configmap "${env}-feature-flags" --from-file=packages/feature-flags/${env}.yaml --dry-run=client -o yaml | kubectl apply -f -
    echo "Applied packages/feature-flags/${env}.yaml -> configmap ${env}-feature-flags"
  fi
  if [ -f "infra/secrets/${env}-secrets.yaml" ]; then
    kubectl --context "${CTX}" apply -f "infra/secrets/${env}-secrets.yaml"
    echo "Applied infra/secrets/${env}-secrets.yaml"
  fi
done

# ---------------------------
# 8) Helm chart scaffolding (one chart per app/service)
# ---------------------------
echo "⛵ Scaffolding Helm charts for apps and services..."
mkdir -p "${HELM_DIR}"
for dir in apps/* services/*; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")
  chart="${HELM_DIR}/${name}"
  mkdir -p "${chart}/templates"

  cat > "${chart}/Chart.yaml" <<CH
apiVersion: v2
name: ${name}
description: Helm chart for ${name}
type: application
version: 0.1.0
appVersion: "1.0"
CH

  cat > "${chart}/values.yaml" <<VY
replicaCount: 1
image:
  repository: ${name}
  tag: latest
service:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 80
ingress:
  enabled: true
  hosts:
    - host: ${name}.local.monorepo
      paths:
        - /
  tls: []
env: {}
VY

  for env in "${ENV_ARRAY[@]}"; do
    cp "${chart}/values.yaml" "${chart}/values-${env}.yaml"
  done

  # templates/deployment.yaml
  cat > "${chart}/templates/deployment.yaml" <<DEP
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "${name}.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ include "${name}.name" . }}
  template:
    metadata:
      labels:
        app: {{ include "${name}.name" . }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
{{- range .Values.service.ports }}
        - containerPort: {{ .targetPort }}
{{- end }}
        envFrom:
        - configMapRef:
            name: {{ .Values.env.CONFIGMAP_NAME | default "default-config" }}
        - secretRef:
            name: {{ .Values.env.SECRET_NAME | default "default-secret" }}
DEP

  # templates/service.yaml
  cat > "${chart}/templates/service.yaml" <<SVC
apiVersion: v1
kind: Service
metadata:
  name: {{ include "${name}.fullname" . }}
spec:
  type: {{ .Values.service.type }}
  selector:
    app: {{ include "${name}.name" . }}
  ports:
{{- range .Values.service.ports }}
  - port: {{ .port }}
    targetPort: {{ .targetPort }}
{{- end }}
SVC

  # templates/ingress.yaml
  cat > "${chart}/templates/ingress.yaml" <<ING
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "${name}.fullname" . }}-ingress
  annotations:
    cert-manager.io/cluster-issuer: "selfsigned-issuer"
spec:
  tls:
{{- range .Values.ingress.tls }}
  - hosts:
    - {{ .host }}
    secretName: {{ .secretName }}
{{- end }}
  rules:
{{- range .Values.ingress.hosts }}
  - host: {{ .host }}
    http:
      paths:
      {{- range .paths }}
      - path: {{ . }}
        pathType: Prefix
        backend:
          service:
            name: {{ include "${name}.fullname" . }}
            port:
              number: {{ $.Values.service.ports[0].port }}
      {{- end }}
{{- end }}
{{- end }}
ING

  echo "  - Helm chart scaffolded for ${name}"
done
echo "✅ Helm charts created."

# ---------------------------
# 9) GitOps manifests (Flux + ArgoCD)
# ---------------------------
echo "🔗 Generating GitOps manifests for Flux and ArgoCD..."
mkdir -p infra/gitops/flux/apps infra/gitops/argocd/apps

for dir in apps/* services/*; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")

  cat > "infra/gitops/flux/apps/${name}.yaml" <<F
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: ${name}
  namespace: flux-system
spec:
  interval: 5m
  path: ./../../../../infra/helm/${name}
  prune: true
  sourceRef:
    kind: GitRepository
    name: monorepo
  targetNamespace: default
F

  cat > "infra/gitops/argocd/apps/${name}.yaml" <<A
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ${name}
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/monorepo
    targetRevision: HEAD
    path: infra/helm/${name}
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
A

  echo "  - GitOps manifests created for ${name}"
done
echo "✅ GitOps manifests generated."

# ---------------------------
# 10) Install FluxCD (bootstrap)
# ---------------------------
echo "⚡ Installing FluxCD into clusters (bootstrap)..."

if ! command -v flux >/dev/null 2>&1; then
  echo "Flux CLI not found — installing..."
  curl -s https://fluxcd.io/install.sh | sudo bash
fi

for env in "${ENV_ARRAY[@]}"; do
  CTX="kind-${CLUSTER_PREFIX}-${env}"
  echo "Bootstrapping Flux into ${CTX} (this may require GitHub credentials or adjust flags)..."
  # Note: flux bootstrap requires a reachable Git provider and repo permissions.
  # For local demos you might prefer to install controllers only:
  kubectl --context "${CTX}" create namespace flux-system >/dev/null 2>&1 || true
  kubectl --context "${CTX}" apply -f https://github.com/fluxcd/flux2/releases/latest/download/manifests-components.yaml
  echo "Installed Flux controllers in ${CTX} (manual Git bootstrap may be required)"
done
echo "✅ Flux controllers installed in clusters."

# ---------------------------
# 11) Install ArgoCD
# ---------------------------
echo "⚡ Installing ArgoCD into clusters..."

for env in "${ENV_ARRAY[@]}"; do
  CTX="kind-${CLUSTER_PREFIX}-${env}"
  echo "Installing ArgoCD in ${CTX}..."
  kubectl --context "${CTX}" create namespace argocd >/dev/null 2>&1 || true
  kubectl --context "${CTX}" apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  echo "Waiting for ArgoCD to be available in ${CTX}..."
  kubectl --context "${CTX}" -n argocd wait --for=condition=available deployment --all --timeout=300s || true
  echo "ArgoCD installed in ${CTX}"
done
echo "✅ ArgoCD installed."

# ---------------------------
# 12) Apply GitOps manifests to clusters (optional)
# ---------------------------
echo "⤴ Applying GitOps manifests to clusters (Flux kustomizations + ArgoCD Applications)..."
for env in "${ENV_ARRAY[@]}"; do
  CTX="kind-${CLUSTER_PREFIX}-${env}"
  kubectl --context "${CTX}" apply -f infra/gitops/flux/apps/ --recursive || true
  kubectl --context "${CTX}" apply -f infra/gitops/argocd/apps/ --recursive || true
done
echo "✅ GitOps manifests applied (controllers will reconcile as configured)."

# ---------------------------
# 13) Apply Helm charts (install example-chart) to clusters (optional)
# ---------------------------
echo "🚀 Installing sample Helm charts into clusters..."
for env in "${ENV_ARRAY[@]}"; do
  CTX="kind-${CLUSTER_PREFIX}-${env}"
  for chart in "${HELM_DIR}"/*; do
    [ -d "$chart" ] || continue
    name=$(basename "$chart")
    echo "Installing/upgrading helm chart ${name} into ${CTX} (namespace: default)..."
    helm --kube-context "${CTX}" upgrade --install "${name}" "${chart}" -n default --create-namespace --wait || true
  done
done
echo "✅ Helm chart install/upgrade attempted."

# ---------------------------
# 14) /etc/hosts entries for generated hosts
# ---------------------------
echo "🖧 Adding /etc/hosts entries for local subdomains..."
for host in "${HOSTS[@]}"; do
  if ! grep -q "${host}" /etc/hosts; then
    echo "127.0.0.1 ${host}" | sudo tee -a /etc/hosts >/dev/null
    echo "  - added ${host}"
  fi
done
echo "✅ /etc/hosts updated."

# ---------------------------
# 15) Final messages
# ---------------------------
echo ""
echo "🎉 Ultimate Bootstrap complete!"
echo "Clusters: ${ENV_ARRAY[*]} (kind-${CLUSTER_PREFIX}-<env>)"
echo "Ingress hosts added to /etc/hosts for local access. Example URLs:"
for h in "${HOSTS[@]}"; do
  echo "  https://${h}/port80"
done
echo ""
echo "Notes:"
echo " - Flux bootstrap (full Git integration) may require GitHub/GitLab access tokens and manual 'flux bootstrap' step."
echo " - For production clusters, rerun cert-manager without --validate=false and ensure webhook readiness."
echo " - Review and secure any default passwords or secrets before sharing or pushing to remote repos."
echo ""
echo "Done."
