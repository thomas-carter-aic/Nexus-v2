'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { newsletterSubscriptionSchema, type NewsletterSubscriptionInput } from '@/lib/validations/newsletter'
import { Mail, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

interface NewsletterFormProps {
  source?: string
  className?: string
  placeholder?: string
  buttonText?: string
  showConsent?: boolean
}

export default function NewsletterForm({ 
  source = 'homepage',
  className = '',
  placeholder = 'Enter your email address',
  buttonText = 'Subscribe',
  showConsent = true
}: NewsletterFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<NewsletterSubscriptionInput>({
    resolver: zodResolver(newsletterSubscriptionSchema),
    defaultValues: {
      email: '',
      source,
      consent: false
    }
  })

  const onSubmit = async (data: NewsletterSubscriptionInput) => {
    setIsSubmitting(true)
    setSubmitStatus('idle')
    setMessage('')

    try {
      const response = await fetch('/api/newsletter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: data.email,
          source: data.source
        }),
      })

      const result = await response.json()

      if (result.success) {
        setSubmitStatus('success')
        setMessage(result.message || 'Thank you for subscribing!')
        reset()
      } else {
        setSubmitStatus('error')
        setMessage(result.error || 'Something went wrong. Please try again.')
      }
    } catch (error) {
      setSubmitStatus('error')
      setMessage('Network error. Please check your connection and try again.')
      console.error('Newsletter subscription error:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (submitStatus === 'success') {
    return (
      <div className={`flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg ${className}`}>
        <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
        <div>
          <p className="text-green-800 font-medium">Successfully subscribed!</p>
          <p className="text-green-700 text-sm">{message}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={className}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                {...register('email')}
                type="email"
                placeholder={placeholder}
                className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                  errors.email ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
                disabled={isSubmitting}
              />
            </div>
            {errors.email && (
              <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
            )}
          </div>
          
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2 min-w-[120px]"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Subscribing...
              </>
            ) : (
              buttonText
            )}
          </button>
        </div>

        {showConsent && (
          <div className="flex items-start gap-3">
            <input
              {...register('consent')}
              type="checkbox"
              id="newsletter-consent"
              className="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              disabled={isSubmitting}
            />
            <label htmlFor="newsletter-consent" className="text-sm text-gray-600">
              I agree to receive marketing communications from Applied Innovations Corporation. 
              You can unsubscribe at any time.
            </label>
          </div>
        )}
        
        {errors.consent && (
          <p className="text-sm text-red-600">{errors.consent.message}</p>
        )}

        {submitStatus === 'error' && (
          <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg">
            <AlertCircle className="h-4 w-4 text-red-600 flex-shrink-0" />
            <p className="text-red-800 text-sm">{message}</p>
          </div>
        )}
      </form>
    </div>
  )
}
