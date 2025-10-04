import type { Metadata } from 'next';
import { Cog, CheckCircle, Zap, Shield, Users, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'AI Implementation & Integration - Applied Innovations Corporation',
  description: 'End-to-end AI solution deployment with seamless integration into your existing business processes and systems.',
};

export default function AIImplementationPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-600 rounded-2xl mb-6">
              <Cog className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              AI Implementation & Integration
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              End-to-end AI solution deployment with seamless integration into your existing 
              business processes, ensuring minimal disruption and maximum value delivery.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Start Implementation
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
                Seamless AI Integration
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                Our implementation service transforms your AI strategy into reality through 
                careful planning, expert execution, and seamless integration with your 
                existing systems and workflows.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'Custom AI solution development',
                  'Legacy system integration',
                  'Data pipeline setup and optimization',
                  'Performance monitoring and optimization',
                ].map((item, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                    <span className="text-secondary-700">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">98%</div>
                  <div className="text-sm text-secondary-600">Success Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">3-6</div>
                  <div className="text-sm text-secondary-600">Months Timeline</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">99.9%</div>
                  <div className="text-sm text-secondary-600">System Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">24/7</div>
                  <div className="text-sm text-secondary-600">Support</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Implementation Process */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Implementation Process</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Our proven methodology ensures successful AI deployment
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                step: '01',
                title: 'Solution Design',
                description: 'Custom AI architecture tailored to your requirements',
                icon: Cog,
              },
              {
                step: '02',
                title: 'Development',
                description: 'Build and configure AI models and systems',
                icon: Zap,
              },
              {
                step: '03',
                title: 'Integration',
                description: 'Seamless connection with existing systems',
                icon: Shield,
              },
              {
                step: '04',
                title: 'Deployment',
                description: 'Go-live with full support and monitoring',
                icon: Users,
              },
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="relative mb-6">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-sm">
                    <item.icon className="w-8 h-8 text-green-600" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {item.step}
                  </div>
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {item.title}
                </h3>
                <p className="text-secondary-600">
                  {item.description}
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
            Ready to Implement AI?
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Transform your business with expertly implemented AI solutions that integrate 
            seamlessly with your existing operations.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Start Your Implementation
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
