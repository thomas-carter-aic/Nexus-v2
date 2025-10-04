Cert-Manager + Vault integration (dev sample)
This folder contains sample manifests and steps to configure cert-manager to use Vault as a CA through the cert-manager 'Vault' issuer type.
Security note: store Vault token in a Kubernetes secret and restrict access. For prod, configure proper auth method (Kubernetes auth + service account).
