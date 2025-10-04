#!/bin/bash
# Build and push Docker images
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
for service in auth-service payment-service analytics-service realtime-service billing-service project-service communication-service ai-service admin; do
  cd services/$service || cd apps/$service
  docker build -t $DOCKER_REGISTRY/$service:latest .
  docker push $DOCKER_REGISTRY/$service:latest
  cd ../..
done
echo "Docker images built and pushed"
