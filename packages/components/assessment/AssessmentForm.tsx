'use client'

import { useState } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { assessmentSubmissionSchema, type AssessmentSubmissionInput } from '@/lib/validations/assessment'
import { assessmentQuestions } from '@/lib/assessment/questions'
import { ChevronLeft, ChevronRight, CheckCircle, AlertCircle, Loader2, FileText, Mail, Building, User, Phone } from 'lucide-react'

interface AssessmentFormProps {
  source?: string
  className?: string
}

export default function AssessmentForm({ 
  source = 'assessment-page',
  className = ''
}: AssessmentFormProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors },
    setValue,
    getValues
  } = useForm<AssessmentSubmissionInput>({
    resolver: zodResolver(assessmentSubmissionSchema),
    defaultValues: {
      email: '',
      companyName: '',
      contactName: '',
      phone: '',
      responses: [],
      source,
      consent: false,
      marketingConsent: false
    }
  })

  // Group questions by category
  const questionsByCategory = assessmentQuestions.reduce((acc, question) => {
    if (!acc[question.category]) {
      acc[question.category] = []
    }
    acc[question.category].push(question)
    return acc
  }, {} as Record<string, typeof assessmentQuestions>)

  const categories = Object.keys(questionsByCategory)
  const totalSteps = categories.length + 2 // Categories + Contact Info + Review
  const isContactStep = currentStep === 0
  const isReviewStep = currentStep === totalSteps - 1
  const currentCategory = categories[currentStep - 1]

  const onSubmit = async (data: AssessmentSubmissionInput) => {
    setIsSubmitting(true)
    setSubmitStatus('idle')
    setMessage('')

    try {
      const response = await fetch('/api/assessment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      const result = await response.json()

      if (result.success) {
        setSubmitStatus('success')
        setMessage(result.message || 'Assessment submitted successfully!')
      } else {
        setSubmitStatus('error')
        setMessage(result.error || 'Something went wrong. Please try again.')
      }
    } catch (error) {
      setSubmitStatus('error')
      setMessage('Network error. Please check your connection and try again.')
      console.error('Assessment submission error:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleQuestionResponse = (questionId: string, answer: any, score: number) => {
    const currentResponses = getValues('responses') || []
    const categoryIndex = currentResponses.findIndex(r => r.category === currentCategory)
    
    if (categoryIndex >= 0) {
      const categoryResponses = [...currentResponses[categoryIndex].responses]
      const questionIndex = categoryResponses.findIndex(r => r.questionId === questionId)
      
      if (questionIndex >= 0) {
        categoryResponses[questionIndex] = { questionId, answer, score }
      } else {
        categoryResponses.push({ questionId, answer, score })
      }
      
      currentResponses[categoryIndex].responses = categoryResponses
    } else {
      currentResponses.push({
        category: currentCategory,
        responses: [{ questionId, answer, score }]
      })
    }
    
    setValue('responses', currentResponses)
  }

  const getQuestionResponse = (questionId: string) => {
    const responses = getValues('responses') || []
    const categoryResponse = responses.find(r => r.category === currentCategory)
    return categoryResponse?.responses.find(r => r.questionId === questionId)
  }

  const isStepComplete = (step: number): boolean => {
    if (step === 0) {
      // Contact info step
      const values = getValues()
      return !!(values.email && values.companyName && values.contactName)
    } else if (step <= categories.length) {
      // Category steps
      const category = categories[step - 1]
      const categoryQuestions = questionsByCategory[category]
      const responses = getValues('responses') || []
      const categoryResponse = responses.find(r => r.category === category)
      
      return categoryQuestions.every(q => 
        categoryResponse?.responses.some(r => r.questionId === q.id)
      )
    }
    return true
  }

  if (submitStatus === 'success') {
    return (
      <div className={`max-w-2xl mx-auto p-8 ${className}`}>
        <div className="text-center">
          <div className="mb-6">
            <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Assessment Submitted Successfully!</h2>
            <p className="text-gray-600">{message}</p>
          </div>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <Mail className="h-8 w-8 text-blue-600 mx-auto mb-3" />
            <h3 className="font-semibold text-blue-900 mb-2">What happens next?</h3>
            <ul className="text-sm text-blue-800 space-y-2">
              <li>✅ Your responses are being analyzed by our AI system</li>
              <li>📊 A comprehensive report is being generated</li>
              <li>📧 You'll receive your personalized AI Readiness Report via email</li>
              <li>🕐 Expected delivery: 5-10 minutes</li>
            </ul>
          </div>
          
          <div className="space-y-4">
            <a 
              href="/services/ai-strategy" 
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Explore Our AI Services
            </a>
            <p className="text-sm text-gray-500">
              Questions? Contact us at <a href="mailto:support@appliedinnovations.com" className="text-blue-600">support@appliedinnovations.com</a>
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`max-w-4xl mx-auto ${className}`}>
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">AI Readiness Assessment</h2>
          <span className="text-sm text-gray-500">
            Step {currentStep + 1} of {totalSteps}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
          />
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* Contact Information Step */}
        {isContactStep && (
          <div className="bg-white p-8 rounded-lg border border-gray-200">
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Contact Information</h3>
              <p className="text-gray-600">We'll use this information to personalize your report and send it to you.</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Mail className="inline h-4 w-4 mr-1" />
                  Email Address *
                </label>
                <input
                  {...register('email')}
                  type="email"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="your.email@company.com"
                />
                {errors.email && (
                  <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <User className="inline h-4 w-4 mr-1" />
                  Your Name *
                </label>
                <input
                  {...register('contactName')}
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="John Smith"
                />
                {errors.contactName && (
                  <p className="mt-1 text-sm text-red-600">{errors.contactName.message}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Building className="inline h-4 w-4 mr-1" />
                  Company Name *
                </label>
                <input
                  {...register('companyName')}
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Your Company Inc."
                />
                {errors.companyName && (
                  <p className="mt-1 text-sm text-red-600">{errors.companyName.message}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Phone className="inline h-4 w-4 mr-1" />
                  Phone Number (Optional)
                </label>
                <input
                  {...register('phone')}
                  type="tel"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
            </div>
          </div>
        )}

        {/* Category Questions */}
        {!isContactStep && !isReviewStep && (
          <div className="bg-white p-8 rounded-lg border border-gray-200">
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2 capitalize">
                {currentCategory.replace(/([A-Z])/g, ' $1').trim()} Assessment
              </h3>
              <p className="text-gray-600">
                Please answer the following questions about your organization's {currentCategory} capabilities.
              </p>
            </div>
            
            <div className="space-y-8">
              {questionsByCategory[currentCategory]?.map((question, index) => (
                <div key={question.id} className="border-b border-gray-100 pb-6 last:border-b-0">
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-900 mb-2">
                      {index + 1}. {question.question}
                    </h4>
                    {question.description && (
                      <p className="text-sm text-gray-600">{question.description}</p>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    {question.options?.map((option) => (
                      <label key={option.value} className="flex items-start space-x-3 cursor-pointer">
                        <input
                          type={question.type === 'multiple-choice' ? 'radio' : 'checkbox'}
                          name={question.id}
                          value={option.value}
                          checked={getQuestionResponse(question.id)?.answer === option.value}
                          onChange={() => handleQuestionResponse(question.id, option.value, option.score)}
                          className="mt-1 h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                        />
                        <span className="text-gray-700">{option.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Review Step */}
        {isReviewStep && (
          <div className="bg-white p-8 rounded-lg border border-gray-200">
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Review & Submit</h3>
              <p className="text-gray-600">Please review your information and submit your assessment.</p>
            </div>
            
            <div className="space-y-6">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">Contact Information</h4>
                <div className="text-sm text-gray-600 space-y-1">
                  <p><strong>Name:</strong> {watch('contactName')}</p>
                  <p><strong>Email:</strong> {watch('email')}</p>
                  <p><strong>Company:</strong> {watch('companyName')}</p>
                  {watch('phone') && <p><strong>Phone:</strong> {watch('phone')}</p>}
                </div>
              </div>
              
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">Assessment Summary</h4>
                <p className="text-sm text-blue-800">
                  You have completed {categories.length} assessment categories covering all aspects of AI readiness.
                  Your personalized report will include detailed scores, recommendations, and an implementation roadmap.
                </p>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Controller
                    name="consent"
                    control={control}
                    render={({ field }) => (
                      <input
                        type="checkbox"
                        checked={field.value}
                        onChange={field.onChange}
                        className="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                      />
                    )}
                  />
                  <label className="text-sm text-gray-700">
                    I agree to receive my AI Readiness Assessment report via email. *
                  </label>
                </div>
                {errors.consent && (
                  <p className="text-sm text-red-600">{errors.consent.message}</p>
                )}
                
                <div className="flex items-start space-x-3">
                  <Controller
                    name="marketingConsent"
                    control={control}
                    render={({ field }) => (
                      <input
                        type="checkbox"
                        checked={field.value || false}
                        onChange={field.onChange}
                        className="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                      />
                    )}
                  />
                  <label className="text-sm text-gray-700">
                    I would like to receive additional AI insights and updates from Applied Innovations Corporation. (Optional)
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error Display */}
        {submitStatus === 'error' && (
          <div className="flex items-center gap-2 p-4 bg-red-50 border border-red-200 rounded-lg">
            <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
            <p className="text-red-800">{message}</p>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between items-center pt-6 border-t border-gray-200">
          <button
            type="button"
            onClick={handlePrevious}
            disabled={currentStep === 0}
            className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="h-4 w-4" />
            Previous
          </button>
          
          <div className="flex items-center gap-2">
            {categories.map((_, index) => (
              <div
                key={index}
                className={`w-2 h-2 rounded-full ${
                  isStepComplete(index + 1) ? 'bg-green-500' : 
                  currentStep === index + 1 ? 'bg-blue-500' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>
          
          {isReviewStep ? (
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  <FileText className="h-4 w-4" />
                  Submit Assessment
                </>
              )}
            </button>
          ) : (
            <button
              type="button"
              onClick={handleNext}
              disabled={!isStepComplete(currentStep)}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Next
              <ChevronRight className="h-4 w-4" />
            </button>
          )}
        </div>
      </form>
    </div>
  )
}
