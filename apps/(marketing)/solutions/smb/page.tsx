import type { Metadata } from 'next';
import { Building2, CheckCircle, DollarSign, Zap, TrendingUp, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Small & Medium Business AI Solutions - Applied Innovations Corporation',
  description: 'Accessible AI solutions designed for growing businesses ready to leverage AI for competitive advantage and operational efficiency.',
};

export default function SMBSolutionsPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl mb-6">
              <Building2 className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              AI Solutions for SMBs
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Accessible AI solutions designed for growing businesses ready to leverage 
              artificial intelligence for competitive advantage and operational efficiency.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Get Started Today
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-secondary-900 mb-6">
                AI That Fits Your Business
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                We understand that small and medium businesses have unique needs, budgets, 
                and timelines. Our SMB solutions are designed to deliver maximum impact 
                with minimal complexity and investment.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'Cost-effective AI implementation',
                  'Rapid deployment and ROI',
                  'Scalable solutions that grow with you',
                  'Simplified AI management tools',
                ].map((item, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-blue-500 mr-3 flex-shrink-0" />
                    <span className="text-secondary-700">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">50%</div>
                  <div className="text-sm text-secondary-600">Cost Savings</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">3x</div>
                  <div className="text-sm text-secondary-600">Faster Implementation</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">200%</div>
                  <div className="text-sm text-secondary-600">ROI in Year 1</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">95%</div>
                  <div className="text-sm text-secondary-600">Customer Satisfaction</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Common Use Cases</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              AI applications that deliver immediate value for growing businesses
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Customer Service',
                description: 'AI chatbots and automated support systems',
                icon: '🤖',
              },
              {
                title: 'Sales Optimization',
                description: 'Lead scoring and sales process automation',
                icon: '📈',
              },
              {
                title: 'Inventory Management',
                description: 'Demand forecasting and stock optimization',
                icon: '📦',
              },
              {
                title: 'Marketing Personalization',
                description: 'Targeted campaigns and customer insights',
                icon: '🎯',
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

      {/* CTA Section */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Grow with AI?
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Join hundreds of SMBs that have successfully implemented AI to drive 
            growth and competitive advantage.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Start Your AI Journey
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
