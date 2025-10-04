import { Queue, Worker, Job } from 'bullmq'
import Redis from 'redis'
import { prisma } from '../db'
import { suiteCRM } from '../services/suitecrm'

// Redis connection
const redisConnection = {
  host: process.env.REDIS_URL?.split('://')[1]?.split(':')[0] || 'localhost',
  port: parseInt(process.env.REDIS_URL?.split(':')[2] || '6379'),
}

// Job data interface
export interface NewsletterSyncJobData {
  subscriptionId: string
  email: string
  source?: string
}

// Create the queue
export const newsletterQueue = new Queue('newsletter-sync', {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 100,
    removeOnFail: 50,
  },
})

// Add job to queue
export async function addNewsletterSyncJob(data: NewsletterSyncJobData): Promise<string> {
  const job = await newsletterQueue.add('sync-to-crm', data, {
    delay: 1000, // 1 second delay to allow for immediate database operations
  })
  
  // Store job reference in database
  await prisma.syncJob.create({
    data: {
      subscriptionId: data.subscriptionId,
      jobId: job.id!,
      status: 'PENDING',
    },
  })
  
  return job.id!
}

// Worker to process jobs
export const newsletterWorker = new Worker(
  'newsletter-sync',
  async (job: Job<NewsletterSyncJobData>) => {
    const { subscriptionId, email, source } = job.data
    
    try {
      // Update job status
      await prisma.syncJob.update({
        where: { jobId: job.id! },
        data: { 
          status: 'PROCESSING',
          attempts: job.attemptsMade + 1
        },
      })

      // Check if contact already exists in SuiteCRM
      let crmContact = await suiteCRM.findContactByEmail(email)
      let crmId: string

      if (crmContact) {
        // Update existing contact
        await suiteCRM.updateContact(crmContact.id!, {
          lead_source: source || 'Website Newsletter',
          description: `Newsletter subscription updated from AIC website (${new Date().toISOString()})`
        })
        crmId = crmContact.id!
      } else {
        // Create new contact
        crmId = await suiteCRM.createContact({
          email1: email,
          lead_source: source || 'Website Newsletter',
          description: `Newsletter subscription from AIC website (${new Date().toISOString()})`
        })
      }

      // Update subscription record
      await prisma.newsletterSubscription.update({
        where: { id: subscriptionId },
        data: {
          crmId,
          crmSynced: true,
          status: 'CONFIRMED',
          lastSyncAt: new Date(),
          syncAttempts: { increment: 1 },
          syncError: null,
        },
      })

      // Update job status
      await prisma.syncJob.update({
        where: { jobId: job.id! },
        data: { 
          status: 'COMPLETED',
          completedAt: new Date()
        },
      })

      console.log(`Successfully synced subscription ${subscriptionId} to SuiteCRM`)
      
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      
      // Update subscription with error
      await prisma.newsletterSubscription.update({
        where: { id: subscriptionId },
        data: {
          syncAttempts: { increment: 1 },
          syncError: errorMessage,
          status: job.attemptsMade >= 2 ? 'FAILED' : 'PENDING', // Mark as failed after final attempt
        },
      })

      // Update job status
      await prisma.syncJob.update({
        where: { jobId: job.id! },
        data: { 
          status: job.attemptsMade >= 2 ? 'FAILED' : 'RETRYING',
          error: errorMessage
        },
      })

      console.error(`Failed to sync subscription ${subscriptionId}:`, error)
      throw error // Re-throw to trigger retry
    }
  },
  {
    connection: redisConnection,
    concurrency: 5, // Process up to 5 jobs concurrently
  }
)

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('Shutting down newsletter worker...')
  await newsletterWorker.close()
  await newsletterQueue.close()
  process.exit(0)
})
