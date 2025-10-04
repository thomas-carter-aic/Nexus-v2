import type { Metadata } from 'next';
import { Cog, CheckCircle, TrendingUp, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Manufacturing AI Solutions - Applied Innovations Corporation',
  description: 'AI solutions for manufacturing including predictive maintenance, quality control, and supply chain optimization.',
};

export default function ManufacturingSolutionsPage() {
  return (
    <div className="bg-white">
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-orange-600 rounded-2xl mb-6">
              <Cog className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Manufacturing AI Solutions
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Optimize manufacturing operations with AI solutions for predictive maintenance, 
              quality control, and supply chain optimization.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Optimize Manufacturing
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
                title: 'Predictive Maintenance',
                description: 'AI-powered equipment monitoring and maintenance',
                icon: '🔧',
                benefits: ['70% reduction in downtime', '35% lower maintenance costs', '90% prediction accuracy'],
              },
              {
                title: 'Quality Control',
                description: 'Automated quality inspection and defect detection',
                icon: '🔍',
                benefits: ['99% defect detection', 'Reduced waste', 'Consistent quality'],
              },
              {
                title: 'Supply Chain',
                description: 'End-to-end supply chain optimization',
                icon: '📦',
                benefits: ['Optimized inventory', 'Reduced costs', 'Better forecasting'],
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
            Smart Manufacturing
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Transform your manufacturing operations with AI-powered optimization 
            and predictive capabilities.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Optimize Operations
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
