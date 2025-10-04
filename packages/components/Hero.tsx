'use client';

import Link from 'next/link';
import { ArrowRight, Brain, Shield, Users } from 'lucide-react';
import { motion } from 'framer-motion';

export function Hero() {
  return (
    <section className="relative overflow-hidden gradient-bg">
      <div className="container section-padding">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <div className="inline-flex items-center rounded-full bg-primary-50 px-4 py-2 text-sm font-medium text-primary-700 ring-1 ring-inset ring-primary-700/10">
              <Brain className="w-4 h-4 mr-2" />
              Trusted AI Transformation Partner
            </div>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl lg:text-7xl"
          >
            Transform Your Business with{' '}
            <span className="gradient-text">AI Excellence</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-6 text-lg leading-8 text-secondary-600 max-w-2xl mx-auto"
          >
            Applied Innovations Corporation empowers SMBs and enterprises with strategic AI consulting, 
            transformation services, and our flagship Nexus platform to implement AI safely and effectively.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-10 flex items-center justify-center gap-x-6"
          >
            <Link href="/consultation" className="btn-primary text-lg px-8 py-4">
              Free Consultation
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
            <Link
              href="#services"
              className="btn-secondary text-lg px-8 py-4"
            >
              <Brain className="w-5 h-5 mr-2" />
              Our Services
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mt-16"
          >
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary-600/20 to-secondary-600/20 rounded-2xl blur-3xl" />
              <div className="relative bg-secondary-900 rounded-2xl p-8 shadow-2xl">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex space-x-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full" />
                    <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                    <div className="w-3 h-3 bg-green-500 rounded-full" />
                  </div>
                  <div className="text-secondary-400 text-sm font-mono">nexus-platform</div>
                </div>
                <div className="text-left font-mono text-sm">
                  <div className="text-green-400">$ nexus ai-audit --comprehensive</div>
                  <div className="text-secondary-400 mt-2">✓ Analyzing AI readiness...</div>
                  <div className="text-secondary-400">✓ Identifying transformation opportunities...</div>
                  <div className="text-secondary-400">✓ Generating strategic recommendations...</div>
                  <div className="text-green-400 mt-2">$ nexus deploy --ai-enabled</div>
                  <div className="text-secondary-400 mt-2">🚀 AI-powered solutions deployed successfully</div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Service highlights */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="container pb-16"
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
              <Brain className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-secondary-900 mb-2">AI Strategy & Consulting</h3>
            <p className="text-secondary-600">
              Expert guidance on AI implementation, risk assessment, and strategic planning for your business.
            </p>
          </div>
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
              <Shield className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-secondary-900 mb-2">Safe AI Implementation</h3>
            <p className="text-secondary-600">
              Secure, compliant AI deployment with comprehensive risk management and governance frameworks.
            </p>
          </div>
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
              <Users className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-secondary-900 mb-2">Team Enablement</h3>
            <p className="text-secondary-600">
              Comprehensive training and enablement programs to upskill your team for the AI-driven future.
            </p>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
