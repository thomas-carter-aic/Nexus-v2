import type { Metadata } from 'next';
import { Handshake, CheckCircle, Users, TrendingUp, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Partners - Applied Innovations Corporation',
  description: 'Our strategic partnerships with leading technology companies and industry experts to deliver comprehensive AI solutions.',
};

const partners = [
  {
    name: 'Microsoft Azure',
    type: 'Cloud Platform Partner',
    description: 'Strategic partnership for cloud infrastructure and AI services',
    logo: '🔷',
    benefits: ['Azure AI integration', 'Enterprise cloud solutions', 'Global scalability'],
  },
  {
    name: 'NVIDIA',
    type: 'Technology Partner',
    description: 'GPU computing and AI acceleration partnership',
    logo: '🟢',
    benefits: ['High-performance computing', 'AI model training', 'Edge AI solutions'],
  },
  {
    name: 'Amazon Web Services',
    type: 'Cloud Partner',
    description: 'AWS cloud services and AI/ML platform integration',
    logo: '🟠',
    benefits: ['AWS AI services', 'Scalable infrastructure', 'Global deployment'],
  },
  {
    name: 'Google Cloud',
    type: 'AI Platform Partner',
    description: 'Google Cloud AI and machine learning services',
    logo: '🔴',
    benefits: ['Google AI Platform', 'TensorFlow integration', 'Advanced analytics'],
  },
  {
    name: 'Snowflake',
    type: 'Data Partner',
    description: 'Data cloud platform for AI and analytics',
    logo: '❄️',
    benefits: ['Data warehousing', 'Real-time analytics', 'Data sharing'],
  },
  {
    name: 'Databricks',
    type: 'Analytics Partner',
    description: 'Unified analytics platform for big data and machine learning',
    logo: '🧱',
    benefits: ['MLOps platform', 'Data engineering', 'Collaborative analytics'],
  },
];

const partnerPrograms = [
  {
    title: 'Technology Partners',
    description: 'Leading technology companies providing platforms and infrastructure',
    icon: '🔧',
    count: '15+',
  },
  {
    title: 'Consulting Partners',
    description: 'Professional services firms and implementation specialists',
    icon: '👥',
    count: '25+',
  },
  {
    title: 'Industry Partners',
    description: 'Domain experts and industry-specific solution providers',
    icon: '🏢',
    count: '30+',
  },
  {
    title: 'Academic Partners',
    description: 'Universities and research institutions for cutting-edge AI research',
    icon: '🎓',
    count: '10+',
  },
];

export default function PartnersPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl mb-6">
              <Handshake className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Our Partners
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              We collaborate with leading technology companies and industry experts to deliver 
              comprehensive AI solutions that drive business transformation and success.
            </p>
          </div>
        </div>
      </section>

      {/* Partner Programs */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Partner Ecosystem</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Our comprehensive partner network spans technology, consulting, industry, and academic sectors
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {partnerPrograms.map((program, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl mb-4">{program.icon}</div>
                <div className="text-3xl font-bold text-primary-600 mb-2">{program.count}</div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {program.title}
                </h3>
                <p className="text-secondary-600">
                  {program.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Strategic Partners */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Strategic Partners</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Key partnerships that enable us to deliver world-class AI solutions
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {partners.map((partner, index) => (
              <div key={index} className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-4">
                  <div className="text-3xl mr-3">{partner.logo}</div>
                  <div>
                    <h3 className="text-lg font-semibold text-secondary-900">
                      {partner.name}
                    </h3>
                    <p className="text-sm text-primary-600">{partner.type}</p>
                  </div>
                </div>
                
                <p className="text-secondary-600 mb-4">
                  {partner.description}
                </p>

                <div className="space-y-2">
                  {partner.benefits.map((benefit, benefitIndex) => (
                    <div key={benefitIndex} className="flex items-center text-sm text-secondary-700">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                      {benefit}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Partnership Benefits */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Partnership Benefits</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              How our partnerships benefit your AI transformation journey
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'Best-in-Class Technology',
                description: 'Access to cutting-edge AI platforms and tools from industry leaders',
                icon: TrendingUp,
              },
              {
                title: 'Comprehensive Solutions',
                description: 'End-to-end solutions that integrate seamlessly across platforms',
                icon: CheckCircle,
              },
              {
                title: 'Expert Support',
                description: 'Combined expertise from multiple industry-leading organizations',
                icon: Users,
              },
            ].map((benefit, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
                  <benefit.icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {benefit.title}
                </h3>
                <p className="text-secondary-600">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Partner CTA */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Become a Partner
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Join our partner ecosystem and help businesses transform with AI. 
            Let's build the future of artificial intelligence together.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="/contact" className="btn-primary text-lg px-8 py-4">
              Partner With Us
              <ArrowRight className="w-5 h-5 ml-2" />
            </a>
            <a href="/consultation" className="btn-secondary text-lg px-8 py-4 bg-transparent border-white text-white hover:bg-white hover:text-secondary-900">
              Learn More
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
