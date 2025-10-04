'use client';

import { useState } from 'react';
import { CheckCircle, X, Star, Zap, Shield, Clock } from 'lucide-react';

interface ComparisonFeature {
  category: string;
  features: {
    name: string;
    description: string;
    traditional: boolean | string;
    nexus: boolean | string;
    highlight?: boolean;
  }[];
}

const comparisonData: ComparisonFeature[] = [
  {
    category: 'Development Speed',
    features: [
      {
        name: 'Time to Deploy',
        description: 'From concept to production',
        traditional: '6-12 months',
        nexus: '2-4 weeks',
        highlight: true
      },
      {
        name: 'Pre-built Components',
        description: 'Ready-to-use AI modules',
        traditional: false,
        nexus: true
      },
      {
        name: 'Code Generation',
        description: 'Automated code scaffolding',
        traditional: false,
        nexus: true
      },
      {
        name: 'Integration Complexity',
        description: 'Effort required for system integration',
        traditional: 'High',
        nexus: 'Low'
      }
    ]
  },
  {
    category: 'Scalability & Performance',
    features: [
      {
        name: 'Auto-scaling',
        description: 'Automatic resource adjustment',
        traditional: 'Manual',
        nexus: 'Automatic',
        highlight: true
      },
      {
        name: 'Load Balancing',
        description: 'Traffic distribution',
        traditional: 'Custom setup',
        nexus: 'Built-in'
      },
      {
        name: 'Performance Monitoring',
        description: 'Real-time system insights',
        traditional: 'Basic',
        nexus: 'Advanced'
      },
      {
        name: 'Multi-region Support',
        description: 'Global deployment capability',
        traditional: false,
        nexus: true
      }
    ]
  },
  {
    category: 'Security & Compliance',
    features: [
      {
        name: 'Enterprise Security',
        description: 'Built-in security protocols',
        traditional: 'Custom implementation',
        nexus: 'Enterprise-grade',
        highlight: true
      },
      {
        name: 'Compliance Frameworks',
        description: 'SOC2, GDPR, HIPAA support',
        traditional: 'Manual compliance',
        nexus: 'Automated compliance'
      },
      {
        name: 'Data Encryption',
        description: 'End-to-end encryption',
        traditional: 'Basic',
        nexus: 'Advanced'
      },
      {
        name: 'Access Controls',
        description: 'Role-based permissions',
        traditional: 'Limited',
        nexus: 'Granular'
      }
    ]
  },
  {
    category: 'Cost & Maintenance',
    features: [
      {
        name: 'Development Cost',
        description: 'Initial investment required',
        traditional: 'High',
        nexus: 'Low',
        highlight: true
      },
      {
        name: 'Maintenance Overhead',
        description: 'Ongoing maintenance effort',
        traditional: 'High',
        nexus: 'Minimal'
      },
      {
        name: 'Infrastructure Management',
        description: 'Server and resource management',
        traditional: 'Manual',
        nexus: 'Managed'
      },
      {
        name: 'Update Frequency',
        description: 'Feature and security updates',
        traditional: 'Quarterly',
        nexus: 'Continuous'
      }
    ]
  }
];

export function FeatureComparison() {
  const [selectedCategory, setSelectedCategory] = useState<string>(comparisonData[0].category);

  const selectedData = comparisonData.find(cat => cat.category === selectedCategory);

  const renderValue = (value: boolean | string, isNexus: boolean = false) => {
    if (typeof value === 'boolean') {
      return value ? (
        <div className={`flex items-center gap-2 ${isNexus ? 'text-green-600' : 'text-gray-600'}`}>
          <CheckCircle className="w-5 h-5" />
          <span>Yes</span>
        </div>
      ) : (
        <div className="flex items-center gap-2 text-gray-400">
          <X className="w-5 h-5" />
          <span>No</span>
        </div>
      );
    }
    
    return (
      <span className={`font-medium ${
        isNexus ? 'text-blue-600' : 'text-gray-600'
      }`}>
        {value}
      </span>
    );
  };

  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Why Choose Nexus?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            See how Nexus compares to traditional AI development approaches
          </p>
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap justify-center gap-2 mb-12">
          {comparisonData.map((category) => (
            <button
              key={category.category}
              onClick={() => setSelectedCategory(category.category)}
              className={`px-6 py-3 rounded-full font-medium transition-all duration-300 ${
                selectedCategory === category.category
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {category.category}
            </button>
          ))}
        </div>

        {/* Comparison Table */}
        {selectedData && (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-6 py-4 text-left">
                      <div className="font-bold text-gray-900">Feature</div>
                    </th>
                    <th className="px-6 py-4 text-center">
                      <div className="font-bold text-gray-600">Traditional Approach</div>
                    </th>
                    <th className="px-6 py-4 text-center">
                      <div className="flex items-center justify-center gap-2 font-bold text-blue-600">
                        <Star className="w-5 h-5" />
                        Nexus Platform
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {selectedData.features.map((feature, index) => (
                    <tr 
                      key={feature.name}
                      className={`border-t border-gray-100 ${
                        feature.highlight ? 'bg-blue-50' : ''
                      } hover:bg-gray-50 transition-colors duration-200`}
                    >
                      <td className="px-6 py-6">
                        <div className="flex items-start gap-3">
                          {feature.highlight && (
                            <Zap className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
                          )}
                          <div>
                            <div className="font-semibold text-gray-900 mb-1">
                              {feature.name}
                            </div>
                            <div className="text-sm text-gray-600">
                              {feature.description}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-6 text-center">
                        {renderValue(feature.traditional)}
                      </td>
                      <td className="px-6 py-6 text-center">
                        {renderValue(feature.nexus, true)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Bottom CTA */}
        <div className="mt-16 text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
            <div className="max-w-3xl mx-auto">
              <h3 className="text-2xl font-bold mb-4">
                Ready to Experience the Difference?
              </h3>
              <p className="text-lg mb-6 opacity-90">
                Join hundreds of companies already accelerating their AI initiatives with Nexus
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                  Start Free Trial
                </button>
                <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors duration-200">
                  Schedule Demo
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
