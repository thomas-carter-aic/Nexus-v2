'use client';

import { motion } from 'framer-motion';
import {
  Brain,
  Shield,
  Users,
  Lightbulb,
  Target,
  Cog,
  TrendingUp,
  CheckCircle,
  AlertTriangle,
  Zap,
  BookOpen,
  Rocket,
} from 'lucide-react';

const services = [
  {
    name: 'AI Strategy & Assessment',
    description: 'Comprehensive AI readiness evaluation and strategic roadmap development tailored to your business objectives.',
    icon: Brain,
    color: 'bg-blue-500',
    features: ['AI Maturity Assessment', 'Strategic Roadmapping', 'ROI Analysis', 'Risk Evaluation'],
  },
  {
    name: 'AI Implementation & Integration',
    description: 'End-to-end AI solution deployment with seamless integration into your existing business processes.',
    icon: Cog,
    color: 'bg-green-500',
    features: ['Custom AI Solutions', 'System Integration', 'Data Pipeline Setup', 'Performance Optimization'],
  },
  {
    name: 'AI Governance & Compliance',
    description: 'Establish robust AI governance frameworks ensuring ethical, compliant, and responsible AI usage.',
    icon: Shield,
    color: 'bg-purple-500',
    features: ['Compliance Frameworks', 'Risk Management', 'Ethical AI Guidelines', 'Audit & Monitoring'],
  },
  {
    name: 'Team Training & Enablement',
    description: 'Comprehensive training programs to upskill your workforce for AI-driven business transformation.',
    icon: Users,
    color: 'bg-orange-500',
    features: ['Executive Workshops', 'Technical Training', 'Change Management', 'Ongoing Support'],
  },
  {
    name: 'AI Innovation Consulting',
    description: 'Identify and develop innovative AI use cases that drive competitive advantage and business growth.',
    icon: Lightbulb,
    color: 'bg-yellow-500',
    features: ['Use Case Discovery', 'Proof of Concepts', 'Innovation Labs', 'Market Analysis'],
  },
  {
    name: 'Performance Optimization',
    description: 'Continuous monitoring and optimization of AI systems to maximize ROI and business impact.',
    icon: TrendingUp,
    color: 'bg-red-500',
    features: ['Performance Monitoring', 'Cost Optimization', 'Scalability Planning', 'Continuous Improvement'],
  },
];

export function Services() {
  return (
    <section id="services" className="section-padding bg-white">
      <div className="container">
        <div className="mx-auto max-w-2xl text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-3xl font-bold tracking-tight text-secondary-900 sm:text-4xl"
          >
            Comprehensive AI Transformation Services
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
            className="mt-6 text-lg leading-8 text-secondary-600"
          >
            From strategy to implementation, we guide your organization through every step 
            of AI transformation with expert consulting and proven methodologies.
          </motion.p>
        </div>

        <div className="mx-auto mt-16 max-w-7xl">
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
            {services.map((service, index) => (
              <motion.div
                key={service.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="relative group"
              >
                <div className="card-hover rounded-2xl border border-secondary-200 bg-white p-8 shadow-sm">
                  <div className="flex items-start space-x-4">
                    <div className={`flex-shrink-0 inline-flex items-center justify-center w-12 h-12 ${service.color} rounded-xl group-hover:scale-110 transition-transform duration-200`}>
                      <service.icon className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                        {service.name}
                      </h3>
                      <p className="text-secondary-600 mb-4 leading-relaxed">
                        {service.description}
                      </p>
                      <div className="space-y-2">
                        {service.features.map((feature) => (
                          <div key={feature} className="flex items-center text-sm text-secondary-700">
                            <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                            {feature}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <div className="rounded-2xl border border-secondary-200 bg-gradient-to-r from-primary-50 to-secondary-50 p-8 shadow-sm">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-secondary-900 mb-4">
                Why Choose Applied Innovations Corporation?
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
                    <Target className="w-6 h-6 text-primary-600" />
                  </div>
                  <h4 className="text-lg font-semibold text-secondary-900 mb-2">
                    Proven Expertise
                  </h4>
                  <p className="text-secondary-600 text-sm">
                    Deep AI expertise across industries with a track record of successful transformations
                  </p>
                </div>
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
                    <Rocket className="w-6 h-6 text-primary-600" />
                  </div>
                  <h4 className="text-lg font-semibold text-secondary-900 mb-2">
                    Nexus Platform
                  </h4>
                  <p className="text-secondary-600 text-sm">
                    Proprietary platform and tools that accelerate AI implementation and management
                  </p>
                </div>
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
                    <BookOpen className="w-6 h-6 text-primary-600" />
                  </div>
                  <h4 className="text-lg font-semibold text-secondary-900 mb-2">
                    Ongoing Support
                  </h4>
                  <p className="text-secondary-600 text-sm">
                    Continuous partnership with training, support, and optimization services
                  </p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
