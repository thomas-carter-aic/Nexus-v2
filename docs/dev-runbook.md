# Dev Runbook: Local Kind + Platform Services

This guide shows how to bring up the full local dev environment and run integration tests.

## Prerequisites
- Docker
- kind
- kubectl
- helm
- Go 1.20
- Node.js & npm
- Maven (for Java services)

## Quick start (all-in-one)
1. Create kind cluster and install platform components:

```bash
./scripts/make-dev-up.sh dev-cluster
```

This will:
- create a kind cluster
- install Strimzi (Kafka operator) and apply an example Kafka cluster
- install Apicurio (schema registry)
- install Jaeger, Prometheus, Grafana
- install Postgres (bitnami)
- build and load service images into kind
- deploy Helm charts
- create Kafka topic `platform-events`

## Run integration tests locally (or in CI)
From the repo root:

```bash
cd services/orchestration-service
go test ./... -v
```

This test suite uses dockertest to spin up a temporary Postgres container and runs the orchestration binary via `go run`.

## Troubleshooting
- If `go test` fails due to Docker permissions, ensure Docker daemon accessible by current user and that GitHub Actions runner allows Docker-in-Docker.
- If migrations fail, check `POSTGRES_URL` and connectivity. You can port-forward the Postgres pod or exec into the pod to inspect logs.
- If Kafka-related operations fail, ensure Strimzi and Kafka cluster are healthy (`kubectl -n kafka get pods`).

## Notes
- The runbook is for local dev only; secrets are insecure and for demo purposes.
- For CI, the workflow `services/orchestration-service/.github/workflows/integration.yml` runs the integration test on GitHub runners.

## Secrets & Vault
We added ExternalSecrets templates and a ClusterSecretStore example to integrate with HashiCorp Vault via external-secrets operator. In production configure Vault server and Kubernetes auth.

## OpenTelemetry & Metrics
Services include simple OpenTelemetry console exporters and Prometheus metrics endpoints. Replace console exporters with OTLP exporters to send to collector in production.
