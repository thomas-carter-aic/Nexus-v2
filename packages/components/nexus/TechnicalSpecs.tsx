'use client';

import { useState } from 'react';
import { 
  Code, Database, Cloud, Shield, Zap, Globe, 
  Server, Lock, CheckCircle, ArrowRight, Download,
  Monitor, Cpu, HardDrive, Network
} from 'lucide-react';

interface TechSpec {
  category: string;
  icon: React.ReactNode;
  specs: {
    name: string;
    value: string;
    description?: string;
  }[];
}

interface Integration {
  name: string;
  category: string;
  logo: string;
  description: string;
  status: 'available' | 'coming-soon' | 'beta';
}

const technicalSpecs: TechSpec[] = [
  {
    category: 'Infrastructure',
    icon: <Server className="w-6 h-6" />,
    specs: [
      { name: 'Cloud Providers', value: 'AWS, Azure, GCP', description: 'Multi-cloud deployment support' },
      { name: 'Regions', value: '15+ Global', description: 'Low-latency worldwide coverage' },
      { name: 'Uptime SLA', value: '99.9%', description: 'Enterprise-grade reliability' },
      { name: 'Auto-scaling', value: '0-1000+ instances', description: 'Elastic resource management' },
      { name: 'Load Balancing', value: 'Built-in', description: 'Automatic traffic distribution' },
      { name: 'CDN', value: 'Global Edge Network', description: 'Optimized content delivery' }
    ]
  },
  {
    category: 'Performance',
    icon: <Zap className="w-6 h-6" />,
    specs: [
      { name: 'API Response Time', value: '<100ms', description: 'P95 latency globally' },
      { name: 'Throughput', value: '10M+ requests/min', description: 'High-volume processing' },
      { name: 'Concurrent Users', value: '100K+', description: 'Massive scale support' },
      { name: 'Data Processing', value: '1TB+/hour', description: 'Real-time analytics' },
      { name: 'Model Inference', value: '<50ms', description: 'Ultra-fast AI responses' },
      { name: 'Batch Processing', value: '1M+ records/min', description: 'Bulk operations' }
    ]
  },
  {
    category: 'Security',
    icon: <Shield className="w-6 h-6" />,
    specs: [
      { name: 'Encryption', value: 'AES-256', description: 'Data at rest and in transit' },
      { name: 'Authentication', value: 'OAuth 2.0, SAML', description: 'Enterprise SSO support' },
      { name: 'Compliance', value: 'SOC2, GDPR, HIPAA', description: 'Industry certifications' },
      { name: 'Access Control', value: 'RBAC', description: 'Role-based permissions' },
      { name: 'Audit Logging', value: 'Complete', description: 'Full activity tracking' },
      { name: 'Vulnerability Scanning', value: 'Continuous', description: 'Automated security monitoring' }
    ]
  },
  {
    category: 'Development',
    icon: <Code className="w-6 h-6" />,
    specs: [
      { name: 'APIs', value: 'REST, GraphQL, WebSocket', description: 'Multiple interface options' },
      { name: 'SDKs', value: 'Python, JavaScript, Java, Go', description: 'Native language support' },
      { name: 'Webhooks', value: 'Real-time events', description: 'Event-driven integrations' },
      { name: 'Documentation', value: 'Interactive', description: 'Live API explorer' },
      { name: 'Testing', value: 'Sandbox environment', description: 'Safe development space' },
      { name: 'Versioning', value: 'Semantic', description: 'Backward compatibility' }
    ]
  },
  {
    category: 'Data & Storage',
    icon: <Database className="w-6 h-6" />,
    specs: [
      { name: 'Storage Types', value: 'Object, Block, File', description: 'Flexible storage options' },
      { name: 'Databases', value: 'SQL, NoSQL, Vector', description: 'Multi-database support' },
      { name: 'Backup', value: 'Automated daily', description: 'Point-in-time recovery' },
      { name: 'Replication', value: 'Multi-region', description: 'Data redundancy' },
      { name: 'Compression', value: 'Up to 90%', description: 'Efficient storage usage' },
      { name: 'Data Retention', value: 'Configurable', description: 'Compliance-ready policies' }
    ]
  },
  {
    category: 'Monitoring',
    icon: <Monitor className="w-6 h-6" />,
    specs: [
      { name: 'Metrics', value: '500+ built-in', description: 'Comprehensive observability' },
      { name: 'Alerting', value: 'Real-time', description: 'Proactive notifications' },
      { name: 'Dashboards', value: 'Customizable', description: 'Visual insights' },
      { name: 'Logging', value: 'Structured', description: 'Searchable log data' },
      { name: 'Tracing', value: 'Distributed', description: 'End-to-end visibility' },
      { name: 'Health Checks', value: 'Automated', description: 'Continuous monitoring' }
    ]
  }
];

const integrations: Integration[] = [
  { name: 'Salesforce', category: 'CRM', logo: '/api/placeholder/40/40', description: 'Customer data sync', status: 'available' },
  { name: 'Slack', category: 'Communication', logo: '/api/placeholder/40/40', description: 'Team notifications', status: 'available' },
  { name: 'AWS S3', category: 'Storage', logo: '/api/placeholder/40/40', description: 'Object storage', status: 'available' },
  { name: 'PostgreSQL', category: 'Database', logo: '/api/placeholder/40/40', description: 'Relational data', status: 'available' },
  { name: 'Stripe', category: 'Payments', logo: '/api/placeholder/40/40', description: 'Payment processing', status: 'available' },
  { name: 'Tableau', category: 'Analytics', logo: '/api/placeholder/40/40', description: 'Data visualization', status: 'available' },
  { name: 'Microsoft Teams', category: 'Communication', logo: '/api/placeholder/40/40', description: 'Team collaboration', status: 'beta' },
  { name: 'Snowflake', category: 'Data Warehouse', logo: '/api/placeholder/40/40', description: 'Data analytics', status: 'coming-soon' }
];

export function TechnicalSpecs() {
  const [selectedCategory, setSelectedCategory] = useState<string>('Infrastructure');
  const [showAllIntegrations, setShowAllIntegrations] = useState(false);

  const selectedSpecs = technicalSpecs.find(spec => spec.category === selectedCategory);
  const visibleIntegrations = showAllIntegrations ? integrations : integrations.slice(0, 6);

  const getStatusBadge = (status: Integration['status']) => {
    switch (status) {
      case 'available':
        return <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">Available</span>;
      case 'beta':
        return <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">Beta</span>;
      case 'coming-soon':
        return <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full">Coming Soon</span>;
    }
  };

  return (
    <section className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Technical Specifications
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Enterprise-grade infrastructure built for scale, security, and performance
          </p>
        </div>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Category Navigation */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-8">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Categories</h3>
              <nav className="space-y-2">
                {technicalSpecs.map((spec) => (
                  <button
                    key={spec.category}
                    onClick={() => setSelectedCategory(spec.category)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors duration-200 ${
                      selectedCategory === spec.category
                        ? 'bg-blue-50 text-blue-700 border border-blue-200'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <div className={`p-1 rounded ${
                      selectedCategory === spec.category ? 'text-blue-600' : 'text-gray-400'
                    }`}>
                      {spec.icon}
                    </div>
                    <span className="font-medium">{spec.category}</span>
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Specifications Display */}
          <div className="lg:col-span-3">
            {selectedSpecs && (
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <div className="flex items-center gap-3 mb-8">
                  <div className="p-3 bg-blue-100 rounded-lg text-blue-600">
                    {selectedSpecs.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">{selectedSpecs.category}</h3>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  {selectedSpecs.specs.map((spec, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-6 hover:border-blue-300 transition-colors duration-200">
                      <div className="flex items-start justify-between mb-3">
                        <h4 className="font-semibold text-gray-900">{spec.name}</h4>
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                      </div>
                      <div className="text-2xl font-bold text-blue-600 mb-2">
                        {spec.value}
                      </div>
                      {spec.description && (
                        <p className="text-sm text-gray-600">{spec.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Integrations Section */}
        <div className="mt-24">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              Integrations & Ecosystem
            </h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Connect with your existing tools and services seamlessly
            </p>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-8">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {visibleIntegrations.map((integration, index) => (
                <div key={index} className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition-colors duration-200">
                  <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                    <div className="w-6 h-6 bg-gray-300 rounded"></div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-semibold text-gray-900">{integration.name}</h4>
                      {getStatusBadge(integration.status)}
                    </div>
                    <p className="text-sm text-gray-600">{integration.description}</p>
                    <p className="text-xs text-gray-500 mt-1">{integration.category}</p>
                  </div>
                </div>
              ))}
            </div>

            {!showAllIntegrations && integrations.length > 6 && (
              <div className="text-center mt-8">
                <button
                  onClick={() => setShowAllIntegrations(true)}
                  className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium"
                >
                  View All Integrations
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Architecture Diagram */}
        <div className="mt-24">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              System Architecture
            </h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Built on modern, scalable architecture principles
            </p>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-8">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Globe className="w-8 h-8 text-blue-600" />
                </div>
                <h4 className="text-lg font-bold text-gray-900 mb-2">Edge Layer</h4>
                <p className="text-gray-600 text-sm">
                  Global CDN and edge computing for optimal performance
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Cpu className="w-8 h-8 text-green-600" />
                </div>
                <h4 className="text-lg font-bold text-gray-900 mb-2">Processing Layer</h4>
                <p className="text-gray-600 text-sm">
                  Auto-scaling compute resources with intelligent load balancing
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <HardDrive className="w-8 h-8 text-purple-600" />
                </div>
                <h4 className="text-lg font-bold text-gray-900 mb-2">Data Layer</h4>
                <p className="text-gray-600 text-sm">
                  Multi-database support with automated backup and replication
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Download Resources */}
        <div className="mt-16 text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-4">
              Need More Technical Details?
            </h3>
            <p className="text-lg mb-6 opacity-90">
              Download our comprehensive technical documentation and architecture guides
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="inline-flex items-center gap-2 bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                <Download className="w-5 h-5" />
                Technical Whitepaper
              </button>
              <button className="inline-flex items-center gap-2 border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors duration-200">
                <Code className="w-5 h-5" />
                API Documentation
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
