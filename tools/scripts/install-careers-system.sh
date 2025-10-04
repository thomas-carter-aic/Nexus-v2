#!/bin/bash

# Job Application System Installation Script
# This script sets up the complete development environment for the AIC careers system

set -e

echo "🚀 Installing AIC Job Application System..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    print_error "package.json not found. Please run this script from the project root directory."
    exit 1
fi

print_info "Step 1: Checking system requirements..."

# Check Node.js version
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

print_status "Node.js version check passed: $(node -v)"

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm and try again."
    exit 1
fi

print_status "npm is available: $(npm -v)"

print_info "Step 2: Installing dependencies..."

# Install dependencies if not already installed
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    npm install
    print_status "Dependencies installed successfully"
else
    print_status "Dependencies already installed"
fi

print_info "Step 3: Setting up PostgreSQL database..."

# Make database setup script executable
chmod +x scripts/setup-database.sh

# Run database setup
if ./scripts/setup-database.sh; then
    print_status "PostgreSQL database setup completed"
else
    print_warning "Database setup encountered issues. You may need to set it up manually."
    print_info "Please ensure PostgreSQL is installed and running, then run: ./scripts/setup-database.sh"
fi

print_info "Step 4: Setting up environment configuration..."

# Copy environment file if it doesn't exist
if [ ! -f ".env.local" ]; then
    cp .env.careers.example .env.local
    print_status "Environment file created from template"
    print_warning "Please update .env.local with your actual configuration values"
else
    print_info "Environment file already exists"
fi

print_info "Step 5: Setting up Prisma and database schema..."

# Generate Prisma client
npm run db:generate
print_status "Prisma client generated"

# Push database schema
if npm run db:push; then
    print_status "Database schema pushed successfully"
else
    print_warning "Database schema push failed. Please check your database connection."
fi

print_info "Step 6: Creating upload directories..."

# Create upload directories
mkdir -p uploads/resumes
mkdir -p uploads/temp
chmod 755 uploads
chmod 755 uploads/resumes
chmod 755 uploads/temp

print_status "Upload directories created"

print_info "Step 7: Seeding database with sample data..."

# Seed database
if npm run db:seed; then
    print_status "Database seeded with sample job postings"
else
    print_warning "Database seeding failed. You can run 'npm run db:seed' manually later."
fi

print_info "Step 8: Testing email configuration..."

# Test email configuration (optional)
if [ -n "$SMTP_USER" ] && [ -n "$SMTP_PASS" ]; then
    print_status "Email configuration detected"
else
    print_warning "Email configuration not found. Please update .env.local with SMTP settings."
fi

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
print_status "Job Application System has been successfully installed!"
echo ""
echo "📋 Next Steps:"
echo "1. Update .env.local with your actual configuration values:"
echo "   - Database connection string"
echo "   - SMTP email settings"
echo "   - File upload paths"
echo ""
echo "2. Start the development server:"
echo "   npm run careers:dev"
echo ""
echo "3. Visit the application:"
echo "   - Main site: http://localhost:3000"
echo "   - Careers page: http://localhost:3000/careers"
echo "   - Admin portal: http://localhost:3000/admin"
echo ""
echo "📚 Available Commands:"
echo "   npm run careers:dev    - Start development server with DB generation"
echo "   npm run db:studio      - Open Prisma Studio (database GUI)"
echo "   npm run db:seed        - Seed database with sample data"
echo "   npm run db:reset       - Reset database (WARNING: deletes all data)"
echo ""
echo "🔧 Configuration Files:"
echo "   .env.local             - Environment variables"
echo "   prisma/schema.prisma   - Database schema"
echo "   lib/email.ts           - Email service configuration"
echo "   lib/storage.ts         - File storage configuration"
echo ""
print_info "For troubleshooting, check the documentation in docs/ directory"
echo ""
