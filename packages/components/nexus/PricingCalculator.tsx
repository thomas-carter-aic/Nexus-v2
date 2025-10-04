'use client';

import { useState } from 'react';
import { Check, X, Zap, Shield, Crown, Calculator, Users, Database, Cloud } from 'lucide-react';

interface PricingTier {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  basePrice: number;
  features: {
    name: string;
    included: boolean;
    limit?: string;
  }[];
  popular?: boolean;
  enterprise?: boolean;
}

interface UsageInputs {
  users: number;
  apiCalls: number;
  dataStorage: number;
  computeHours: number;
}

const pricingTiers: PricingTier[] = [
  {
    id: 'starter',
    name: 'Starter',
    description: 'Perfect for small teams and proof of concepts',
    icon: <Zap className="w-6 h-6" />,
    basePrice: 99,
    features: [
      { name: 'Up to 5 team members', included: true },
      { name: 'Basic AI components', included: true },
      { name: 'API calls', included: true, limit: '10K/month' },
      { name: 'Data storage', included: true, limit: '10GB' },
      { name: 'Compute hours', included: true, limit: '50 hours/month' },
      { name: 'Email support', included: true },
      { name: 'Basic analytics', included: true },
      { name: 'Custom workflows', included: false },
      { name: 'Advanced security', included: false },
      { name: 'Priority support', included: false },
      { name: 'Custom integrations', included: false },
      { name: 'Dedicated account manager', included: false }
    ]
  },
  {
    id: 'professional',
    name: 'Professional',
    description: 'Ideal for growing teams and production workloads',
    icon: <Shield className="w-6 h-6" />,
    basePrice: 299,
    popular: true,
    features: [
      { name: 'Up to 25 team members', included: true },
      { name: 'Advanced AI components', included: true },
      { name: 'API calls', included: true, limit: '100K/month' },
      { name: 'Data storage', included: true, limit: '100GB' },
      { name: 'Compute hours', included: true, limit: '200 hours/month' },
      { name: 'Priority email & chat support', included: true },
      { name: 'Advanced analytics', included: true },
      { name: 'Custom workflows', included: true },
      { name: 'Advanced security', included: true },
      { name: 'Priority support', included: true },
      { name: 'Custom integrations', included: false },
      { name: 'Dedicated account manager', included: false }
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    description: 'For large organizations with custom requirements',
    icon: <Crown className="w-6 h-6" />,
    basePrice: 999,
    enterprise: true,
    features: [
      { name: 'Unlimited team members', included: true },
      { name: 'All AI components', included: true },
      { name: 'API calls', included: true, limit: 'Unlimited' },
      { name: 'Data storage', included: true, limit: '1TB+' },
      { name: 'Compute hours', included: true, limit: 'Unlimited' },
      { name: '24/7 phone & chat support', included: true },
      { name: 'Enterprise analytics', included: true },
      { name: 'Custom workflows', included: true },
      { name: 'Enterprise security', included: true },
      { name: 'Priority support', included: true },
      { name: 'Custom integrations', included: true },
      { name: 'Dedicated account manager', included: true }
    ]
  }
];

const usageRates = {
  users: { starter: 20, professional: 15, enterprise: 10 },
  apiCalls: { starter: 0.01, professional: 0.008, enterprise: 0.005 }, // per 1K calls
  dataStorage: { starter: 2, professional: 1.5, enterprise: 1 }, // per GB
  computeHours: { starter: 5, professional: 4, enterprise: 3 } // per hour
};

export function PricingCalculator() {
  const [selectedTier, setSelectedTier] = useState<string>('professional');
  const [usage, setUsage] = useState<UsageInputs>({
    users: 10,
    apiCalls: 50000,
    dataStorage: 50,
    computeHours: 100
  });
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');

  const calculatePrice = (tierId: string) => {
    const tier = pricingTiers.find(t => t.id === tierId);
    if (!tier) return 0;

    let totalPrice = tier.basePrice;
    const rates = usageRates;

    // Calculate overages based on tier limits
    const limits = {
      starter: { users: 5, apiCalls: 10000, dataStorage: 10, computeHours: 50 },
      professional: { users: 25, apiCalls: 100000, dataStorage: 100, computeHours: 200 },
      enterprise: { users: Infinity, apiCalls: Infinity, dataStorage: 1000, computeHours: Infinity }
    };

    const tierLimits = limits[tierId as keyof typeof limits];
    const tierRates = rates.users[tierId as keyof typeof rates.users];

    // Calculate additional costs
    if (usage.users > tierLimits.users) {
      totalPrice += (usage.users - tierLimits.users) * tierRates;
    }

    if (usage.apiCalls > tierLimits.apiCalls) {
      const extraCalls = Math.ceil((usage.apiCalls - tierLimits.apiCalls) / 1000);
      totalPrice += extraCalls * rates.apiCalls[tierId as keyof typeof rates.apiCalls];
    }

    if (usage.dataStorage > tierLimits.dataStorage) {
      totalPrice += (usage.dataStorage - tierLimits.dataStorage) * rates.dataStorage[tierId as keyof typeof rates.dataStorage];
    }

    if (usage.computeHours > tierLimits.computeHours) {
      totalPrice += (usage.computeHours - tierLimits.computeHours) * rates.computeHours[tierId as keyof typeof rates.computeHours];
    }

    // Apply annual discount
    if (billingCycle === 'annual') {
      totalPrice *= 0.8; // 20% discount
    }

    return totalPrice;
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Flexible Pricing for Every Scale
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Choose the plan that fits your needs. Scale up or down as your requirements change.
          </p>

          {/* Billing Toggle */}
          <div className="flex items-center justify-center gap-4 mb-12">
            <span className={`font-medium ${billingCycle === 'monthly' ? 'text-gray-900' : 'text-gray-500'}`}>
              Monthly
            </span>
            <button
              onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                billingCycle === 'annual' ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  billingCycle === 'annual' ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={`font-medium ${billingCycle === 'annual' ? 'text-gray-900' : 'text-gray-500'}`}>
              Annual
            </span>
            {billingCycle === 'annual' && (
              <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                Save 20%
              </span>
            )}
          </div>
        </div>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Usage Calculator */}
          <div className="lg:col-span-1">
            <div className="bg-gray-50 rounded-2xl p-6 sticky top-8">
              <div className="flex items-center gap-2 mb-6">
                <Calculator className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-bold text-gray-900">Usage Calculator</h3>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Team Members
                  </label>
                  <div className="relative">
                    <Users className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                      type="number"
                      min="1"
                      value={usage.users}
                      onChange={(e) => setUsage({...usage, users: parseInt(e.target.value) || 1})}
                      className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Calls/Month
                  </label>
                  <div className="relative">
                    <Zap className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                      type="number"
                      min="0"
                      step="1000"
                      value={usage.apiCalls}
                      onChange={(e) => setUsage({...usage, apiCalls: parseInt(e.target.value) || 0})}
                      className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Data Storage (GB)
                  </label>
                  <div className="relative">
                    <Database className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                      type="number"
                      min="0"
                      value={usage.dataStorage}
                      onChange={(e) => setUsage({...usage, dataStorage: parseInt(e.target.value) || 0})}
                      className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Compute Hours/Month
                  </label>
                  <div className="relative">
                    <Cloud className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                      type="number"
                      min="0"
                      value={usage.computeHours}
                      onChange={(e) => setUsage({...usage, computeHours: parseInt(e.target.value) || 0})}
                      className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Pricing Tiers */}
          <div className="lg:col-span-3 grid md:grid-cols-3 gap-6">
            {pricingTiers.map((tier) => {
              const calculatedPrice = calculatePrice(tier.id);
              const isSelected = selectedTier === tier.id;

              return (
                <div
                  key={tier.id}
                  className={`relative bg-white rounded-2xl shadow-lg border-2 transition-all duration-300 ${
                    tier.popular
                      ? 'border-blue-500 shadow-blue-100'
                      : isSelected
                      ? 'border-blue-300'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {tier.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <span className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                        Most Popular
                      </span>
                    </div>
                  )}

                  <div className="p-6">
                    <div className="flex items-center gap-3 mb-4">
                      <div className={`p-2 rounded-lg ${
                        tier.popular ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {tier.icon}
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-gray-900">{tier.name}</h3>
                        <p className="text-sm text-gray-600">{tier.description}</p>
                      </div>
                    </div>

                    <div className="mb-6">
                      <div className="flex items-baseline gap-1">
                        <span className="text-3xl font-bold text-gray-900">
                          {formatPrice(calculatedPrice)}
                        </span>
                        <span className="text-gray-600">
                          /{billingCycle === 'monthly' ? 'month' : 'year'}
                        </span>
                      </div>
                      {calculatedPrice !== tier.basePrice && (
                        <p className="text-sm text-gray-500 mt-1">
                          Base: {formatPrice(tier.basePrice)} + usage overages
                        </p>
                      )}
                    </div>

                    <ul className="space-y-3 mb-8">
                      {tier.features.map((feature, index) => (
                        <li key={index} className="flex items-start gap-3">
                          {feature.included ? (
                            <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                          ) : (
                            <X className="w-5 h-5 text-gray-300 flex-shrink-0 mt-0.5" />
                          )}
                          <div className={`text-sm ${feature.included ? 'text-gray-700' : 'text-gray-400'}`}>
                            {feature.name}
                            {feature.limit && (
                              <span className="text-gray-500"> ({feature.limit})</span>
                            )}
                          </div>
                        </li>
                      ))}
                    </ul>

                    <button
                      onClick={() => setSelectedTier(tier.id)}
                      className={`w-full py-3 px-4 rounded-lg font-semibold transition-colors duration-200 ${
                        tier.popular
                          ? 'bg-blue-600 text-white hover:bg-blue-700'
                          : isSelected
                          ? 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {tier.enterprise ? 'Contact Sales' : 'Get Started'}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-24 text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-8">
            Frequently Asked Questions
          </h3>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="text-left">
              <h4 className="font-semibold text-gray-900 mb-2">Can I change plans anytime?</h4>
              <p className="text-gray-600 text-sm">
                Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.
              </p>
            </div>
            <div className="text-left">
              <h4 className="font-semibold text-gray-900 mb-2">What happens if I exceed my limits?</h4>
              <p className="text-gray-600 text-sm">
                You'll be charged for overages at the rates shown. We'll notify you before you reach your limits.
              </p>
            </div>
            <div className="text-left">
              <h4 className="font-semibold text-gray-900 mb-2">Is there a free trial?</h4>
              <p className="text-gray-600 text-sm">
                Yes, we offer a 14-day free trial with full access to Professional features.
              </p>
            </div>
            <div className="text-left">
              <h4 className="font-semibold text-gray-900 mb-2">Do you offer custom enterprise plans?</h4>
              <p className="text-gray-600 text-sm">
                Yes, we can create custom plans for large organizations with specific requirements.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
