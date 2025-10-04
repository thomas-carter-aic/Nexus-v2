#!/bin/bash

echo "🧠 Setting up AI Readiness Assessment System"
echo "==========================================="

# Check if required tools are installed
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed. Aborting." >&2; exit 1; }

echo "✅ Node.js and npm are installed"

# Install dependencies
echo "📦 Installing assessment dependencies..."
npm install react-hook-form zod @hookform/resolvers puppeteer @react-pdf/renderer jspdf html2canvas multer @types/multer minio nodemailer @types/nodemailer uuid @types/uuid date-fns chart.js chartjs-node-canvas @types/node

echo "🗄️  Setting up database schema..."
# Add assessment schema to existing Prisma schema
if [ -f "prisma/schema.prisma" ]; then
    echo "// Assessment Models - Added by setup-assessment.sh" >> prisma/schema.prisma
    cat prisma/schema-assessment.prisma >> prisma/schema.prisma
    echo "✅ Assessment schema added to existing Prisma schema"
else
    echo "⚠️  Prisma schema not found. Please manually add the assessment schema."
fi

# Generate Prisma client and push schema
npx prisma generate
npx prisma db push

echo "📁 Creating storage directories..."
mkdir -p storage/assessments
mkdir -p storage/reports
mkdir -p logs

echo "📝 Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.assessment.example .env
    echo "⚠️  Please update .env file with your actual configuration values:"
    echo "   - SMTP_* variables for email delivery"
    echo "   - STORAGE_PATH for file storage"
    echo "   - PDF generation settings"
else
    echo "⚠️  Please add assessment configuration to your existing .env file"
    echo "   See .env.assessment.example for required variables"
fi

echo "🔧 Creating worker service scripts..."

# Assessment worker script
cat > scripts/assessment-worker.js << 'EOF'
#!/usr/bin/env node

// Import the assessment workers
require('../src/lib/queue/assessment-queue')

console.log('🧠 Assessment processing workers started...')
console.log('📊 Report generation worker started...')
console.log('📧 Email delivery worker started...')
console.log('Press Ctrl+C to stop all workers')

// Keep the process running
process.on('SIGINT', () => {
  console.log('\n👋 Assessment workers shutting down...')
  process.exit(0)
})
EOF

chmod +x scripts/assessment-worker.js

# PDF generation test script
cat > scripts/test-pdf.js << 'EOF'
#!/usr/bin/env node

const { pdfGenerator } = require('../src/lib/services/pdf-generator')

async function testPDFGeneration() {
  console.log('🧪 Testing PDF generation...')
  
  const testData = {
    id: 'test-123',
    companyName: 'Test Company',
    contactName: 'John Doe',
    email: 'john@testcompany.com',
    overallScore: 75,
    categoryScores: {
      strategy: 80,
      data: 70,
      technology: 75,
      talent: 65,
      governance: 85,
      culture: 70,
      processes: 75,
      infrastructure: 80
    },
    responses: [],
    createdAt: new Date(),
    recommendations: [],
    benchmarks: {
      industryAverage: 62,
      topPerformers: 85,
      yourPosition: 'above-average'
    }
  }
  
  try {
    const pdfBuffer = await pdfGenerator.generateAssessmentReport(testData)
    console.log('✅ PDF generated successfully:', pdfBuffer.length, 'bytes')
    
    // Save test PDF
    const fs = require('fs').promises
    await fs.writeFile('./test-report.pdf', pdfBuffer)
    console.log('📄 Test PDF saved as test-report.pdf')
    
  } catch (error) {
    console.error('❌ PDF generation failed:', error)
  } finally {
    await pdfGenerator.close()
  }
}

testPDFGeneration()
EOF

chmod +x scripts/test-pdf.js

# Email test script
cat > scripts/test-email.js << 'EOF'
#!/usr/bin/env node

const { emailService } = require('../src/lib/services/email-service')

async function testEmailService() {
  console.log('📧 Testing email service...')
  
  try {
    const isConnected = await emailService.verifyConnection()
    if (isConnected) {
      console.log('✅ Email service connection successful')
    } else {
      console.log('❌ Email service connection failed')
    }
  } catch (error) {
    console.error('❌ Email service test failed:', error)
  }
}

testEmailService()
EOF

chmod +x scripts/test-email.js

echo "📋 Adding package.json scripts..."
# Add scripts to package.json
npm pkg set scripts.assessment:worker="node scripts/assessment-worker.js"
npm pkg set scripts.assessment:test-pdf="node scripts/test-pdf.js"
npm pkg set scripts.assessment:test-email="node scripts/test-email.js"
npm pkg set scripts.assessment:dev="concurrently \"npm run dev\" \"npm run assessment:worker\""

echo "🎨 Creating admin dashboard route..."
mkdir -p src/app/admin/assessment
cat > src/app/admin/assessment/page.tsx << 'EOF'
'use client'

import { useState, useEffect } from 'react'
import { FileText, Users, CheckCircle, XCircle, Clock, AlertTriangle, Download } from 'lucide-react'

interface AssessmentStats {
  total: number
  completed: number
  processing: number
  failed: number
  recentSubmissions: Array<{
    id: string
    email: string
    companyName: string
    overallScore: number
    status: string
    createdAt: string
    reportGenerated: boolean
  }>
}

export default function AssessmentAdminPage() {
  const [stats, setStats] = useState<AssessmentStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock data - replace with actual API call
    setTimeout(() => {
      setStats({
        total: 342,
        completed: 298,
        processing: 12,
        failed: 32,
        recentSubmissions: [
          {
            id: '1',
            email: 'john@company.com',
            companyName: 'Tech Corp',
            overallScore: 78,
            status: 'COMPLETED',
            createdAt: '2024-01-15T10:30:00Z',
            reportGenerated: true
          },
          {
            id: '2',
            email: 'sarah@startup.com',
            companyName: 'AI Startup',
            overallScore: 0,
            status: 'PROCESSING',
            createdAt: '2024-01-15T09:15:00Z',
            reportGenerated: false
          }
        ]
      })
      setLoading(false)
    }, 1000)
  }, [])

  if (loading) {
    return <div className="p-6">Loading...</div>
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Assessment Management</h1>
        <p className="text-gray-600">Monitor AI readiness assessments and report generation</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Assessments</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.total.toLocaleString()}</p>
            </div>
            <FileText className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-green-600">{stats?.completed.toLocaleString()}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Processing</p>
              <p className="text-2xl font-bold text-yellow-600">{stats?.processing.toLocaleString()}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Failed</p>
              <p className="text-2xl font-bold text-red-600">{stats?.failed.toLocaleString()}</p>
            </div>
            <XCircle className="h-8 w-8 text-red-600" />
          </div>
        </div>
      </div>

      {/* Recent Assessments */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Assessments</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {stats?.recentSubmissions.map((assessment) => (
                <tr key={assessment.id}>
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                    {assessment.companyName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                    {assessment.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {assessment.overallScore > 0 ? (
                      <span className="font-medium">{assessment.overallScore}/100</span>
                    ) : (
                      <span className="text-gray-400">Calculating...</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      assessment.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
                      assessment.status === 'PROCESSING' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {assessment.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                    {new Date(assessment.createdAt).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {assessment.reportGenerated && (
                      <button className="text-blue-600 hover:text-blue-800">
                        <Download className="h-4 w-4" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
EOF

echo ""
echo "✅ AI Readiness Assessment system setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Update your .env file with SMTP and storage configuration"
echo "2. Make sure PostgreSQL and Redis are running"
echo "3. Test PDF generation: npm run assessment:test-pdf"
echo "4. Test email service: npm run assessment:test-email"
echo "5. Start the assessment workers: npm run assessment:worker"
echo "6. Visit /assessment to test the form"
echo ""
echo "🔧 Useful commands:"
echo "   npm run assessment:worker     - Start background workers"
echo "   npm run assessment:test-pdf   - Test PDF generation"
echo "   npm run assessment:test-email - Test email configuration"
echo "   npm run assessment:dev        - Run dev server + workers"
echo ""
echo "📊 Admin dashboard available at: /admin/assessment"
echo "🧠 Assessment form available at: /assessment"
