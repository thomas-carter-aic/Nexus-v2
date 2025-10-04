import type { Metadata } from 'next';
import { Users, CheckCircle, Shield, TrendingUp, Zap, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Enterprise AI Solutions - Applied Innovations Corporation',
  description: 'Enterprise-grade AI transformation with comprehensive governance, security, and scalability for large organizations.',
};

export default function EnterpriseSolutionsPage() {
  return (
    <div className="bg-white">
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-600 rounded-2xl mb-6">
              <Users className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Enterprise AI Solutions
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Enterprise-grade AI transformation with comprehensive governance, security, 
              and scalability designed for large organizations and complex requirements.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Transform Your Enterprise
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-secondary-900 mb-6">
                Enterprise-Scale AI
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                Large organizations require AI solutions that can handle complex requirements, 
                strict compliance needs, and enterprise-scale deployment across multiple 
                departments and geographies.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'Enterprise-scale AI architecture',
                  'Advanced security & compliance',
                  'Multi-department integration',
                  'Executive-level strategic guidance',
                ].map((item, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-purple-500 mr-3 flex-shrink-0" />
                    <span className="text-secondary-700">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">Fortune 500</div>
                  <div className="text-sm text-secondary-600">Clients Served</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">99.99%</div>
                  <div className="text-sm text-secondary-600">Enterprise Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">100%</div>
                  <div className="text-sm text-secondary-600">Compliance Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">24/7</div>
                  <div className="text-sm text-secondary-600">Enterprise Support</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Enterprise Use Cases</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              AI applications designed for enterprise complexity and scale
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Document Processing',
                description: 'Intelligent document analysis and automation',
                icon: '📄',
              },
              {
                title: 'Predictive Analytics',
                description: 'Advanced forecasting and business intelligence',
                icon: '📊',
              },
              {
                title: 'Supply Chain',
                description: 'End-to-end supply chain optimization',
                icon: '🚚',
              },
              {
                title: 'Risk Management',
                description: 'Automated risk assessment and mitigation',
                icon: '🛡️',
              },
            ].map((useCase, index) => (
              <div key={index} className="bg-white rounded-lg p-6 text-center shadow-sm">
                <div className="text-4xl mb-4">{useCase.icon}</div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {useCase.title}
                </h3>
                <p className="text-secondary-600">
                  {useCase.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Scale AI Across Your Enterprise
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Transform your entire organization with enterprise-grade AI solutions 
            that deliver measurable results at scale.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Schedule Enterprise Consultation
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
