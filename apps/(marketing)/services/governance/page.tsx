import type { Metadata } from 'next';
import { Shield, CheckCircle, Scale, FileCheck, Users, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'AI Governance & Compliance - Applied Innovations Corporation',
  description: 'Establish robust AI governance frameworks ensuring ethical, compliant, and responsible AI usage across your organization.',
};

export default function AIGovernancePage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-600 rounded-2xl mb-6">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              AI Governance & Compliance
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Establish robust AI governance frameworks ensuring ethical, compliant, and 
              responsible AI usage while maintaining regulatory compliance and risk management.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Secure Your AI
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
                Responsible AI Implementation
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                Navigate the complex landscape of AI ethics, compliance, and governance 
                with our comprehensive framework that ensures your AI initiatives are 
                responsible, transparent, and compliant.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'Compliance framework development',
                  'Risk management and mitigation',
                  'Ethical AI guidelines implementation',
                  'Audit and monitoring systems',
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
                  <div className="text-3xl font-bold text-purple-600 mb-2">100%</div>
                  <div className="text-sm text-secondary-600">Compliance Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">50+</div>
                  <div className="text-sm text-secondary-600">Regulations Covered</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">Zero</div>
                  <div className="text-sm text-secondary-600">Compliance Violations</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">24/7</div>
                  <div className="text-sm text-secondary-600">Monitoring</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Governance Framework */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Governance Framework</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Comprehensive approach to AI governance and compliance
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Policy Development',
                description: 'Create comprehensive AI policies and procedures',
                icon: FileCheck,
                color: 'bg-purple-100 text-purple-600',
              },
              {
                title: 'Risk Assessment',
                description: 'Identify and mitigate AI-related risks',
                icon: Shield,
                color: 'bg-red-100 text-red-600',
              },
              {
                title: 'Compliance Monitoring',
                description: 'Continuous monitoring for regulatory compliance',
                icon: Scale,
                color: 'bg-blue-100 text-blue-600',
              },
              {
                title: 'Ethics Training',
                description: 'Train teams on ethical AI practices',
                icon: Users,
                color: 'bg-green-100 text-green-600',
              },
            ].map((item, index) => (
              <div key={index} className="bg-white rounded-lg p-6 text-center shadow-sm">
                <div className={`inline-flex items-center justify-center w-12 h-12 ${item.color} rounded-xl mb-4`}>
                  <item.icon className="w-6 h-6" />
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
            Ensure Responsible AI
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Implement AI governance frameworks that protect your organization while 
            enabling innovation and growth.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Get Governance Framework
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
