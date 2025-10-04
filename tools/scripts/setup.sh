#!/bin/bash

echo "🚀 Setting up Ultimate PaaS Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create environment files
echo "🔧 Setting up environment files..."
for app in dashboard app-management deployment ai-analytics plugin-management security monitoring; do
    if [ -f "apps/$app/.env.example" ] && [ ! -f "apps/$app/.env.local" ]; then
        cp "apps/$app/.env.example" "apps/$app/.env.local"
        echo "✅ Created apps/$app/.env.local"
    fi
done

# Build shared packages
echo "🔨 Building shared packages..."
npm run build --filter="@ultimate-paas/ui"
npm run build --filter="@ultimate-paas/types"
npm run build --filter="@ultimate-paas/auth"
npm run build --filter="@ultimate-paas/api-client"

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update environment variables in apps/*/env.local files"
echo "2. Start the backend server (ultimate-paas-base)"
echo "3. Run 'npm run dev' to start all microfrontends"
echo ""
echo "Individual microfrontend URLs:"
echo "- Dashboard: http://localhost:3000"
echo "- App Management: http://localhost:3001"
echo "- Deployment: http://localhost:3002"
echo "- AI Analytics: http://localhost:3003"
echo "- Plugin Management: http://localhost:3004"
echo "- Security: http://localhost:3005"
echo "- Monitoring: http://localhost:3006"
