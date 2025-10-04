schema-registry module skeleton


## Local Dev Usage (example)
This module is a skeleton. For local development we recommend using `kind` or `k3d` to create a local k8s cluster,
then install platform components via Helm. Example steps:

1. Install kind: https://kind.sigs.k8s.io/
2. Create a cluster:
   ```
   kind create cluster --name dev-cluster
   ```
3. Install Strimzi (Kafka) via Helm:
   ```
   helm repo add strimzi https://strimzi.io/charts/
   helm repo update
   helm install strimzi-kafka strimzi/strimzi-kafka-operator
   ```
4. Deploy a Kafka cluster using Strimzi CRDs (see examples/ in this repo)
5. Install Schema Registry (Confluent OSS) or Apicurio via Helm
6. Install Jaeger (observability) and Prometheus/Grafana via community charts:
   ```
   helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
   helm install jaeger jaegertracing/jaeger
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm install prometheus prometheus-community/prometheus
   helm repo add grafana https://grafana.github.io/helm-charts
   helm install grafana grafana/grafana
   ```
7. Use `kubectl port-forward` or LoadBalancer to access dashboards.
