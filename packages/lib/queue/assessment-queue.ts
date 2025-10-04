import { Queue, Worker, Job } from 'bullmq'
import { prisma } from '../db'
import { pdfGenerator } from '../services/pdf-generator'
import { emailService } from '../services/email-service'
import { promises as fs } from 'fs'
import path from 'path'
import { assessmentQuestions, calculateCategoryScore, calculateOverallScore } from '../assessment/questions'

// Redis connection
const redisConnection = {
  host: process.env.REDIS_URL?.split('://')[1]?.split(':')[0] || 'localhost',
  port: parseInt(process.env.REDIS_URL?.split(':')[2] || '6379'),
}

// Job data interfaces
export interface AssessmentProcessingJobData {
  assessmentId: string
}

export interface ReportGenerationJobData {
  assessmentId: string
  format: 'pdf' | 'html'
}

export interface EmailDeliveryJobData {
  assessmentId: string
  reportPath: string
}

// Create queues
export const assessmentQueue = new Queue('assessment-processing', {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 50,
    removeOnFail: 25,
  },
})

export const reportQueue = new Queue('report-generation', {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 2,
    backoff: {
      type: 'exponential',
      delay: 5000,
    },
    removeOnComplete: 25,
    removeOnFail: 10,
  },
})

export const emailQueue = new Queue('email-delivery', {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 3000,
    },
    removeOnComplete: 100,
    removeOnFail: 50,
  },
})

// Add jobs to queues
export async function processAssessmentSubmission(assessmentId: string): Promise<void> {
  // Step 1: Process assessment and calculate scores
  await assessmentQueue.add('calculate-scores', { assessmentId }, {
    priority: 10
  })
  
  // Step 2: Generate PDF report (depends on step 1)
  await reportQueue.add('generate-pdf', { assessmentId, format: 'pdf' }, {
    delay: 2000, // Wait for score calculation
    priority: 5
  })
  
  // Step 3: Send email with report (depends on step 2)
  await emailQueue.add('send-report', { assessmentId }, {
    delay: 10000, // Wait for PDF generation
    priority: 1
  })
}

// Assessment processing worker
export const assessmentWorker = new Worker(
  'assessment-processing',
  async (job: Job<AssessmentProcessingJobData>) => {
    const { assessmentId } = job.data
    
    try {
      console.log(`Processing assessment ${assessmentId}`)
      
      // Get assessment data
      const assessment = await prisma.assessmentSubmission.findUnique({
        where: { id: assessmentId }
      })
      
      if (!assessment) {
        throw new Error(`Assessment ${assessmentId} not found`)
      }
      
      // Calculate category scores
      const responses = assessment.responses as any[]
      const categoryScores: Record<string, number> = {}
      
      // Get unique categories from responses
      const categories = [...new Set(responses.map((r: any) => r.category))]
      
      categories.forEach(category => {
        const categoryResponses = responses.filter((r: any) => r.category === category)
        categoryScores[category] = calculateCategoryScore(categoryResponses, category)
      })
      
      // Calculate overall score
      const overallScore = calculateOverallScore(categoryScores)
      
      // Generate recommendations
      const recommendations = generateRecommendations(categoryScores, overallScore)
      
      // Generate benchmarks
      const benchmarks = generateBenchmarks(overallScore)
      
      // Update assessment with calculated scores
      await prisma.assessmentSubmission.update({
        where: { id: assessmentId },
        data: {
          overallScore,
          categoryScores: categoryScores as any,
          status: 'PROCESSING'
        }
      })
      
      console.log(`Assessment ${assessmentId} processed successfully. Overall score: ${overallScore}`)
      
    } catch (error) {
      console.error(`Failed to process assessment ${assessmentId}:`, error)
      
      // Update assessment status
      await prisma.assessmentSubmission.update({
        where: { id: assessmentId },
        data: {
          status: 'FAILED',
          processingError: error instanceof Error ? error.message : 'Unknown error'
        }
      })
      
      throw error
    }
  },
  {
    connection: redisConnection,
    concurrency: 3,
  }
)

// Report generation worker
export const reportWorker = new Worker(
  'report-generation',
  async (job: Job<ReportGenerationJobData>) => {
    const { assessmentId, format } = job.data
    
    try {
      console.log(`Generating ${format} report for assessment ${assessmentId}`)
      
      // Get assessment data with calculated scores
      const assessment = await prisma.assessmentSubmission.findUnique({
        where: { id: assessmentId }
      })
      
      if (!assessment) {
        throw new Error(`Assessment ${assessmentId} not found`)
      }
      
      if (!assessment.overallScore) {
        throw new Error(`Assessment ${assessmentId} scores not calculated yet`)
      }
      
      // Prepare report data
      const reportData = {
        id: assessment.id,
        companyName: assessment.companyName || 'Your Organization',
        contactName: assessment.contactName || 'Valued Client',
        email: assessment.email,
        overallScore: assessment.overallScore,
        categoryScores: assessment.categoryScores as Record<string, number>,
        responses: assessment.responses as any[],
        createdAt: assessment.createdAt,
        recommendations: generateRecommendations(
          assessment.categoryScores as Record<string, number>,
          assessment.overallScore
        ),
        benchmarks: generateBenchmarks(assessment.overallScore)
      }
      
      // Generate PDF
      const pdfBuffer = await pdfGenerator.generateAssessmentReport(reportData)
      
      // Save PDF to storage
      const storageDir = process.env.STORAGE_PATH || './storage/assessments'
      await fs.mkdir(storageDir, { recursive: true })
      
      const filename = `assessment-report-${assessmentId}-${Date.now()}.pdf`
      const filePath = path.join(storageDir, filename)
      
      await fs.writeFile(filePath, pdfBuffer)
      
      // Update assessment with report path
      await prisma.assessmentSubmission.update({
        where: { id: assessmentId },
        data: {
          reportGenerated: true,
          reportPath: filePath,
          reportUrl: `/api/reports/${filename}` // API endpoint to serve the file
        }
      })
      
      console.log(`Report generated successfully for assessment ${assessmentId}: ${filePath}`)
      
    } catch (error) {
      console.error(`Failed to generate report for assessment ${assessmentId}:`, error)
      
      await prisma.assessmentSubmission.update({
        where: { id: assessmentId },
        data: {
          status: 'FAILED',
          processingError: error instanceof Error ? error.message : 'Report generation failed'
        }
      })
      
      throw error
    }
  },
  {
    connection: redisConnection,
    concurrency: 2, // Limit concurrency for resource-intensive PDF generation
  }
)

// Email delivery worker
export const emailWorker = new Worker(
  'email-delivery',
  async (job: Job<AssessmentProcessingJobData>) => {
    const { assessmentId } = job.data
    
    try {
      console.log(`Sending report email for assessment ${assessmentId}`)
      
      // Get assessment data
      const assessment = await prisma.assessmentSubmission.findUnique({
        where: { id: assessmentId }
      })
      
      if (!assessment) {
        throw new Error(`Assessment ${assessmentId} not found`)
      }
      
      if (!assessment.reportPath) {
        throw new Error(`Report not generated for assessment ${assessmentId}`)
      }
      
      // Read PDF file
      const pdfBuffer = await fs.readFile(assessment.reportPath)
      
      // Prepare email data
      const emailData = {
        recipientEmail: assessment.email,
        recipientName: assessment.contactName || 'Valued Client',
        companyName: assessment.companyName || 'Your Organization',
        overallScore: assessment.overallScore,
        reportPath: assessment.reportPath,
        assessmentId: assessment.id
      }
      
      // Send email with PDF attachment
      await emailService.sendAssessmentReport(emailData, pdfBuffer)
      
      // Update assessment status
      await prisma.assessmentSubmission.update({
        where: { id: assessmentId },
        data: {
          status: 'COMPLETED',
          reportSentAt: new Date()
        }
      })
      
      // Schedule follow-up emails
      await scheduleFollowUpEmails(assessmentId)
      
      console.log(`Report email sent successfully for assessment ${assessmentId}`)
      
    } catch (error) {
      console.error(`Failed to send report email for assessment ${assessmentId}:`, error)
      
      await prisma.assessmentSubmission.update({
        where: { id: assessmentId },
        data: {
          status: 'FAILED',
          processingError: error instanceof Error ? error.message : 'Email delivery failed'
        }
      })
      
      throw error
    }
  },
  {
    connection: redisConnection,
    concurrency: 5,
  }
)

// Helper functions
function generateRecommendations(categoryScores: Record<string, number>, overallScore: number) {
  const recommendations = []
  
  // Sort categories by score (lowest first for prioritization)
  const sortedCategories = Object.entries(categoryScores).sort(([,a], [,b]) => a - b)
  
  for (const [category, score] of sortedCategories) {
    const level = getScoreLevel(score)
    const priority = score < 50 ? 'high' : score < 70 ? 'medium' : 'low'
    
    recommendations.push({
      category,
      score,
      level,
      priority,
      recommendations: getCategoryRecommendations(category, level),
      nextSteps: getCategoryNextSteps(category, level)
    })
  }
  
  return recommendations
}

function generateBenchmarks(overallScore: number) {
  // These would typically come from a database of industry benchmarks
  const industryAverage = 62
  const topPerformers = 85
  
  let yourPosition: 'top-quartile' | 'above-average' | 'average' | 'below-average'
  
  if (overallScore >= topPerformers) {
    yourPosition = 'top-quartile'
  } else if (overallScore >= industryAverage + 10) {
    yourPosition = 'above-average'
  } else if (overallScore >= industryAverage - 10) {
    yourPosition = 'average'
  } else {
    yourPosition = 'below-average'
  }
  
  return {
    industryAverage,
    topPerformers,
    yourPosition
  }
}

function getScoreLevel(score: number): 'excellent' | 'good' | 'fair' | 'poor' {
  if (score >= 85) return 'excellent'
  if (score >= 70) return 'good'
  if (score >= 50) return 'fair'
  return 'poor'
}

function getCategoryRecommendations(category: string, level: string): string[] {
  const recommendations: Record<string, Record<string, string[]>> = {
    strategy: {
      poor: [
        'Develop a formal AI strategy document with clear objectives and success metrics',
        'Conduct stakeholder workshops to align on AI vision and priorities',
        'Establish an AI steering committee with executive sponsorship'
      ],
      fair: [
        'Refine your AI strategy with specific use cases and ROI projections',
        'Create a detailed AI roadmap with timeline and resource requirements',
        'Develop change management plans for AI adoption'
      ],
      good: [
        'Optimize your AI strategy based on initial pilot results',
        'Expand successful AI use cases to additional business areas',
        'Establish AI centers of excellence for knowledge sharing'
      ],
      excellent: [
        'Lead industry AI innovation initiatives',
        'Develop AI-powered competitive advantages',
        'Share AI best practices through thought leadership'
      ]
    },
    data: {
      poor: [
        'Conduct a comprehensive data audit to assess quality and accessibility',
        'Implement basic data governance policies and procedures',
        'Establish data quality monitoring and improvement processes'
      ],
      fair: [
        'Enhance data integration capabilities across systems',
        'Implement advanced data governance frameworks',
        'Develop self-service analytics capabilities for business users'
      ],
      good: [
        'Implement real-time data processing and analytics capabilities',
        'Establish data lakes and advanced analytics platforms',
        'Develop predictive analytics and machine learning models'
      ],
      excellent: [
        'Implement advanced AI/ML data pipelines',
        'Establish real-time decision-making capabilities',
        'Lead data-driven innovation initiatives'
      ]
    }
    // Add more categories as needed
  }
  
  return recommendations[category]?.[level] || [
    'Assess current capabilities and identify improvement opportunities',
    'Develop targeted improvement plans with clear timelines',
    'Implement best practices and monitor progress regularly'
  ]
}

function getCategoryNextSteps(category: string, level: string): string[] {
  const nextSteps: Record<string, Record<string, string[]>> = {
    strategy: {
      poor: [
        'Schedule AI strategy workshop with key stakeholders',
        'Research AI use cases relevant to your industry',
        'Identify executive sponsor for AI initiatives'
      ],
      fair: [
        'Prioritize AI use cases based on business impact and feasibility',
        'Develop detailed business cases for top AI opportunities',
        'Create AI governance framework and decision-making processes'
      ],
      good: [
        'Launch pilot AI projects in high-impact areas',
        'Establish success metrics and monitoring processes',
        'Plan for scaling successful AI initiatives'
      ],
      excellent: [
        'Expand AI capabilities to new business areas',
        'Develop AI-powered products and services',
        'Establish AI innovation partnerships'
      ]
    }
    // Add more categories as needed
  }
  
  return nextSteps[category]?.[level] || [
    'Conduct detailed assessment of current state',
    'Develop improvement roadmap with priorities',
    'Begin implementation of highest-impact initiatives'
  ]
}

async function scheduleFollowUpEmails(assessmentId: string): Promise<void> {
  const assessment = await prisma.assessmentSubmission.findUnique({
    where: { id: assessmentId }
  })
  
  if (!assessment) return
  
  // Schedule follow-up emails
  const followUps = [
    {
      type: 'consultation-offer' as const,
      scheduledFor: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000) // 2 days
    },
    {
      type: 'implementation-guide' as const,
      scheduledFor: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 1 week
    },
    {
      type: 'survey-feedback' as const,
      scheduledFor: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000) // 2 weeks
    }
  ]
  
  for (const followUp of followUps) {
    await prisma.assessmentFollowUp.create({
      data: {
        assessmentId: assessment.id,
        type: followUp.type,
        scheduledFor: followUp.scheduledFor
      }
    })
    
    // Schedule email job
    await emailQueue.add(
      'send-followup',
      {
        assessmentId: assessment.id,
        followUpType: followUp.type
      },
      {
        delay: followUp.scheduledFor.getTime() - Date.now()
      }
    )
  }
}

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('Shutting down assessment workers...')
  await Promise.all([
    assessmentWorker.close(),
    reportWorker.close(),
    emailWorker.close(),
    assessmentQueue.close(),
    reportQueue.close(),
    emailQueue.close()
  ])
  await pdfGenerator.close()
  process.exit(0)
})
