ADR 0001: Adoption of Apache Kafka for Event-Driven Architecture
Status
Accepted
Context
The monorepo requires an event-driven architecture with CQRS and event sourcing to support microservices. A robust event store is needed for scalability and fault tolerance.
Decision
Adopt Apache Kafka as the event store for publishing and consuming events across Python, Go, Java, and Node.js services.
Consequences

Pros: Scalability, fault tolerance, polyglot support via clients (confluent-kafka, sarama, spring-kafka, kafkajs).
Cons: Increased complexity in managing Kafka brokers.
Mitigation: Deploy Kafka via ArgoCD (gitops/manifests/kafka.yaml).

Date
2025-07-18
