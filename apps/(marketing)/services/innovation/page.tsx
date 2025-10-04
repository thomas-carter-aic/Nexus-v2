import type { Metadata } from 'next';
import { Lightbulb, CheckCircle, Zap, Target, TrendingUp, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'AI Innovation Consulting - Applied Innovations Corporation',
  description: 'Identify and develop innovative AI use cases that drive competitive advantage and business growth through cutting-edge solutions.',
};

export default function AIInnovationPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-yellow-600 rounded-2xl mb-6">
              <Lightbulb className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              AI Innovation Consulting
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Identify and develop innovative AI use cases that drive competitive advantage 
              and business growth through cutting-edge solutions and strategic thinking.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Explore Innovation
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
                Drive Innovation with AI
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                Stay ahead of the competition by identifying breakthrough AI opportunities 
                that can transform your industry and create new revenue streams.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'Use case discovery and validation',
                  'Proof of concept development',
                  'Innovation lab establishment',
                  'Market analysis and competitive intelligence',
                ].map((item, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-yellow-500 mr-3 flex-shrink-0" />
                    <span className="text-secondary-700">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-2">150+</div>
                  <div className="text-sm text-secondary-600">Innovation Projects</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-2">80%</div>
                  <div className="text-sm text-secondary-600">Success Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-2">25+</div>
                  <div className="text-sm text-secondary-600">Industries</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-2">$50M+</div>
                  <div className="text-sm text-secondary-600">Value Created</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Innovation Process */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Innovation Process</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Systematic approach to AI innovation and breakthrough discovery
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Discovery',
                description: 'Identify breakthrough AI opportunities',
                icon: Target,
                color: 'bg-blue-100 text-blue-600',
              },
              {
                title: 'Validation',
                description: 'Test and validate innovative concepts',
                icon: Zap,
                color: 'bg-green-100 text-green-600',
              },
              {
                title: 'Development',
                description: 'Build proof of concepts and prototypes',
                icon: Lightbulb,
                color: 'bg-yellow-100 text-yellow-600',
              },
              {
                title: 'Scale',
                description: 'Scale successful innovations to market',
                icon: TrendingUp,
                color: 'bg-purple-100 text-purple-600',
              },
            ].map((step, index) => (
              <div key={index} className="bg-white rounded-lg p-6 text-center shadow-sm">
                <div className={`inline-flex items-center justify-center w-12 h-12 ${step.color} rounded-xl mb-4`}>
                  <step.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {step.title}
                </h3>
                <p className="text-secondary-600">
                  {step.description}
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
            Innovate with AI
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Discover breakthrough AI opportunities that can transform your business 
            and create competitive advantages.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Start Innovation Journey
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
