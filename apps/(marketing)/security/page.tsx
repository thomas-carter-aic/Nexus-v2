import type { Metadata } from 'next';
import { Shield, Lock, Eye, CheckCircle, Award } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Security - Applied Innovations Corporation',
  description: 'Learn about our comprehensive security measures, compliance standards, and data protection practices.',
};

export default function SecurityPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-600 rounded-2xl mb-6">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Security & Compliance
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Your data security and privacy are our top priorities. Learn about our comprehensive 
              security measures, compliance standards, and data protection practices.
            </p>
          </div>
        </div>
      </section>

      {/* Security Overview */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-secondary-900 mb-6">
                Enterprise-Grade Security
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                We implement multiple layers of security controls to protect your data and ensure 
                the integrity of our AI platform. Our security framework is designed to meet the 
                highest industry standards and regulatory requirements.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'End-to-end encryption for data in transit and at rest',
                  'Multi-factor authentication and access controls',
                  'Regular security audits and penetration testing',
                  'Compliance with SOC 2, ISO 27001, and GDPR',
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
                  <div className="text-3xl font-bold text-green-600 mb-2">99.9%</div>
                  <div className="text-sm text-secondary-600">Security Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">256-bit</div>
                  <div className="text-sm text-secondary-600">AES Encryption</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">24/7</div>
                  <div className="text-sm text-secondary-600">Security Monitoring</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">Zero</div>
                  <div className="text-sm text-secondary-600">Data Breaches</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Security Measures */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Security Measures</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Comprehensive security controls protecting your data and systems
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Data Encryption',
                description: 'AES-256 encryption for data at rest and TLS 1.3 for data in transit',
                icon: Lock,
                color: 'bg-blue-100 text-blue-600',
              },
              {
                title: 'Access Control',
                description: 'Role-based access control with multi-factor authentication',
                icon: Eye,
                color: 'bg-purple-100 text-purple-600',
              },
              {
                title: 'Network Security',
                description: 'Firewalls, intrusion detection, and network segmentation',
                icon: Shield,
                color: 'bg-green-100 text-green-600',
              },
              {
                title: 'Compliance',
                description: 'SOC 2 Type II, ISO 27001, GDPR, and HIPAA compliance',
                icon: Award,
                color: 'bg-orange-100 text-orange-600',
              },
            ].map((measure, index) => (
              <div key={index} className="bg-white rounded-lg p-6 text-center shadow-sm">
                <div className={`inline-flex items-center justify-center w-12 h-12 ${measure.color} rounded-xl mb-4`}>
                  <measure.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {measure.title}
                </h3>
                <p className="text-secondary-600">
                  {measure.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Compliance Standards */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Compliance Standards</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              We maintain compliance with industry-leading security and privacy standards
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                name: 'SOC 2 Type II',
                description: 'Service Organization Control 2 certification for security, availability, and confidentiality',
                status: 'Certified',
              },
              {
                name: 'ISO 27001',
                description: 'International standard for information security management systems',
                status: 'Certified',
              },
              {
                name: 'GDPR',
                description: 'General Data Protection Regulation compliance for EU data protection',
                status: 'Compliant',
              },
              {
                name: 'HIPAA',
                description: 'Health Insurance Portability and Accountability Act for healthcare data',
                status: 'Compliant',
              },
              {
                name: 'CCPA',
                description: 'California Consumer Privacy Act compliance for California residents',
                status: 'Compliant',
              },
              {
                name: 'PCI DSS',
                description: 'Payment Card Industry Data Security Standard for payment processing',
                status: 'Compliant',
              },
            ].map((standard, index) => (
              <div key={index} className="bg-white border border-secondary-200 rounded-lg p-6">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-semibold text-secondary-900">
                    {standard.name}
                  </h3>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    {standard.status}
                  </span>
                </div>
                <p className="text-secondary-600">
                  {standard.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Security Practices */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Security Practices</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Our ongoing security practices and procedures
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              {
                title: 'Regular Security Audits',
                items: [
                  'Annual third-party security assessments',
                  'Quarterly internal security reviews',
                  'Continuous vulnerability scanning',
                  'Penetration testing by certified professionals',
                ],
              },
              {
                title: 'Employee Security Training',
                items: [
                  'Mandatory security awareness training',
                  'Phishing simulation exercises',
                  'Secure coding practices',
                  'Incident response procedures',
                ],
              },
              {
                title: 'Data Protection',
                items: [
                  'Data minimization principles',
                  'Secure data disposal procedures',
                  'Data loss prevention systems',
                  'Regular backup and recovery testing',
                ],
              },
              {
                title: 'Incident Response',
                items: [
                  '24/7 security monitoring',
                  'Automated threat detection',
                  'Rapid incident response team',
                  'Transparent incident reporting',
                ],
              },
            ].map((practice, index) => (
              <div key={index} className="bg-white rounded-lg p-6">
                <h3 className="text-xl font-semibold text-secondary-900 mb-4">
                  {practice.title}
                </h3>
                <ul className="space-y-2">
                  {practice.items.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-center text-secondary-700">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Security Team */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Security Questions?
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Our security team is available to answer questions about our security practices, 
            compliance standards, and data protection measures.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="mailto:security@appliedinnovations.ai" className="btn-primary text-lg px-8 py-4">
              Contact Security Team
            </a>
            <a href="/privacy" className="btn-secondary text-lg px-8 py-4 bg-transparent border-white text-white hover:bg-white hover:text-secondary-900">
              View Privacy Policy
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
