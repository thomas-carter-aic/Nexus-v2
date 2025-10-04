import type { Metadata } from 'next';
import { DollarSign, CheckCircle, Shield, TrendingUp, Users, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Financial Services AI Solutions - Applied Innovations Corporation',
  description: 'AI solutions for financial services including fraud detection, risk assessment, and automated compliance systems.',
};

export default function FinancialSolutionsPage() {
  return (
    <div className="bg-white">
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-600 rounded-2xl mb-6">
              <DollarSign className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Financial Services AI
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Transform financial services with AI solutions for fraud detection, risk assessment, 
              automated compliance, and enhanced customer experiences.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Secure Your Finance Operations
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'Fraud Detection',
                description: 'Real-time fraud detection and prevention systems',
                icon: '🛡️',
                benefits: ['95% fraud detection accuracy', '80% reduction in false positives', '$15M+ prevented losses'],
              },
              {
                title: 'Risk Assessment',
                description: 'Advanced risk modeling and credit scoring',
                icon: '📊',
                benefits: ['Improved risk models', 'Faster loan approvals', 'Reduced default rates'],
              },
              {
                title: 'Compliance Automation',
                description: 'Automated regulatory compliance and reporting',
                icon: '📋',
                benefits: ['100% compliance rate', 'Reduced manual work', 'Faster reporting'],
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
            Secure Financial AI
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Protect your financial operations and enhance customer experiences with 
            AI solutions built for the financial industry.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Secure Your Operations
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
