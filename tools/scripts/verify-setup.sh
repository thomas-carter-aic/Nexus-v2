#!/bin/bash
set -e

echo "🔍 Verifying development environment setup..."

# Test Docker
echo "Testing Docker..."
docker --version

# Test Node.js
echo "Testing Node.js..."
node --version
npm --version

# Test Python
echo "Testing Python..."
python3 --version
source .venv/bin/activate
pip --version

# Test Java
echo "Testing Java..."
java --version

# Test Go
echo "Testing Go..."
go version

echo "✅ All tools verified successfully!"
