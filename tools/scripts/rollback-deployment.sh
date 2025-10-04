#!/bin/bash
# Roll back ArgoCD application to previous version
SERVICE=$1
if [ -z "$SERVICE" ]; then
  echo "Usage: $0 <service>"
  exit 1
fi
argocd app history $SERVICE --namespace argocd
echo "Enter revision number to rollback to:"
read REVISION
argocd app rollback $SERVICE $REVISION --namespace argocd
echo "Rolled back $SERVICE to revision $REVISION"
