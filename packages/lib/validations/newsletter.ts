import { z } from 'zod'

export const newsletterSubscriptionSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address')
    .max(255, 'Email is too long'),
  source: z.string().optional(),
  consent: z
    .boolean()
    .refine(val => val === true, {
      message: 'You must agree to receive marketing communications'
    })
})

export type NewsletterSubscriptionInput = z.infer<typeof newsletterSubscriptionSchema>

// Server-side validation (without consent checkbox)
export const serverNewsletterSchema = z.object({
  email: z.string().email().max(255),
  source: z.string().optional(),
  ipAddress: z.string().optional(),
  userAgent: z.string().optional()
})

export type ServerNewsletterInput = z.infer<typeof serverNewsletterSchema>
