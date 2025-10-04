import type { Metadata } from 'next';
import { MessageCircle, Phone, Mail, Book, Search, Clock, Users, Zap } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Support - Applied Innovations Corporation',
  description: 'Get help and support for Applied Innovations AI services. Access documentation, contact support, and find answers to common questions.',
};

const supportOptions = [
  {
    icon: MessageCircle,
    title: 'Live Chat',
    description: 'Get instant help from our support team',
    availability: '24/7 for Enterprise customers',
    action: 'Start Chat',
    color: 'bg-blue-100 text-blue-600',
  },
  {
    icon: Phone,
    title: 'Phone Support',
    description: 'Speak directly with our technical experts',
    availability: 'Mon-Fri, 6AM-6PM PST',
    action: 'Call Now',
    color: 'bg-green-100 text-green-600',
  },
  {
    icon: Mail,
    title: 'Email Support',
    description: 'Send us detailed questions and get comprehensive answers',
    availability: 'Response within 4 hours',
    action: 'Send Email',
    color: 'bg-purple-100 text-purple-600',
  },
  {
    icon: Book,
    title: 'Documentation',
    description: 'Comprehensive guides and API documentation',
    availability: 'Available 24/7',
    action: 'Browse Docs',
    color: 'bg-orange-100 text-orange-600',
  },
];

const faqCategories = [
  {
    title: 'Getting Started',
    questions: [
      {
        question: 'How do I get started with Applied Innovations AI services?',
        answer: 'Start with our free consultation to assess your AI readiness and discuss your specific needs. Our team will create a customized roadmap for your AI transformation journey.',
      },
      {
        question: 'What is the Nexus platform?',
        answer: 'Nexus is our proprietary AI platform that accelerates AI implementation with pre-built components, automated workflows, and comprehensive management tools.',
      },
      {
        question: 'How long does a typical AI implementation take?',
        answer: 'Implementation timelines vary based on project complexity, but most projects are completed within 3-6 months. We provide detailed timelines during the planning phase.',
      },
    ],
  },
  {
    title: 'Technical Support',
    questions: [
      {
        question: 'What are your system requirements?',
        answer: 'Our platform is cloud-based and accessible through modern web browsers. For on-premise deployments, we provide detailed system requirements based on your specific needs.',
      },
      {
        question: 'How do you ensure data security?',
        answer: 'We implement enterprise-grade security measures including encryption, access controls, regular audits, and compliance with industry standards like SOC 2 and ISO 27001.',
      },
      {
        question: 'Do you provide API access?',
        answer: 'Yes, we provide comprehensive REST APIs for integration with your existing systems. Full API documentation is available in our developer portal.',
      },
    ],
  },
  {
    title: 'Billing & Pricing',
    questions: [
      {
        question: 'How is pricing structured?',
        answer: 'We offer flexible pricing models including project-based, subscription, and enterprise licensing options. Contact us for a customized quote based on your needs.',
      },
      {
        question: 'Do you offer free trials?',
        answer: 'Yes, we offer a 30-day free trial of our Nexus platform for qualified businesses. This includes access to core features and basic support.',
      },
      {
        question: 'What payment methods do you accept?',
        answer: 'We accept major credit cards, ACH transfers, and wire transfers. Enterprise customers can also arrange for invoicing and purchase orders.',
      },
    ],
  },
];

const resources = [
  {
    title: 'Quick Start Guide',
    description: 'Get up and running with our platform in minutes',
    link: '/docs/quick-start',
    icon: Zap,
  },
  {
    title: 'API Documentation',
    description: 'Complete reference for our REST APIs',
    link: '/docs/api',
    icon: Book,
  },
  {
    title: 'Video Tutorials',
    description: 'Step-by-step video guides for common tasks',
    link: '/docs/tutorials',
    icon: Users,
  },
  {
    title: 'Best Practices',
    description: 'Learn from our AI implementation expertise',
    link: '/docs/best-practices',
    icon: Search,
  },
];

export default function SupportPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              How Can We Help You?
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Get the support you need to succeed with AI. Our expert team is here to help 
              you every step of the way.
            </p>
          </div>
        </div>
      </section>

      {/* Support Options */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Get Support</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Choose the support option that works best for you
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {supportOptions.map((option, index) => (
              <div key={index} className="bg-white border border-secondary-200 rounded-lg p-6 text-center hover:shadow-lg transition-shadow">
                <div className={`inline-flex items-center justify-center w-16 h-16 ${option.color} rounded-2xl mb-4`}>
                  <option.icon className="w-8 h-8" />
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-2">
                  {option.title}
                </h3>
                <p className="text-secondary-600 mb-4">
                  {option.description}
                </p>
                <div className="flex items-center justify-center text-sm text-secondary-500 mb-4">
                  <Clock className="w-4 h-4 mr-1" />
                  {option.availability}
                </div>
                <button className="btn-primary w-full text-sm">
                  {option.action}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Frequently Asked Questions</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Find answers to common questions about our AI services and platform
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {faqCategories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="bg-white rounded-lg p-6">
                <h3 className="text-xl font-semibold text-secondary-900 mb-6">
                  {category.title}
                </h3>
                <div className="space-y-6">
                  {category.questions.map((faq, faqIndex) => (
                    <div key={faqIndex}>
                      <h4 className="text-sm font-semibold text-secondary-900 mb-2">
                        {faq.question}
                      </h4>
                      <p className="text-sm text-secondary-600">
                        {faq.answer}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <p className="text-secondary-600 mb-4">
              Can't find what you're looking for?
            </p>
            <button className="btn-secondary">
              View All FAQs
            </button>
          </div>
        </div>
      </section>

      {/* Resources Section */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Helpful Resources</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Explore our documentation and learning materials
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {resources.map((resource, index) => (
              <div key={index} className="bg-white border border-secondary-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
                  <resource.icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-2">
                  {resource.title}
                </h3>
                <p className="text-secondary-600 mb-4">
                  {resource.description}
                </p>
                <a href={resource.link} className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                  Learn More →
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="section-padding bg-secondary-900">
        <div className="container">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-6">
              Still Need Help?
            </h2>
            <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
              Our support team is standing by to help you succeed with AI. 
              Get in touch and we'll respond quickly.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <a href="mailto:support@appliedinnovations.ai" className="btn-primary text-lg px-8 py-4">
                <Mail className="w-5 h-5 mr-2" />
                Email Support
              </a>
              <a href="tel:+1-555-AI-TRANSFORM" className="btn-secondary text-lg px-8 py-4 bg-transparent border-white text-white hover:bg-white hover:text-secondary-900">
                <Phone className="w-5 h-5 mr-2" />
                Call Us
              </a>
            </div>
            
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-2xl font-bold text-white mb-2">24/7</div>
                <div className="text-secondary-300">Enterprise Support</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white mb-2">&lt; 4hrs</div>
                <div className="text-secondary-300">Average Response Time</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white mb-2">98%</div>
                <div className="text-secondary-300">Customer Satisfaction</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
