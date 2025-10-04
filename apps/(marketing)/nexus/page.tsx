import type { Metadata } from 'next';
import { Suspense } from 'react';
import { 
  Cpu, Zap, Shield, TrendingUp, Users, CheckCircle, ArrowRight, 
  Play, Download, Star, Clock, Database, Cloud, Lock, 
  BarChart3, Workflow, Code, Layers, Globe, Smartphone
} from 'lucide-react';
import { PlatformDemo } from '@/components/nexus/PlatformDemo';
import { InteractiveArchitecture } from '@/components/nexus/InteractiveArchitecture';
import { FeatureComparison } from '@/components/nexus/FeatureComparison';
import { ROICalculator } from '@/components/nexus/ROICalculator';
import { TestimonialCarousel } from '@/components/nexus/TestimonialCarousel';
import { PricingCalculator } from '@/components/nexus/PricingCalculator';
import { TechnicalSpecs } from '@/components/nexus/TechnicalSpecs';

export const metadata: Metadata = {
  title: 'Nexus AI Platform - Enterprise AI Acceleration | Applied Innovations Corporation',
  description: 'Transform your business with the Nexus AI Platform. Deploy AI solutions 10x faster with pre-built components, automated workflows, and enterprise-grade security. Request a demo today.',
  keywords: 'AI platform, enterprise AI, AI acceleration, machine learning platform, AI deployment, automated workflows, AI components',
  openGraph: {
    title: 'Nexus AI Platform - Deploy AI Solutions 10x Faster',
    description: 'Enterprise AI platform with pre-built components, automated workflows, and comprehensive management tools.',
    images: ['/images/nexus-platform-hero.jpg'],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Nexus AI Platform - Enterprise AI Acceleration',
    description: 'Deploy AI solutions 10x faster with our comprehensive AI platform.',
    images: ['/images/nexus-platform-hero.jpg'],
  },
};

const platformFeatures = [
  {
    icon: Zap,
    title: 'Rapid Deployment',
    description: 'Deploy AI solutions 10x faster with pre-built components and automated workflows',
    color: 'bg-yellow-100 text-yellow-600',
    benefits: ['Pre-built AI components', 'One-click deployment', 'Automated testing', 'CI/CD integration'],
    metrics: { improvement: '10x', description: 'Faster deployment' }
  },
  {
    icon: Shield,
    title: 'Enterprise Security',
    description: 'Built-in compliance and governance with SOC 2, GDPR, and HIPAA support',
    color: 'bg-green-100 text-green-600',
    benefits: ['SOC 2 Type II certified', 'GDPR compliant', 'HIPAA ready', 'Zero-trust architecture'],
    metrics: { improvement: '99.9%', description: 'Security uptime' }
  },
  {
    icon: TrendingUp,
    title: 'Auto-Scaling',
    description: 'Intelligent scaling that adapts to your workload automatically',
    color: 'bg-blue-100 text-blue-600',
    benefits: ['Automatic scaling', 'Cost optimization', 'Performance monitoring', 'Load balancing'],
    metrics: { improvement: '75%', description: 'Cost reduction' }
  },
  {
    icon: Users,
    title: 'User Experience',
    description: 'Intuitive interface designed for both technical and business users',
    color: 'bg-purple-100 text-purple-600',
    benefits: ['No-code interface', 'Visual workflows', 'Real-time monitoring', 'Custom dashboards'],
    metrics: { improvement: '90%', description: 'User satisfaction' }
  },
  {
    icon: Database,
    title: 'Data Integration',
    description: 'Connect to any data source with 200+ pre-built connectors',
    color: 'bg-indigo-100 text-indigo-600',
    benefits: ['200+ connectors', 'Real-time sync', 'Data transformation', 'Quality monitoring'],
    metrics: { improvement: '200+', description: 'Data sources' }
  },
  {
    icon: Cloud,
    title: 'Multi-Cloud',
    description: 'Deploy across AWS, Azure, GCP, or on-premises infrastructure',
    color: 'bg-cyan-100 text-cyan-600',
    benefits: ['Multi-cloud support', 'Hybrid deployment', 'Edge computing', 'Disaster recovery'],
    metrics: { improvement: '99.99%', description: 'Availability' }
  },
  {
    icon: BarChart3,
    title: 'Analytics & Insights',
    description: 'Comprehensive analytics with real-time monitoring and reporting',
    color: 'bg-orange-100 text-orange-600',
    benefits: ['Real-time dashboards', 'Custom reports', 'Predictive analytics', 'Anomaly detection'],
    metrics: { improvement: '5x', description: 'Faster insights' }
  },
  {
    icon: Workflow,
    title: 'Workflow Automation',
    description: 'Visual workflow builder with advanced automation capabilities',
    color: 'bg-pink-100 text-pink-600',
    benefits: ['Visual builder', 'Event triggers', 'Conditional logic', 'Error handling'],
    metrics: { improvement: '80%', description: 'Process automation' }
  }
];

const useCases = [
  {
    title: 'Predictive Analytics',
    description: 'Forecast trends and make data-driven decisions',
    icon: TrendingUp,
    industries: ['Finance', 'Retail', 'Manufacturing'],
    timeToValue: '2-4 weeks',
    roi: '300%'
  },
  {
    title: 'Document Processing',
    description: 'Automate document analysis and data extraction',
    icon: Code,
    industries: ['Legal', 'Healthcare', 'Insurance'],
    timeToValue: '1-2 weeks',
    roi: '250%'
  },
  {
    title: 'Customer Intelligence',
    description: 'Understand customer behavior and preferences',
    icon: Users,
    industries: ['E-commerce', 'SaaS', 'Media'],
    timeToValue: '3-6 weeks',
    roi: '400%'
  },
  {
    title: 'Process Optimization',
    description: 'Optimize operations with intelligent automation',
    icon: Workflow,
    industries: ['Manufacturing', 'Logistics', 'Energy'],
    timeToValue: '4-8 weeks',
    roi: '200%'
  }
];

const testimonials = [
  {
    quote: "Nexus reduced our AI deployment time from months to weeks. The pre-built components and automated workflows are game-changers.",
    author: "Sarah Chen",
    title: "CTO",
    company: "TechCorp Industries",
    avatar: "/images/testimonials/sarah-chen.jpg",
    rating: 5,
    results: "10x faster deployment"
  },
  {
    quote: "The security and compliance features gave us confidence to deploy AI across our entire organization. Outstanding platform.",
    author: "Michael Rodriguez",
    title: "CISO",
    company: "SecureBank",
    avatar: "/images/testimonials/michael-rodriguez.jpg",
    rating: 5,
    results: "100% compliance achieved"
  },
  {
    quote: "ROI was evident within the first quarter. Nexus transformed how we approach AI implementation.",
    author: "Dr. Emily Watson",
    title: "Head of Innovation",
    company: "MedTech Solutions",
    avatar: "/images/testimonials/emily-watson.jpg",
    rating: 5,
    results: "300% ROI in Q1"
  }
];

export default function NexusPlatformPage() {
  return (
    <div className="bg-white">
      {/* Enhanced Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-secondary-50">
          <div className="absolute inset-0 bg-[url('/images/grid-pattern.svg')] opacity-10"></div>
        </div>
        
        <div className="relative section-padding">
          <div className="container">
            <div className="mx-auto max-w-4xl text-center">
              {/* Platform Badge */}
              <div className="inline-flex items-center bg-primary-100 text-primary-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
                <Star className="w-4 h-4 mr-2" />
                #1 Enterprise AI Platform
              </div>
              
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-3xl mb-8 shadow-lg">
                <Cpu className="w-10 h-10 text-white" />
              </div>
              
              <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-secondary-900 mb-6">
                The <span className="bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">Nexus</span> Platform
              </h1>
              
              <p className="text-xl md:text-2xl leading-relaxed text-secondary-600 mb-8 max-w-3xl mx-auto">
                Deploy AI solutions <strong>10x faster</strong> with our enterprise-grade platform. 
                Pre-built components, automated workflows, and comprehensive management tools.
              </p>
              
              {/* Key Stats */}
              <div className="flex flex-wrap justify-center gap-8 mb-10 text-sm">
                <div className="flex items-center text-secondary-600">
                  <Clock className="w-4 h-4 mr-2 text-primary-600" />
                  Deploy in minutes, not months
                </div>
                <div className="flex items-center text-secondary-600">
                  <Shield className="w-4 h-4 mr-2 text-green-600" />
                  Enterprise-grade security
                </div>
                <div className="flex items-center text-secondary-600">
                  <Globe className="w-4 h-4 mr-2 text-blue-600" />
                  500+ active deployments
                </div>
              </div>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
                <a href="/consultation" className="btn-primary text-lg px-8 py-4 shadow-lg hover:shadow-xl transition-shadow">
                  <Play className="w-5 h-5 mr-2" />
                  Watch Demo
                </a>
                <a href="#features" className="btn-secondary text-lg px-8 py-4">
                  Explore Features
                  <ArrowRight className="w-5 h-5 ml-2" />
                </a>
                <a href="#pricing" className="text-primary-600 hover:text-primary-700 font-medium text-lg">
                  View Pricing →
                </a>
              </div>
              
              {/* Trust Indicators */}
              <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
                <div className="text-sm text-secondary-500">Trusted by:</div>
                <div className="flex items-center gap-6">
                  <span className="text-secondary-400 font-medium">Fortune 500</span>
                  <span className="text-secondary-400 font-medium">Healthcare</span>
                  <span className="text-secondary-400 font-medium">Financial Services</span>
                  <span className="text-secondary-400 font-medium">Manufacturing</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Platform Demo */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">See Nexus in Action</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              Experience the power of our platform with an interactive demo
            </p>
          </div>
          
          <Suspense fallback={<div className="h-96 bg-secondary-100 rounded-lg animate-pulse"></div>}>
            <PlatformDemo />
          </Suspense>
        </div>
      </section>

      {/* Enhanced Features Grid */}
      <section id="features" className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Platform Capabilities</h2>
            <p className="text-xl text-secondary-600 max-w-3xl mx-auto">
              Everything you need to implement, manage, and scale AI solutions across your organization
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {platformFeatures.map((feature, index) => (
              <div key={index} className="group bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 border border-secondary-100">
                <div className={`inline-flex items-center justify-center w-14 h-14 ${feature.color} rounded-xl mb-4 group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-7 h-7" />
                </div>
                
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                  {feature.title}
                </h3>
                
                <p className="text-secondary-600 mb-4">
                  {feature.description}
                </p>
                
                {/* Key Benefits */}
                <ul className="space-y-2 mb-4">
                  {feature.benefits.slice(0, 2).map((benefit, idx) => (
                    <li key={idx} className="flex items-center text-sm text-secondary-600">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                      {benefit}
                    </li>
                  ))}
                </ul>
                
                {/* Metric */}
                <div className="bg-secondary-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-primary-600">{feature.metrics.improvement}</div>
                  <div className="text-xs text-secondary-600">{feature.metrics.description}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive Architecture Diagram */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Platform Architecture</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              Explore our scalable, secure, and flexible architecture
            </p>
          </div>
          
          <Suspense fallback={<div className="h-96 bg-secondary-100 rounded-lg animate-pulse"></div>}>
            <InteractiveArchitecture />
          </Suspense>
        </div>
      </section>

      {/* Use Cases & ROI */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Popular Use Cases</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              See how organizations are using Nexus to transform their operations
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {useCases.map((useCase, index) => (
              <div key={index} className="bg-white rounded-xl p-8 shadow-sm hover:shadow-lg transition-shadow">
                <div className="flex items-start mb-6">
                  <div className="bg-primary-100 text-primary-600 p-3 rounded-xl mr-4">
                    <useCase.icon className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                      {useCase.title}
                    </h3>
                    <p className="text-secondary-600 mb-4">
                      {useCase.description}
                    </p>
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-lg font-bold text-primary-600">{useCase.timeToValue}</div>
                    <div className="text-xs text-secondary-600">Time to Value</div>
                  </div>
                  <div>
                    <div className="text-lg font-bold text-green-600">{useCase.roi}</div>
                    <div className="text-xs text-secondary-600">Average ROI</div>
                  </div>
                  <div>
                    <div className="text-lg font-bold text-blue-600">{useCase.industries.length}</div>
                    <div className="text-xs text-secondary-600">Industries</div>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-secondary-100">
                  <div className="text-sm text-secondary-600 mb-2">Popular in:</div>
                  <div className="flex flex-wrap gap-2">
                    {useCase.industries.map((industry, idx) => (
                      <span key={idx} className="bg-secondary-100 text-secondary-700 px-2 py-1 rounded text-xs">
                        {industry}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ROI Calculator */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Calculate Your ROI</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              See the potential return on investment for your organization
            </p>
          </div>
          
          <Suspense fallback={<div className="h-96 bg-secondary-100 rounded-lg animate-pulse"></div>}>
            <ROICalculator />
          </Suspense>
        </div>
      </section>

      {/* Feature Comparison */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Why Choose Nexus?</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              See how we compare to traditional AI implementation approaches
            </p>
          </div>
          
          <Suspense fallback={<div className="h-96 bg-secondary-100 rounded-lg animate-pulse"></div>}>
            <FeatureComparison />
          </Suspense>
        </div>
      </section>

      {/* Customer Testimonials */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Customer Success Stories</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              Hear from organizations that have transformed their business with Nexus
            </p>
          </div>
          
          <Suspense fallback={<div className="h-64 bg-secondary-100 rounded-lg animate-pulse"></div>}>
            <TestimonialCarousel testimonials={testimonials} />
          </Suspense>
        </div>
      </section>

      {/* Technical Specifications */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Technical Specifications</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              Enterprise-grade platform built for scale and reliability
            </p>
          </div>
          
          <Suspense fallback={<div className="h-96 bg-secondary-100 rounded-lg animate-pulse"></div>}>
            <TechnicalSpecs />
          </Suspense>
        </div>
      </section>

      {/* Pricing Calculator */}
      <section id="pricing" className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Flexible Pricing</h2>
            <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
              Choose the plan that fits your organization's needs
            </p>
          </div>
          
          <Suspense fallback={<div className="h-96 bg-secondary-100 rounded-lg animate-pulse"></div>}>
            <PricingCalculator />
          </Suspense>
        </div>
      </section>

      {/* Enhanced CTA Section */}
      <section className="section-padding bg-gradient-to-br from-secondary-900 via-secondary-800 to-primary-900 text-white relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-[url('/images/circuit-pattern.svg')] opacity-10"></div>
        
        <div className="container relative">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Accelerate Your AI Journey?
            </h2>
            <p className="text-xl text-secondary-300 mb-8 max-w-2xl mx-auto">
              Join hundreds of organizations already transforming their business with Nexus. 
              Get started with a personalized demo and see results in weeks, not months.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4 bg-white text-secondary-900 hover:bg-secondary-100 shadow-lg">
                <Play className="w-5 h-5 mr-2" />
                Schedule Demo
              </a>
              <a href="/case-studies" className="btn-secondary text-lg px-8 py-4 bg-transparent border-white text-white hover:bg-white hover:text-secondary-900">
                View Case Studies
                <ArrowRight className="w-5 h-5 ml-2" />
              </a>
              <a href="/docs" className="text-white hover:text-secondary-300 font-medium text-lg flex items-center">
                <Download className="w-5 h-5 mr-2" />
                Download Whitepaper
              </a>
            </div>
            
            {/* Contact Options */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
              <div>
                <div className="bg-white bg-opacity-10 rounded-lg p-6">
                  <Smartphone className="w-8 h-8 mx-auto mb-3 text-primary-400" />
                  <h3 className="font-semibold mb-2">Call Sales</h3>
                  <p className="text-secondary-300 text-sm">1-800-AIC-NEXUS</p>
                </div>
              </div>
              <div>
                <div className="bg-white bg-opacity-10 rounded-lg p-6">
                  <Users className="w-8 h-8 mx-auto mb-3 text-primary-400" />
                  <h3 className="font-semibold mb-2">Expert Consultation</h3>
                  <p className="text-secondary-300 text-sm">Free 30-min session</p>
                </div>
              </div>
              <div>
                <div className="bg-white bg-opacity-10 rounded-lg p-6">
                  <Clock className="w-8 h-8 mx-auto mb-3 text-primary-400" />
                  <h3 className="font-semibold mb-2">24/7 Support</h3>
                  <p className="text-secondary-300 text-sm">Enterprise customers</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
