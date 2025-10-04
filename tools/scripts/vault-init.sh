#!/bin/bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault --namespace vault --create-namespace
kubectl exec -n vault vault-0 -- vault operator init
echo "Vault initialized. Retrieve keys from Vault pod logs."
