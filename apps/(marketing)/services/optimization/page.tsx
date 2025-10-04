import type { Metadata } from 'next';
import { TrendingUp, CheckCircle, BarChart3, Zap, Target, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Performance Optimization - Applied Innovations Corporation',
  description: 'Continuous monitoring and optimization of AI systems to maximize ROI and business impact through data-driven improvements.',
};

export default function PerformanceOptimizationPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-red-600 rounded-2xl mb-6">
              <TrendingUp className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Performance Optimization
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Continuous monitoring and optimization of AI systems to maximize ROI and business 
              impact through data-driven improvements and performance tuning.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Optimize Performance
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Service Overview */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-secondary-900 mb-6">
                Maximize AI Performance
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                Ensure your AI systems deliver optimal performance and maximum ROI through 
                continuous monitoring, analysis, and strategic optimization.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'Performance monitoring and analytics',
                  'Cost optimization and efficiency improvements',
                  'Scalability planning and implementation',
                  'Continuous improvement processes',
                ].map((item, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
                    <span className="text-secondary-700">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-red-50 to-pink-50 rounded-2xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600 mb-2">45%</div>
                  <div className="text-sm text-secondary-600">Avg Performance Gain</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600 mb-2">30%</div>
                  <div className="text-sm text-secondary-600">Cost Reduction</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600 mb-2">99.9%</div>
                  <div className="text-sm text-secondary-600">System Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600 mb-2">24/7</div>
                  <div className="text-sm text-secondary-600">Monitoring</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Optimization Areas */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Optimization Areas</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Comprehensive optimization across all aspects of your AI systems
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Performance',
                description: 'Speed, accuracy, and efficiency improvements',
                icon: Zap,
                color: 'bg-yellow-100 text-yellow-600',
              },
              {
                title: 'Cost',
                description: 'Resource optimization and cost reduction',
                icon: Target,
                color: 'bg-green-100 text-green-600',
              },
              {
                title: 'Scalability',
                description: 'System scaling and capacity planning',
                icon: TrendingUp,
                color: 'bg-blue-100 text-blue-600',
              },
              {
                title: 'Analytics',
                description: 'Performance monitoring and insights',
                icon: BarChart3,
                color: 'bg-purple-100 text-purple-600',
              },
            ].map((area, index) => (
              <div key={index} className="bg-white rounded-lg p-6 text-center shadow-sm">
                <div className={`inline-flex items-center justify-center w-12 h-12 ${area.color} rounded-xl mb-4`}>
                  <area.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {area.title}
                </h3>
                <p className="text-secondary-600">
                  {area.description}
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
            Optimize Your AI Performance
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Maximize the value of your AI investments through continuous optimization 
            and performance improvements.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Start Optimization
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
