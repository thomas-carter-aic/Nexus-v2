import type { Metadata } from 'next';
import { Brain, Target, TrendingUp, Shield, Users, CheckCircle } from 'lucide-react';

export const metadata: Metadata = {
  title: 'AI Strategy & Assessment - Applied Innovations Corporation',
  description: 'Comprehensive AI readiness evaluation and strategic roadmap development tailored to your business objectives.',
};

export default function AIStrategyPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl mb-6">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              AI Strategy & Assessment
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Comprehensive AI readiness evaluation and strategic roadmap development 
              tailored to your business objectives and industry requirements.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Start Your Assessment
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
                Build Your AI Foundation
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                Before implementing AI solutions, it's crucial to understand your organization's 
                readiness, identify opportunities, and create a strategic roadmap that aligns 
                with your business goals.
              </p>
              <p className="text-secondary-600 mb-8">
                Our AI Strategy & Assessment service provides a comprehensive evaluation of your 
                current state, identifies high-impact use cases, and delivers a detailed roadmap 
                for successful AI transformation.
              </p>
              <div className="space-y-4">
                {[
                  'Comprehensive AI maturity assessment',
                  'Strategic roadmap development',
                  'ROI analysis and business case creation',
                  'Risk evaluation and mitigation planning',
                ].map((item, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                    <span className="text-secondary-700">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-2xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600 mb-2">95%</div>
                  <div className="text-sm text-secondary-600">Strategy Success Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600 mb-2">4-6</div>
                  <div className="text-sm text-secondary-600">Weeks to Complete</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600 mb-2">340%</div>
                  <div className="text-sm text-secondary-600">Average ROI</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600 mb-2">500+</div>
                  <div className="text-sm text-secondary-600">Assessments Completed</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Process */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Our Assessment Process</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              A systematic approach to understanding your AI readiness and opportunities
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                step: '01',
                title: 'Current State Analysis',
                description: 'Evaluate existing technology, data, and processes',
                icon: Target,
              },
              {
                step: '02',
                title: 'Opportunity Identification',
                description: 'Identify high-impact AI use cases for your business',
                icon: TrendingUp,
              },
              {
                step: '03',
                title: 'Risk Assessment',
                description: 'Analyze potential risks and compliance requirements',
                icon: Shield,
              },
              {
                step: '04',
                title: 'Strategic Roadmap',
                description: 'Create detailed implementation plan with timelines',
                icon: Users,
              },
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="relative mb-6">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-sm">
                    <item.icon className="w-8 h-8 text-primary-600" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
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

      {/* Deliverables */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">What You'll Receive</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Comprehensive documentation and strategic guidance for your AI journey
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'AI Maturity Assessment Report',
                description: 'Detailed analysis of your current AI readiness across technology, data, processes, and people.',
                items: ['Technology infrastructure evaluation', 'Data quality and availability assessment', 'Process automation opportunities', 'Skills gap analysis'],
              },
              {
                title: 'Strategic AI Roadmap',
                description: 'Prioritized implementation plan with timelines, resources, and success metrics.',
                items: ['Phased implementation approach', 'Resource requirements', 'Timeline and milestones', 'Success metrics and KPIs'],
              },
              {
                title: 'Business Case & ROI Analysis',
                description: 'Financial justification and expected returns for your AI investments.',
                items: ['Cost-benefit analysis', 'ROI projections', 'Risk assessment', 'Funding recommendations'],
              },
            ].map((deliverable, index) => (
              <div key={index} className="bg-white border border-secondary-200 rounded-lg p-6">
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                  {deliverable.title}
                </h3>
                <p className="text-secondary-600 mb-4">
                  {deliverable.description}
                </p>
                <ul className="space-y-2">
                  {deliverable.items.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-start text-sm text-secondary-700">
                      <div className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-2 mr-2 flex-shrink-0"></div>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Start Your AI Strategy?
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Get a comprehensive assessment of your AI readiness and a strategic roadmap 
            for successful implementation.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="/consultation" className="btn-primary text-lg px-8 py-4">
              Schedule Free Consultation
            </a>
            <a href="/contact" className="btn-secondary text-lg px-8 py-4 bg-transparent border-white text-white hover:bg-white hover:text-secondary-900">
              Learn More
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
