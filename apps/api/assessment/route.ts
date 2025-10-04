import { NextRequest, NextResponse } from 'next/server'
import { headers } from 'next/headers'
import { prisma } from '@/lib/db'
import { serverAssessmentSchema } from '@/lib/validations/assessment'
import { processAssessmentSubmission } from '@/lib/queue/assessment-queue'
import { emailService } from '@/lib/services/email-service'

export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json()
    
    // Get client info
    const headersList = headers()
    const ipAddress = headersList.get('x-forwarded-for') || 
                     headersList.get('x-real-ip') || 
                     request.ip || 
                     'unknown'
    const userAgent = headersList.get('user-agent') || 'unknown'

    // Validate input
    const validatedData = serverAssessmentSchema.parse({
      ...body,
      ipAddress,
      userAgent
    })

    // Check for recent submissions from same email (rate limiting)
    const recentSubmission = await prisma.assessmentSubmission.findFirst({
      where: {
        email: validatedData.email,
        createdAt: {
          gte: new Date(Date.now() - 24 * 60 * 60 * 1000) // Last 24 hours
        }
      }
    })

    if (recentSubmission) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'You have already submitted an assessment in the last 24 hours. Please check your email for the report or contact support.' 
        },
        { status: 429 }
      )
    }

    // Process responses and calculate initial scores
    const processedResponses = validatedData.responses.map(category => ({
      category: category.category,
      responses: category.responses.map(response => ({
        questionId: response.questionId,
        answer: response.answer,
        score: response.score || 0
      }))
    }))

    // Create assessment submission
    const assessment = await prisma.assessmentSubmission.create({
      data: {
        email: validatedData.email,
        companyName: validatedData.companyName,
        contactName: validatedData.contactName,
        phone: validatedData.phone,
        responses: processedResponses as any,
        overallScore: 0, // Will be calculated by worker
        categoryScores: {}, // Will be calculated by worker
        ipAddress: validatedData.ipAddress,
        userAgent: validatedData.userAgent,
        source: validatedData.source,
        status: 'SUBMITTED'
      }
    })

    // Send immediate confirmation email
    try {
      await emailService.sendAssessmentConfirmation(
        assessment.email,
        assessment.contactName || 'Valued Client',
        assessment.companyName || 'Your Organization'
      )
    } catch (emailError) {
      console.error('Failed to send confirmation email:', emailError)
      // Don't fail the entire request if email fails
    }

    // Queue assessment processing
    await processAssessmentSubmission(assessment.id)

    return NextResponse.json({ 
      success: true, 
      message: 'Assessment submitted successfully! Your personalized AI readiness report will be delivered to your email within 5-10 minutes.',
      assessmentId: assessment.id
    })

  } catch (error) {
    console.error('Assessment submission error:', error)
    
    // Handle validation errors
    if (error instanceof Error && error.name === 'ZodError') {
      return NextResponse.json(
        { success: false, error: 'Please check your responses and try again.' },
        { status: 400 }
      )
    }

    // Handle database errors
    if (error instanceof Error && error.message.includes('Unique constraint')) {
      return NextResponse.json(
        { success: false, error: 'An assessment with this email already exists.' },
        { status: 409 }
      )
    }

    return NextResponse.json(
      { success: false, error: 'Something went wrong. Please try again later.' },
      { status: 500 }
    )
  }
}

// GET endpoint for assessment status
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const assessmentId = searchParams.get('id')
  const email = searchParams.get('email')

  if (!assessmentId && !email) {
    return NextResponse.json(
      { error: 'Assessment ID or email parameter is required' },
      { status: 400 }
    )
  }

  try {
    const whereClause = assessmentId 
      ? { id: assessmentId }
      : { email: email! }

    const assessment = await prisma.assessmentSubmission.findFirst({
      where: whereClause,
      select: {
        id: true,
        status: true,
        overallScore: true,
        reportGenerated: true,
        reportSentAt: true,
        createdAt: true,
        processingError: true
      },
      orderBy: { createdAt: 'desc' }
    })

    if (!assessment) {
      return NextResponse.json(
        { found: false },
        { status: 404 }
      )
    }

    return NextResponse.json({
      found: true,
      status: assessment.status,
      overallScore: assessment.overallScore,
      reportGenerated: assessment.reportGenerated,
      reportSent: !!assessment.reportSentAt,
      submittedAt: assessment.createdAt,
      error: assessment.processingError
    })

  } catch (error) {
    console.error('Assessment status check error:', error)
    return NextResponse.json(
      { error: 'Failed to check assessment status' },
      { status: 500 }
    )
  }
}
