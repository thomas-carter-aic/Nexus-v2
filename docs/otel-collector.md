# OpenTelemetry Collector

The repo includes a Helm chart under infra/helm/otel-collector. The Collector receives OTLP from services and exports to Jaeger & Prometheus remote write.

In production, configure additional receivers/exporters and a secure endpoint.
