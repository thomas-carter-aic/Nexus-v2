'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight, Calendar, Phone, Brain } from 'lucide-react';

export function CTA() {
  return (
    <section className="section-padding bg-secondary-900">
      <div className="container">
        <div className="mx-auto max-w-4xl text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-3xl font-bold tracking-tight text-white sm:text-4xl"
          >
            Ready to Transform Your Business with AI?
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
            className="mt-6 text-lg leading-8 text-secondary-300"
          >
            Join hundreds of businesses that have successfully implemented AI with Applied Innovations Corporation. 
            Start your transformation journey with a free consultation from our AI experts.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-6"
          >
            <Link
              href="/consultation"
              className="inline-flex items-center justify-center rounded-lg bg-primary-600 px-8 py-4 text-lg font-semibold text-white shadow-sm transition-all duration-200 hover:bg-primary-700 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 focus:ring-offset-secondary-900"
            >
              <Calendar className="w-5 h-5 mr-2" />
              Schedule Free Consultation
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
            <Link
              href="/contact"
              className="inline-flex items-center justify-center rounded-lg border border-secondary-600 bg-transparent px-8 py-4 text-lg font-semibold text-white shadow-sm transition-all duration-200 hover:bg-secondary-800 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 focus:ring-offset-secondary-900"
            >
              <Phone className="w-5 h-5 mr-2" />
              Contact Our Experts
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
            className="mt-12"
          >
            <div className="rounded-2xl bg-secondary-800 p-6 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full" />
                  <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                  <div className="w-3 h-3 bg-green-500 rounded-full" />
                </div>
                <div className="text-secondary-400 text-sm font-mono">AI Transformation Process</div>
              </div>
              <div className="text-left font-mono text-sm space-y-2">
                <div className="text-secondary-400"># Step 1: Assessment & Strategy</div>
                <div className="text-green-400">$ aic assess --comprehensive --industry=your-sector</div>
                <div className="text-secondary-400 mt-4"># Step 2: Implementation Planning</div>
                <div className="text-green-400">$ aic plan --roadmap --risk-assessment</div>
                <div className="text-secondary-400 mt-4"># Step 3: AI Deployment</div>
                <div className="text-green-400">$ aic deploy --nexus-platform --secure</div>
                <div className="text-secondary-400 mt-4"># Step 4: Team Enablement</div>
                <div className="text-green-400">$ aic train --workforce --ongoing-support</div>
                <div className="text-secondary-400 mt-4">✓ AI transformation complete - ROI achieved</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            viewport={{ once: true }}
            className="mt-8 flex items-center justify-center space-x-6 text-sm text-secondary-400"
          >
            <div className="flex items-center">
              <Brain className="w-4 h-4 mr-2" />
              Free Initial Consultation
            </div>
            <div>•</div>
            <div>No Obligation Assessment</div>
            <div>•</div>
            <div>Proven Track Record</div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
