#!/bin/bash
# Post-deployment commands for AIC-AIPaaS

echo "🚀 AIC-AIPaaS Post-Deployment Setup"
echo "=================================="

# 1. Configure kubectl
echo "📋 Configuring kubectl..."
aws eks update-kubeconfig --region us-east-1 --name aic-aipaas-eks-dev

# 2. Verify cluster access
echo "🔍 Verifying cluster access..."
kubectl get nodes

# 3. Check node groups
echo "📊 Checking node groups..."
kubectl get nodes --show-labels

# 4. Install AWS Load Balancer Controller (required for ALB)
echo "🔧 Installing AWS Load Balancer Controller..."
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

# 5. Install NVIDIA GPU Operator (for AI/ML nodes)
echo "🎮 Installing NVIDIA GPU Operator..."
kubectl create namespace gpu-operator
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install --wait gpu-operator nvidia/gpu-operator -n gpu-operator

# 6. Create namespaces for AIC-AIPaaS services
echo "📦 Creating application namespaces..."
kubectl create namespace aic-aipaas
kubectl create namespace monitoring
kubectl create namespace ai-ml
kubectl create namespace serverless

# 7. Apply resource quotas and limits
echo "⚖️ Applying resource quotas..."
kubectl apply -f ../kubernetes/namespaces/

# 8. Show cluster info
echo "ℹ️ Cluster Information:"
kubectl cluster-info
kubectl get nodes -o wide

echo "✅ Post-deployment setup complete!"
echo "🔗 Next steps:"
echo "   1. Deploy AIC-AIPaaS services: make deploy"
echo "   2. Access monitoring: kubectl port-forward -n monitoring svc/grafana 3000:80"
echo "   3. Check GPU nodes: kubectl get nodes -l nvidia.com/gpu=true"
