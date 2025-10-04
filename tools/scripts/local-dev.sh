#!/bin/bash
# Local Development Environment Setup
# Test everything locally before deploying to AWS

set -e

echo "🏠 Setting up Local AIC-AIPaaS Development Environment"
echo "===================================================="

# Check prerequisites
check_prerequisites() {
    echo "🔍 Checking prerequisites..."
    
    command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
    command -v kind >/dev/null 2>&1 || { echo "❌ Kind is required but not installed."; exit 1; }
    command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl is required but not installed."; exit 1; }
    command -v helm >/dev/null 2>&1 || { echo "❌ Helm is required but not installed."; exit 1; }
    
    echo "✅ All prerequisites found!"
}

# Install missing tools
install_tools() {
    echo "🔧 Installing missing development tools..."
    
    # Install Kind (Kubernetes in Docker)
    if ! command -v kind &> /dev/null; then
        echo "Installing Kind..."
        curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
        chmod +x ./kind
        sudo mv ./kind /usr/local/bin/kind
    fi
    
    # Install kubectl if not present
    if ! command -v kubectl &> /dev/null; then
        echo "Installing kubectl..."
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
    fi
    
    # Install Helm if not present
    if ! command -v helm &> /dev/null; then
        echo "Installing Helm..."
        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    fi
}

# Create local Kubernetes cluster
create_local_cluster() {
    echo "🚀 Creating local Kubernetes cluster..."
    
    # Create Kind cluster with custom configuration
    cat <<EOF | kind create cluster --name aic-aipaas-local --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
- role: worker
EOF

    echo "✅ Local cluster created!"
}

# Deploy local services
deploy_local_services() {
    echo "📦 Deploying AIC-AIPaaS services locally..."
    
    # Create namespaces
    kubectl create namespace aic-aipaas --dry-run=client -o yaml | kubectl apply -f -
    kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
    kubectl create namespace ai-ml --dry-run=client -o yaml | kubectl apply -f -
    
    # Deploy using docker-compose equivalent in Kubernetes
    cd /home/oss/Business/aic-aipaas
    
    # Use local development configuration
    export ENVIRONMENT=local
    make dev-local
    
    echo "✅ Services deployed locally!"
}

# Show access information
show_access_info() {
    echo "🔗 Local Development Access Information:"
    echo "======================================="
    echo "Cluster: kind-aic-aipaas-local"
    echo "Context: kind-aic-aipaas-local"
    echo ""
    echo "Services:"
    kubectl get services --all-namespaces
    echo ""
    echo "Pods:"
    kubectl get pods --all-namespaces
    echo ""
    echo "💡 To access services:"
    echo "   kubectl port-forward -n aic-aipaas svc/auth-service 8080:80"
    echo "   kubectl port-forward -n monitoring svc/grafana 3000:80"
    echo ""
    echo "🧹 To cleanup:"
    echo "   kind delete cluster --name aic-aipaas-local"
}

# Cleanup function
cleanup() {
    echo "🧹 Cleaning up local environment..."
    kind delete cluster --name aic-aipaas-local
    echo "✅ Cleanup complete!"
}

# Main execution
case "${1:-setup}" in
    "setup")
        check_prerequisites
        install_tools
        create_local_cluster
        deploy_local_services
        show_access_info
        ;;
    "cleanup")
        cleanup
        ;;
    "info")
        show_access_info
        ;;
    *)
        echo "Usage: $0 [setup|cleanup|info]"
        echo "  setup   - Create local development environment"
        echo "  cleanup - Remove local development environment"
        echo "  info    - Show access information"
        ;;
esac
