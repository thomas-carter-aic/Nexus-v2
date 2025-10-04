#!/bin/bash
set -e

echo "🚀 Setting up AICP development environment..."

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check Java
if ! command -v java &> /dev/null; then
    echo "❌ Java is required but not installed"
    exit 1
fi

# Check Go
if ! command -v go &> /dev/null; then
    echo "❌ Go is required but not installed"
    exit 1
fi

echo "✅ All prerequisites found"

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Set up Python virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Create Python requirements file
cat > requirements.txt << 'PYTHON_EOF'
# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.0

# AI/ML dependencies
torch==2.1.0
transformers==4.35.0
scikit-learn==1.3.0
numpy==1.24.3
pandas==2.0.3

# Data processing
apache-beam==2.51.0
kafka-python==2.0.2
redis==5.0.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.0

# Development
black==23.10.1
isort==5.12.0
flake8==6.1.0
mypy==1.7.0
PYTHON_EOF

pip install -r requirements.txt

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'make test' to verify everything works"
echo "2. Run 'docker-compose up -d' to start local services"
echo "3. Visit http://localhost:3000 for the dashboard"
