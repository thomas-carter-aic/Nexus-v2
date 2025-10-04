Flagger + Argo Rollouts:
Install Flagger (supports Istio, Linkerd, NGINX) and Argo Rollouts for canary deployments.
helm repo add flagger https://flagger.app
helm install flagger flagger/flagger -n flagger-system --create-namespace
helm repo add argo https://argoproj.github.io/argo-helm
helm install argo-rollouts argo/argo-rollouts -n argo-rollouts --create-namespace
