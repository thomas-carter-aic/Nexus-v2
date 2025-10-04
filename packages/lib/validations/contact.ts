import { z } from 'zod'

// Contact form validation schema
export const contactSubmissionSchema = z.object({
  // Required fields
  firstName: z.string().min(1, 'First name is required').max(50, 'First name is too long'),
  lastName: z.string().min(1, 'Last name is required').max(50, 'Last name is too long'),
  email: z.string().email('Please enter a valid email address').max(255, 'Email is too long'),
  message: z.string().min(10, 'Message must be at least 10 characters').max(2000, 'Message is too long'),
  
  // Optional fields
  phone: z.string().optional(),
  company: z.string().max(100, 'Company name is too long').optional(),
  jobTitle: z.string().max(100, 'Job title is too long').optional(),
  website: z.string().url('Please enter a valid website URL').optional().or(z.literal('')),
  
  // Service and project details
  service: z.enum([
    'strategy',
    'implementation', 
    'governance',
    'training',
    'innovation',
    'optimization',
    'other'
  ]).optional(),
  
  budget: z.enum([
    'under-50k',
    '50k-100k',
    '100k-250k',
    '250k-500k',
    '500k-1m',
    'over-1m',
    'not-sure'
  ]).optional(),
  
  timeline: z.enum([
    'immediate',
    '1-3-months',
    '3-6-months',
    '6-12-months',
    'over-12-months',
    'not-sure'
  ]).optional(),
  
  // Contact preferences
  preferredContact: z.enum(['email', 'phone', 'video-call']).default('email'),
  bestTimeToCall: z.string().optional(),
  
  // Lead source tracking
  source: z.string().optional(),
  referrer: z.string().optional(),
  
  // Consent and agreements
  consent: z.boolean().refine(val => val === true, {
    message: 'You must agree to be contacted about your inquiry'
  }),
  marketingConsent: z.boolean().optional(),
  
  // reCAPTCHA token
  recaptchaToken: z.string().optional()
})

export type ContactSubmissionInput = z.infer<typeof contactSubmissionSchema>

// Server-side validation (without consent and recaptcha)
export const serverContactSchema = contactSubmissionSchema.omit({ 
  consent: true,
  recaptchaToken: true 
}).extend({
  ipAddress: z.string().optional(),
  userAgent: z.string().optional(),
  sessionId: z.string().optional()
})

export type ServerContactInput = z.infer<typeof serverContactSchema>

// Contact activity validation
export const contactActivitySchema = z.object({
  contactId: z.string(),
  type: z.enum([
    'FORM_SUBMISSION',
    'EMAIL_SENT',
    'EMAIL_OPENED', 
    'EMAIL_CLICKED',
    'PHONE_CALL',
    'MEETING_SCHEDULED',
    'MEETING_COMPLETED',
    'PROPOSAL_SENT',
    'CONTRACT_SIGNED',
    'NOTE_ADDED',
    'STATUS_CHANGED',
    'CRM_SYNC'
  ]),
  description: z.string(),
  performedBy: z.string().optional(),
  metadata: z.record(z.any()).optional()
})

export type ContactActivityInput = z.infer<typeof contactActivitySchema>

// Follow-up scheduling validation
export const followUpSchema = z.object({
  contactId: z.string(),
  type: z.enum([
    'AUTO_RESPONSE',
    'QUALIFICATION_CALL',
    'PROPOSAL_FOLLOWUP',
    'CHECK_IN',
    'NURTURE_EMAIL',
    'MEETING_REMINDER',
    'CONTRACT_FOLLOWUP'
  ]),
  scheduledFor: z.date(),
  notes: z.string().optional(),
  assignedTo: z.string().optional()
})

export type FollowUpInput = z.infer<typeof followUpSchema>

// Lead scoring configuration
export const leadScoringConfig = {
  // Company size indicators
  companyKeywords: {
    'enterprise': 20,
    'corporation': 15,
    'inc': 10,
    'llc': 5,
    'startup': -5
  },
  
  // Job title scoring
  jobTitleKeywords: {
    'ceo': 25,
    'cto': 25,
    'president': 20,
    'vp': 20,
    'director': 15,
    'manager': 10,
    'analyst': 5,
    'intern': -10
  },
  
  // Service interest scoring
  serviceScoring: {
    'strategy': 20,
    'implementation': 25,
    'governance': 15,
    'training': 10,
    'innovation': 20,
    'optimization': 15,
    'other': 5
  },
  
  // Budget scoring
  budgetScoring: {
    'over-1m': 30,
    '500k-1m': 25,
    '250k-500k': 20,
    '100k-250k': 15,
    '50k-100k': 10,
    'under-50k': 5,
    'not-sure': 0
  },
  
  // Timeline urgency
  timelineScoring: {
    'immediate': 25,
    '1-3-months': 20,
    '3-6-months': 15,
    '6-12-months': 10,
    'over-12-months': 5,
    'not-sure': 0
  },
  
  // Message quality indicators
  messageKeywords: {
    'urgent': 10,
    'asap': 10,
    'immediately': 10,
    'budget': 5,
    'timeline': 5,
    'proposal': 10,
    'meeting': 5,
    'call': 5
  }
}

// Calculate lead score
export function calculateLeadScore(contact: ServerContactInput): number {
  let score = 0
  
  // Company scoring
  if (contact.company) {
    const companyLower = contact.company.toLowerCase()
    Object.entries(leadScoringConfig.companyKeywords).forEach(([keyword, points]) => {
      if (companyLower.includes(keyword)) {
        score += points
      }
    })
  }
  
  // Job title scoring
  if (contact.jobTitle) {
    const titleLower = contact.jobTitle.toLowerCase()
    Object.entries(leadScoringConfig.jobTitleKeywords).forEach(([keyword, points]) => {
      if (titleLower.includes(keyword)) {
        score += points
      }
    })
  }
  
  // Service interest scoring
  if (contact.service) {
    score += leadScoringConfig.serviceScoring[contact.service] || 0
  }
  
  // Budget scoring
  if (contact.budget) {
    score += leadScoringConfig.budgetScoring[contact.budget] || 0
  }
  
  // Timeline scoring
  if (contact.timeline) {
    score += leadScoringConfig.timelineScoring[contact.timeline] || 0
  }
  
  // Message content scoring
  if (contact.message) {
    const messageLower = contact.message.toLowerCase()
    Object.entries(leadScoringConfig.messageKeywords).forEach(([keyword, points]) => {
      if (messageLower.includes(keyword)) {
        score += points
      }
    })
    
    // Length bonus (longer messages often indicate more serious inquiries)
    if (contact.message.length > 200) score += 5
    if (contact.message.length > 500) score += 5
  }
  
  // Website presence bonus
  if (contact.website) {
    score += 5
  }
  
  // Phone number provided bonus
  if (contact.phone) {
    score += 5
  }
  
  return Math.max(0, score) // Ensure non-negative score
}

// Determine priority based on lead score
export function getPriorityFromScore(score: number): 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT' {
  if (score >= 80) return 'URGENT'
  if (score >= 60) return 'HIGH'
  if (score >= 30) return 'MEDIUM'
  return 'LOW'
}

// Email template validation
export const emailTemplateSchema = z.object({
  name: z.string().min(1, 'Template name is required'),
  type: z.enum([
    'AUTO_RESPONSE',
    'QUALIFICATION',
    'PROPOSAL',
    'FOLLOWUP',
    'NURTURE',
    'MEETING_CONFIRMATION',
    'THANK_YOU'
  ]),
  subject: z.string().min(1, 'Subject is required'),
  content: z.string().min(1, 'Content is required'),
  variables: z.record(z.string()).optional()
})

export type EmailTemplateInput = z.infer<typeof emailTemplateSchema>
