#!/bin/bash

echo "🚀 Setting up Newsletter System for AIC Website"
echo "=============================================="

# Check if required tools are installed
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed. Aborting." >&2; exit 1; }

echo "✅ Node.js and npm are installed"

# Install dependencies
echo "📦 Installing dependencies..."
npm install react-hook-form zod @hookform/resolvers pg @types/pg prisma @prisma/client bullmq redis @types/redis axios @types/node

echo "🗄️  Setting up database..."
# Initialize Prisma
npx prisma generate
npx prisma db push

echo "📝 Creating environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please update .env file with your actual configuration values:"
    echo "   - DATABASE_URL"
    echo "   - REDIS_URL"
    echo "   - SUITECRM_URL"
    echo "   - SUITECRM_USERNAME"
    echo "   - SUITECRM_PASSWORD"
fi

echo "🔧 Creating worker service script..."
cat > scripts/newsletter-worker.js << 'EOF'
#!/usr/bin/env node

// Import the worker
require('../src/lib/queue/newsletter-queue')

console.log('📧 Newsletter worker started...')
console.log('Press Ctrl+C to stop')

// Keep the process running
process.on('SIGINT', () => {
  console.log('\n👋 Newsletter worker shutting down...')
  process.exit(0)
})
EOF

chmod +x scripts/newsletter-worker.js

echo "📋 Creating package.json scripts..."
# Add scripts to package.json if they don't exist
npm pkg set scripts.newsletter:worker="node scripts/newsletter-worker.js"
npm pkg set scripts.db:migrate="prisma migrate dev"
npm pkg set scripts.db:generate="prisma generate"
npm pkg set scripts.db:studio="prisma studio"

echo ""
echo "✅ Newsletter system setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Update your .env file with actual configuration values"
echo "2. Make sure PostgreSQL and Redis are running"
echo "3. Run 'npm run newsletter:worker' to start the background worker"
echo "4. Add the NewsletterForm component to your pages"
echo ""
echo "🔧 Useful commands:"
echo "   npm run newsletter:worker  - Start the background worker"
echo "   npm run db:studio         - Open Prisma Studio"
echo "   npm run db:migrate        - Run database migrations"
echo ""
echo "📧 The newsletter form is ready to use!"
