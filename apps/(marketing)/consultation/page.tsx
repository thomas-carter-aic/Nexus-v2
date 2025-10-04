import type { Metadata } from 'next';
import { Calendar, Clock, CheckCircle, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Free AI Consultation - Applied Innovations Corporation',
  description: 'Schedule a free 30-minute consultation with our AI experts to discuss your transformation goals and discover how we can help.',
};

export default function ConsultationPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Schedule Your Free AI Consultation
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Get expert guidance on your AI transformation journey. Our 30-minute consultation 
              will help you understand your opportunities and create a roadmap for success.
            </p>
          </div>
        </div>
      </section>

      {/* What You'll Get */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="mx-auto max-w-3xl">
            <h2 className="text-3xl font-bold text-center text-secondary-900 mb-12">
              What You'll Get in Your Free Consultation
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="flex items-start space-x-4">
                <CheckCircle className="w-6 h-6 text-green-500 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-secondary-900 mb-2">AI Readiness Assessment</h3>
                  <p className="text-secondary-600">Evaluate your current state and identify AI opportunities specific to your business.</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <CheckCircle className="w-6 h-6 text-green-500 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-secondary-900 mb-2">Strategic Roadmap</h3>
                  <p className="text-secondary-600">Get a high-level roadmap for your AI transformation journey with key milestones.</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <CheckCircle className="w-6 h-6 text-green-500 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-secondary-900 mb-2">ROI Estimation</h3>
                  <p className="text-secondary-600">Understand the potential return on investment for AI initiatives in your organization.</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <CheckCircle className="w-6 h-6 text-green-500 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-secondary-900 mb-2">Next Steps</h3>
                  <p className="text-secondary-600">Clear recommendations on how to move forward with your AI transformation.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Booking Form */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="mx-auto max-w-2xl">
            <div className="rounded-2xl border border-secondary-200 bg-white p-8 shadow-sm">
              <div className="text-center mb-8">
                <Calendar className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-secondary-900 mb-2">
                  Book Your Consultation
                </h2>
                <p className="text-secondary-600">
                  Fill out the form below and we'll contact you within 24 hours to schedule your consultation.
                </p>
              </div>

              <form className="space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-secondary-900 mb-2">
                      First Name *
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      required
                      className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      placeholder="John"
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-secondary-900 mb-2">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      required
                      className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      placeholder="Doe"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-secondary-900 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="john.doe@company.com"
                  />
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-secondary-900 mb-2">
                    Company Name *
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    required
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="Your Company"
                  />
                </div>

                <div>
                  <label htmlFor="role" className="block text-sm font-medium text-secondary-900 mb-2">
                    Your Role
                  </label>
                  <select
                    id="role"
                    name="role"
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                  >
                    <option value="">Select your role</option>
                    <option value="ceo">CEO/President</option>
                    <option value="cto">CTO/Technology Leader</option>
                    <option value="cio">CIO/IT Director</option>
                    <option value="manager">Manager/Director</option>
                    <option value="consultant">Consultant</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="companySize" className="block text-sm font-medium text-secondary-900 mb-2">
                    Company Size
                  </label>
                  <select
                    id="companySize"
                    name="companySize"
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                  >
                    <option value="">Select company size</option>
                    <option value="startup">Startup (1-10 employees)</option>
                    <option value="small">Small Business (11-50 employees)</option>
                    <option value="medium">Medium Business (51-200 employees)</option>
                    <option value="large">Large Business (201-1000 employees)</option>
                    <option value="enterprise">Enterprise (1000+ employees)</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="goals" className="block text-sm font-medium text-secondary-900 mb-2">
                    AI Goals & Challenges *
                  </label>
                  <textarea
                    id="goals"
                    name="goals"
                    rows={4}
                    required
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="Tell us about your AI goals, current challenges, and what you hope to achieve..."
                  />
                </div>

                <button
                  type="submit"
                  className="btn-primary w-full text-lg py-4"
                >
                  <Calendar className="w-5 h-5 mr-2" />
                  Schedule My Free Consultation
                  <ArrowRight className="w-5 h-5 ml-2" />
                </button>
              </form>

              <div className="mt-6 flex items-center justify-center space-x-6 text-sm text-secondary-500">
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-2" />
                  30 minutes
                </div>
                <div>•</div>
                <div>No obligation</div>
                <div>•</div>
                <div>Expert guidance</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
