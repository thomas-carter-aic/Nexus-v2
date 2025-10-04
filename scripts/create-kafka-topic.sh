#!/usr/bin/env bash
set -euo pipefail
NAMESPACE=${1:-kafka}
CLUSTER_NAME=${2:-my-cluster}
TOPIC=${3:-platform-events}
PARTITIONS=${4:-1}
REPLICATION=${5:-1}

echo "Creating topic $TOPIC on Strimzi cluster $CLUSTER_NAME in namespace $NAMESPACE"
POD=$(kubectl -n $NAMESPACE get pods -l strimzi.io/name=$CLUSTER_NAME-kafka -o jsonpath='{.items[0].metadata.name}')
echo "Using pod: $POD"
kubectl -n $NAMESPACE exec $POD -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic $TOPIC --partitions $PARTITIONS --replication-factor $REPLICATION
echo "Topic created."
