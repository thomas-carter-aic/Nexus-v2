#!/bin/bash

echo "📋 Installing AI Readiness Assessment Dependencies"
echo "==============================================="

# Core assessment dependencies
npm install react-hook-form zod @hookform/resolvers

# PDF generation
npm install puppeteer @react-pdf/renderer jspdf html2canvas

# File handling and storage
npm install multer @types/multer minio

# Email delivery
npm install nodemailer @types/nodemailer

# Additional utilities
npm install uuid @types/uuid date-fns

# Chart generation for reports
npm install chart.js chartjs-node-canvas

# Development dependencies
npm install -D @types/node

echo "✅ Dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Run: chmod +x install-assessment-deps.sh && ./install-assessment-deps.sh"
echo "2. Configure environment variables"
echo "3. Set up assessment database schema"
echo "4. Configure PDF templates"
