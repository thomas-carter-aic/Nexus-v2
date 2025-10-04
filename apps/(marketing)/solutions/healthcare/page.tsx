import type { Metadata } from 'next';
import { Heart, CheckCircle, Shield, TrendingUp, Users, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Healthcare AI Solutions - Applied Innovations Corporation',
  description: 'AI-powered healthcare solutions for diagnostics, patient care optimization, and operational efficiency in medical organizations.',
};

export default function HealthcareSolutionsPage() {
  return (
    <div className="bg-white">
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-red-600 rounded-2xl mb-6">
              <Heart className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Healthcare AI Solutions
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Transform healthcare delivery with AI-powered solutions for diagnostics, 
              patient care optimization, and operational efficiency while maintaining 
              the highest standards of privacy and compliance.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Improve Patient Care
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Healthcare Use Cases</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              AI applications specifically designed for healthcare environments
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'Diagnostic Assistance',
                description: 'AI-powered medical imaging and diagnostic support',
                icon: '🔬',
                benefits: ['25% improvement in diagnostic accuracy', 'Faster diagnosis times', 'Reduced human error'],
              },
              {
                title: 'Patient Monitoring',
                description: 'Real-time patient monitoring and alert systems',
                icon: '📱',
                benefits: ['Early warning systems', '24/7 monitoring', 'Predictive health analytics'],
              },
              {
                title: 'Drug Discovery',
                description: 'Accelerated pharmaceutical research and development',
                icon: '💊',
                benefits: ['Faster drug development', 'Reduced research costs', 'Better success rates'],
              },
            ].map((useCase, index) => (
              <div key={index} className="bg-white border border-secondary-200 rounded-lg p-6">
                <div className="text-4xl mb-4 text-center">{useCase.icon}</div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3 text-center">
                  {useCase.title}
                </h3>
                <p className="text-secondary-600 mb-4 text-center">
                  {useCase.description}
                </p>
                <ul className="space-y-2">
                  {useCase.benefits.map((benefit, benefitIndex) => (
                    <li key={benefitIndex} className="flex items-center text-sm text-secondary-700">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Transform Healthcare with AI
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Improve patient outcomes and operational efficiency with AI solutions 
            designed specifically for healthcare organizations.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Schedule Healthcare Consultation
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
