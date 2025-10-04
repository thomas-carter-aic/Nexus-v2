#!/bin/bash

# Core dependencies
npm install react-hook-form zod @hookform/resolvers

# Database & ORM
npm install pg @types/pg prisma @prisma/client

# Queue system
npm install bullmq redis @types/redis

# HTTP client for CRM integration
npm install axios

# Development dependencies
npm install -D @types/node

echo "Dependencies installed successfully!"
echo "Next steps:"
echo "1. Run the installation script: chmod +x install-newsletter-deps.sh && ./install-newsletter-deps.sh"
echo "2. Set up environment variables"
echo "3. Initialize Prisma database"
