#!/bin/bash

echo "📞 Installing Contact Management System Dependencies"
echo "================================================="

# Core contact form dependencies
npm install react-hook-form zod @hookform/resolvers

# Email and communication
npm install nodemailer @types/nodemailer

# File uploads and attachments
npm install multer @types/multer

# Calendar integration
npm install @calcom/embed-core ical-generator

# CRM integration (SuiteCRM already installed)
# Using existing SuiteCRM service

# Notification systems
npm install web-push @types/web-push

# Analytics and tracking
npm install @vercel/analytics mixpanel-browser

# Rate limiting and security
npm install express-rate-limit helmet

# Additional utilities
npm install uuid @types/uuid slugify

echo "✅ Contact system dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Run: chmod +x install-contact-system-deps.sh && ./install-contact-system-deps.sh"
echo "2. Configure environment variables"
echo "3. Set up contact database schema"
echo "4. Configure email templates and CRM integration"
