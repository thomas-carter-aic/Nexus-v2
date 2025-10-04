#!/usr/bin/env bash
set -euo pipefail
echo "This script bootstraps a local dev environment using kind + Helm + Strimzi + Apicurio + Jaeger + Prometheus + Grafana."
echo "It DOES NOT run in this environment automatically. Run these commands on your machine with kubectl, kind, helm installed."

cat <<'DOC'
Prerequisites:
- Docker running
- kind installed (https://kind.sigs.k8s.io/)
- kubectl installed and configured
- helm installed
- kubectl access to created cluster

Quick steps (manual or copy/paste):
1. Create kind cluster:
   kind create cluster --name dev-cluster --config ./infra/kind-config.yaml
2. Install Strimzi (Kafka operator):
   helm repo add strimzi https://strimzi.io/charts/
   helm repo update
   kubectl create namespace kafka || true
   helm install strimzi strimzi/strimzi-kafka-operator -n kafka
   # Apply a Strimzi Kafka cluster YAML (see infra/examples/strimzi-kafka.yaml)
   kubectl apply -f infra/examples/strimzi-kafka.yaml -n kafka
3. Install Apicurio Registry (schema registry)
   helm repo add apicurio https://apicurio.github.io/apicurio-registry-charts/
   helm repo update
   kubectl create namespace schema || true
   helm install apicurio apicurio/apicurio-registry -n schema
4. Install Jaeger, Prometheus, Grafana:
   helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo add grafana https://grafana.github.io/helm-charts
   helm repo update
   kubectl create namespace observability || true
   helm install jaeger jaegertracing/jaeger -n observability
   helm install prometheus prometheus-community/prometheus -n observability
   helm install grafana grafana/grafana -n observability
5. Deploy services (examples provided under services/*/helm):
   # build and push images to a registry accessible by the cluster (minikube/Kind may use local registry)
   kubectl apply -f services/workspace-service/helm/deployment.yaml -n default
   kubectl apply -f services/orchestration-service/helm/deployment.yaml -n default
   kubectl apply -f services/user-service/helm/deployment.yaml -n default
   kubectl apply -f services/ai-service/helm/deployment.yaml -n default
   kubectl apply -f services/infra-service/helm/deployment.yaml -n default
6. Create Kafka topics (see scripts/create-kafka-topic.sh)
7. Use kubectl port-forward to access services and dashboards.
DOC
