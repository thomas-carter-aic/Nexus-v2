import { NextRequest, NextResponse } from 'next/server'
import { headers } from 'next/headers'
import { prisma } from '@/lib/db'
import { serverNewsletterSchema } from '@/lib/validations/newsletter'
import { addNewsletterSyncJob } from '@/lib/queue/newsletter-queue'

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
    const validatedData = serverNewsletterSchema.parse({
      ...body,
      ipAddress,
      userAgent
    })

    // Check if email already exists
    const existingSubscription = await prisma.newsletterSubscription.findUnique({
      where: { email: validatedData.email }
    })

    if (existingSubscription) {
      // If already confirmed, return success without doing anything
      if (existingSubscription.status === 'CONFIRMED') {
        return NextResponse.json({ 
          success: true, 
          message: 'You are already subscribed to our newsletter!' 
        })
      }
      
      // If pending or failed, retry the sync
      if (existingSubscription.status === 'PENDING' || existingSubscription.status === 'FAILED') {
        await addNewsletterSyncJob({
          subscriptionId: existingSubscription.id,
          email: validatedData.email,
          source: validatedData.source
        })
        
        return NextResponse.json({ 
          success: true, 
          message: 'Thank you! We are processing your subscription.' 
        })
      }
    }

    // Create new subscription
    const subscription = await prisma.newsletterSubscription.create({
      data: {
        email: validatedData.email,
        source: validatedData.source,
        ipAddress: validatedData.ipAddress,
        userAgent: validatedData.userAgent,
        status: 'PENDING'
      }
    })

    // Add to sync queue
    await addNewsletterSyncJob({
      subscriptionId: subscription.id,
      email: subscription.email,
      source: subscription.source || undefined
    })

    return NextResponse.json({ 
      success: true, 
      message: 'Thank you for subscribing! You will receive a confirmation shortly.' 
    })

  } catch (error) {
    console.error('Newsletter subscription error:', error)
    
    // Handle validation errors
    if (error instanceof Error && error.name === 'ZodError') {
      return NextResponse.json(
        { success: false, error: 'Invalid email address provided' },
        { status: 400 }
      )
    }

    // Handle database errors
    if (error instanceof Error && error.message.includes('Unique constraint')) {
      return NextResponse.json(
        { success: false, error: 'This email is already subscribed' },
        { status: 409 }
      )
    }

    return NextResponse.json(
      { success: false, error: 'Something went wrong. Please try again later.' },
      { status: 500 }
    )
  }
}

// GET endpoint for subscription status (optional)
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const email = searchParams.get('email')

  if (!email) {
    return NextResponse.json(
      { error: 'Email parameter is required' },
      { status: 400 }
    )
  }

  try {
    const subscription = await prisma.newsletterSubscription.findUnique({
      where: { email },
      select: {
        status: true,
        createdAt: true,
        crmSynced: true
      }
    })

    if (!subscription) {
      return NextResponse.json(
        { subscribed: false },
        { status: 404 }
      )
    }

    return NextResponse.json({
      subscribed: true,
      status: subscription.status,
      subscribedAt: subscription.createdAt,
      synced: subscription.crmSynced
    })

  } catch (error) {
    console.error('Newsletter status check error:', error)
    return NextResponse.json(
      { error: 'Failed to check subscription status' },
      { status: 500 }
    )
  }
}
