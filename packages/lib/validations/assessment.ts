import { z } from 'zod'

// Individual question response schema
export const questionResponseSchema = z.object({
  questionId: z.string(),
  answer: z.union([
    z.string(),
    z.number(),
    z.array(z.string()),
    z.boolean()
  ]),
  score: z.number().min(0).max(100).optional()
})

// Assessment categories
export const assessmentCategorySchema = z.object({
  category: z.enum([
    'strategy',
    'data',
    'technology',
    'talent',
    'governance',
    'culture',
    'processes',
    'infrastructure'
  ]),
  responses: z.array(questionResponseSchema),
  categoryScore: z.number().min(0).max(100).optional()
})

// Main assessment submission schema
export const assessmentSubmissionSchema = z.object({
  // Contact information
  email: z.string().email('Please enter a valid email address'),
  companyName: z.string().min(1, 'Company name is required').max(100),
  contactName: z.string().min(1, 'Contact name is required').max(100),
  phone: z.string().optional(),
  
  // Assessment responses
  responses: z.array(assessmentCategorySchema),
  
  // Metadata
  source: z.string().optional(),
  
  // Consent and agreements
  consent: z.boolean().refine(val => val === true, {
    message: 'You must agree to receive the assessment report'
  }),
  marketingConsent: z.boolean().optional()
})

export type AssessmentSubmissionInput = z.infer<typeof assessmentSubmissionSchema>
export type QuestionResponse = z.infer<typeof questionResponseSchema>
export type AssessmentCategory = z.infer<typeof assessmentCategorySchema>

// Server-side validation (without consent)
export const serverAssessmentSchema = assessmentSubmissionSchema.omit({ 
  consent: true,
  marketingConsent: true 
}).extend({
  ipAddress: z.string().optional(),
  userAgent: z.string().optional()
})

export type ServerAssessmentInput = z.infer<typeof serverAssessmentSchema>

// Assessment question structure
export const assessmentQuestionSchema = z.object({
  id: z.string(),
  category: z.string(),
  question: z.string(),
  type: z.enum(['multiple-choice', 'scale', 'boolean', 'text']),
  options: z.array(z.object({
    value: z.string(),
    label: z.string(),
    score: z.number()
  })).optional(),
  required: z.boolean().default(true),
  weight: z.number().default(1),
  description: z.string().optional()
})

export type AssessmentQuestion = z.infer<typeof assessmentQuestionSchema>

// Report generation request
export const reportGenerationSchema = z.object({
  assessmentId: z.string(),
  format: z.enum(['pdf', 'html']).default('pdf'),
  includeRecommendations: z.boolean().default(true),
  includeBenchmarks: z.boolean().default(true)
})

export type ReportGenerationRequest = z.infer<typeof reportGenerationSchema>
