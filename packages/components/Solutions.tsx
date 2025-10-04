'use client';

import { motion } from 'framer-motion';
import { Building2, Users, Zap, Shield, TrendingUp, Cpu } from 'lucide-react';

const solutions = [
  {
    title: 'Small & Medium Businesses',
    description: 'Accessible AI solutions designed for growing businesses ready to leverage AI for competitive advantage.',
    icon: Building2,
    color: 'from-blue-500 to-blue-600',
    benefits: [
      'Cost-effective AI implementation',
      'Rapid deployment and ROI',
      'Scalable solutions that grow with you',
      'Simplified AI management tools',
    ],
    useCases: [
      'Customer service automation',
      'Sales process optimization',
      'Inventory management',
      'Marketing personalization',
    ],
  },
  {
    title: 'Enterprise Organizations',
    description: 'Enterprise-grade AI transformation with comprehensive governance, security, and scalability.',
    icon: Users,
    color: 'from-purple-500 to-purple-600',
    benefits: [
      'Enterprise-scale AI architecture',
      'Advanced security & compliance',
      'Multi-department integration',
      'Executive-level strategic guidance',
    ],
    useCases: [
      'Intelligent document processing',
      'Predictive analytics & forecasting',
      'Supply chain optimization',
      'Risk management automation',
    ],
  },
];

const industries = [
  {
    name: 'Healthcare',
    description: 'AI-powered diagnostics, patient care optimization, and operational efficiency.',
    icon: '🏥',
  },
  {
    name: 'Financial Services',
    description: 'Fraud detection, risk assessment, and automated compliance solutions.',
    icon: '🏦',
  },
  {
    name: 'Manufacturing',
    description: 'Predictive maintenance, quality control, and supply chain optimization.',
    icon: '🏭',
  },
  {
    name: 'Retail & E-commerce',
    description: 'Personalized recommendations, inventory optimization, and customer insights.',
    icon: '🛍️',
  },
  {
    name: 'Technology',
    description: 'Product intelligence, automated testing, and development acceleration.',
    icon: '💻',
  },
  {
    name: 'Professional Services',
    description: 'Document automation, client insights, and operational efficiency.',
    icon: '💼',
  },
];

export function Solutions() {
  return (
    <section id="solutions" className="section-padding gradient-bg">
      <div className="container">
        <div className="mx-auto max-w-2xl text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-3xl font-bold tracking-tight text-secondary-900 sm:text-4xl"
          >
            Tailored AI Solutions for Every Business
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
            className="mt-6 text-lg leading-8 text-secondary-600"
          >
            Whether you're a growing SMB or a large enterprise, we have the expertise 
            and solutions to accelerate your AI transformation journey.
          </motion.p>
        </div>

        {/* Business Size Solutions */}
        <div className="mx-auto mt-16 max-w-7xl">
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
            {solutions.map((solution, index) => (
              <motion.div
                key={solution.title}
                initial={{ opacity: 0, x: index === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="relative group"
              >
                <div className="card-hover rounded-2xl border border-secondary-200 bg-white p-8 shadow-sm overflow-hidden">
                  <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${solution.color} opacity-10 rounded-full -mr-16 -mt-16`} />
                  <div className="relative">
                    <div className={`inline-flex items-center justify-center w-12 h-12 bg-gradient-to-r ${solution.color} rounded-xl mb-6`}>
                      <solution.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-secondary-900 mb-4">
                      {solution.title}
                    </h3>
                    <p className="text-secondary-600 mb-6 leading-relaxed">
                      {solution.description}
                    </p>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="text-sm font-semibold text-secondary-900 mb-3 uppercase tracking-wide">
                          Key Benefits
                        </h4>
                        <ul className="space-y-2">
                          {solution.benefits.map((benefit) => (
                            <li key={benefit} className="flex items-start text-sm text-secondary-700">
                              <div className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-2 mr-2 flex-shrink-0" />
                              {benefit}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="text-sm font-semibold text-secondary-900 mb-3 uppercase tracking-wide">
                          Common Use Cases
                        </h4>
                        <ul className="space-y-2">
                          {solution.useCases.map((useCase) => (
                            <li key={useCase} className="flex items-start text-sm text-secondary-700">
                              <div className="w-1.5 h-1.5 bg-secondary-400 rounded-full mt-2 mr-2 flex-shrink-0" />
                              {useCase}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Industry Solutions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
          className="mt-20"
        >
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-secondary-900 mb-4">
              Industry-Specific Expertise
            </h3>
            <p className="text-secondary-600 max-w-2xl mx-auto">
              Deep domain knowledge across key industries, ensuring AI solutions 
              that address your specific challenges and opportunities.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {industries.map((industry, index) => (
              <motion.div
                key={industry.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card-hover rounded-xl border border-secondary-200 bg-white p-6 shadow-sm text-center"
              >
                <div className="text-3xl mb-4">{industry.icon}</div>
                <h4 className="text-lg font-semibold text-secondary-900 mb-2">
                  {industry.name}
                </h4>
                <p className="text-secondary-600 text-sm">
                  {industry.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Nexus Platform Highlight */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          viewport={{ once: true }}
          className="mt-20"
        >
          <div className="rounded-2xl border border-secondary-200 bg-white p-8 shadow-sm">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-2xl mb-6">
                <Cpu className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-2xl font-bold text-secondary-900 mb-4">
                Powered by the Nexus Platform
              </h3>
              <p className="text-secondary-600 max-w-2xl mx-auto mb-8">
                Our proprietary Nexus platform accelerates AI implementation with pre-built 
                components, automated workflows, and comprehensive management tools.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <Zap className="w-8 h-8 text-primary-600 mx-auto mb-2" />
                  <h4 className="font-semibold text-secondary-900 mb-1">Rapid Deployment</h4>
                  <p className="text-sm text-secondary-600">Deploy AI solutions 10x faster</p>
                </div>
                <div className="text-center">
                  <Shield className="w-8 h-8 text-primary-600 mx-auto mb-2" />
                  <h4 className="font-semibold text-secondary-900 mb-1">Enterprise Security</h4>
                  <p className="text-sm text-secondary-600">Built-in compliance & governance</p>
                </div>
                <div className="text-center">
                  <TrendingUp className="w-8 h-8 text-primary-600 mx-auto mb-2" />
                  <h4 className="font-semibold text-secondary-900 mb-1">Scalable Architecture</h4>
                  <p className="text-sm text-secondary-600">Grows with your business needs</p>
                </div>
                <div className="text-center">
                  <Users className="w-8 h-8 text-primary-600 mx-auto mb-2" />
                  <h4 className="font-semibold text-secondary-900 mb-1">User-Friendly</h4>
                  <p className="text-sm text-secondary-600">Intuitive interface for all users</p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
