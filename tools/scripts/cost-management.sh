#!/bin/bash
# AIC-AIPaaS Cost Management Scripts
# Use these to scale up/down resources for testing

set -e

CLUSTER_NAME="aic-aipaas-eks-dev"
REGION="us-east-1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
echo_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Function to scale node groups
scale_node_group() {
    local node_group=$1
    local min_size=$2
    local desired_size=$3
    local max_size=$4
    
    echo_info "Scaling $node_group to min:$min_size, desired:$desired_size, max:$max_size"
    
    aws eks update-nodegroup-config \
        --cluster-name $CLUSTER_NAME \
        --nodegroup-name $node_group \
        --scaling-config minSize=$min_size,maxSize=$max_size,desiredSize=$desired_size \
        --region $REGION
}

# Function to get current node group status
get_node_status() {
    echo_info "Current Node Group Status:"
    aws eks describe-nodegroup --cluster-name $CLUSTER_NAME --nodegroup-name system-nodes --region $REGION --query 'nodegroup.scalingConfig' 2>/dev/null || echo "System nodes not found"
    aws eks describe-nodegroup --cluster-name $CLUSTER_NAME --nodegroup-name app-nodes --region $REGION --query 'nodegroup.scalingConfig' 2>/dev/null || echo "App nodes not found"
    aws eks describe-nodegroup --cluster-name $CLUSTER_NAME --nodegroup-name ai-ml-nodes --region $REGION --query 'nodegroup.scalingConfig' 2>/dev/null || echo "AI/ML nodes not found"
}

# Scale UP for testing
scale_up() {
    echo_info "🚀 Scaling UP for testing session..."
    
    # Scale system nodes (minimal for cluster operations)
    scale_node_group "system-nodes" 1 1 2
    
    # Scale app nodes for testing
    scale_node_group "app-nodes" 1 2 3
    
    # GPU nodes stay at 0 unless specifically requested
    if [[ "$1" == "--with-gpu" ]]; then
        echo_info "🎮 Including GPU nodes for AI/ML testing..."
        scale_node_group "ai-ml-nodes" 1 1 2
    fi
    
    echo_info "⏳ Waiting for nodes to be ready (this may take 3-5 minutes)..."
    kubectl wait --for=condition=Ready nodes --all --timeout=300s
    
    echo_info "✅ Cluster scaled UP and ready for testing!"
    kubectl get nodes
}

# Scale DOWN to save costs
scale_down() {
    echo_warn "💰 Scaling DOWN to save costs..."
    
    # Scale all node groups to 0
    scale_node_group "system-nodes" 0 0 2
    scale_node_group "app-nodes" 0 0 3
    scale_node_group "ai-ml-nodes" 0 0 2
    
    echo_info "✅ All nodes scaled down. Only EKS control plane running (~$73/month)"
    echo_warn "⚠️  Remember: You won't be able to run workloads until you scale up again"
}

# Quick test function
quick_test() {
    echo_info "🧪 Running quick infrastructure test..."
    
    # Scale up minimal resources
    scale_node_group "system-nodes" 1 1 1
    
    echo_info "⏳ Waiting for node to be ready..."
    sleep 120  # Give time for node to start
    
    # Run basic tests
    kubectl get nodes
    kubectl get pods --all-namespaces
    
    echo_info "✅ Quick test complete!"
    
    # Ask if user wants to scale down
    read -p "Scale down now to save costs? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        scale_down
    fi
}

# Cost estimation
estimate_costs() {
    echo_info "💵 Current Cost Estimation:"
    echo "EKS Control Plane: ~$73/month (always running)"
    echo "NAT Gateway: ~$45/month (always running)"
    echo "CloudWatch Logs: ~$5/month (minimal retention)"
    echo "S3 Storage: ~$5/month (minimal usage)"
    echo ""
    echo "Node Costs (when running):"
    echo "- System nodes (t3.small): ~$15/month per node"
    echo "- App nodes (t3.medium): ~$30/month per node"  
    echo "- GPU nodes (g4dn.xlarge): ~$150/month per node"
    echo ""
    echo "💡 Base cost (no nodes): ~$128/month"
    echo "💡 Minimal testing (1 system + 1 app): ~$173/month"
    echo "💡 Full testing (2 system + 2 app + 1 GPU): ~$343/month"
}

# Main menu
case "${1:-help}" in
    "up")
        scale_up $2
        ;;
    "down")
        scale_down
        ;;
    "status")
        get_node_status
        ;;
    "test")
        quick_test
        ;;
    "costs")
        estimate_costs
        ;;
    "help"|*)
        echo "AIC-AIPaaS Cost Management"
        echo "========================="
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  up [--with-gpu]  Scale up for testing (optionally include GPU nodes)"
        echo "  down             Scale down to save costs"
        echo "  status           Show current node group status"
        echo "  test             Run quick test and optionally scale down"
        echo "  costs            Show cost estimates"
        echo "  help             Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 up                    # Scale up for basic testing"
        echo "  $0 up --with-gpu         # Scale up including GPU nodes"
        echo "  $0 test                  # Quick test with auto-scale down option"
        echo "  $0 down                  # Scale down everything"
        ;;
esac
