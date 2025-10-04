#!/bin/bash
# Update ArgoCD applications with new image tags
SERVICE=$1
TAG=$2
if [ -z "$SERVICE" ] || [ -z "$TAG" ]; then
  echo "Usage: $0 <service> <tag>"
  exit 1
fi
cd gitops/kustomize/dev
sed -i "s|$DOCKER_REGISTRY/$SERVICE:.*|$DOCKER_REGISTRY/$SERVICE:$TAG|" kustomization.yaml
kustomize build . > ../../manifests/dev-$SERVICE.yaml
cd ../prod
sed -i "s|$DOCKER_REGISTRY/$SERVICE:.*|$DOCKER_REGISTRY/$SERVICE:$TAG|" kustomization.yaml
kustomize build . > ../../manifests/prod-$SERVICE.yaml
cd ../..
git config user.name "Script"
git config user.email "script@monorepo.com"
git add manifests/
git commit -m "Update $SERVICE to $TAG"
git push
argocd app sync $SERVICE --namespace argocd
echo "Updated $SERVICE to $TAG"
