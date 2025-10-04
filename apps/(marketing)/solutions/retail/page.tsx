import type { Metadata } from 'next';
import { ShoppingBag, CheckCircle, TrendingUp, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Retail & E-commerce AI Solutions - Applied Innovations Corporation',
  description: 'AI solutions for retail including personalized recommendations, inventory optimization, and customer insights.',
};

export default function RetailSolutionsPage() {
  return (
    <div className="bg-white">
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-pink-600 rounded-2xl mb-6">
              <ShoppingBag className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Retail & E-commerce AI
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Transform retail experiences with AI solutions for personalized recommendations, 
              inventory optimization, and deep customer insights.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Enhance Customer Experience
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
                title: 'Personalization',
                description: 'AI-driven personalization and recommendation engines',
                icon: '🎯',
                benefits: ['45% increase in conversions', '30% higher order value', '65% better retention'],
              },
              {
                title: 'Inventory Optimization',
                description: 'Smart inventory management and demand forecasting',
                icon: '📊',
                benefits: ['Reduced stockouts', 'Lower carrying costs', 'Better forecasting'],
              },
              {
                title: 'Customer Analytics',
                description: 'Deep customer insights and behavior analysis',
                icon: '👥',
                benefits: ['Better customer understanding', 'Targeted marketing', 'Improved satisfaction'],
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
            Smart Retail Solutions
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Create exceptional customer experiences and optimize operations with 
            AI-powered retail solutions.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Transform Retail Experience
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
