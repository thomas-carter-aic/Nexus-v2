'use client';

import { useState, useEffect } from 'react';
import { Calculator, TrendingUp, DollarSign, Clock, Users, Zap } from 'lucide-react';

interface ROIInputs {
  teamSize: number;
  avgSalary: number;
  projectDuration: number;
  maintenanceCost: number;
  infrastructureCost: number;
}

interface ROIResults {
  traditionalCost: number;
  nexusCost: number;
  savings: number;
  roi: number;
  paybackPeriod: number;
  timeToMarket: number;
}

const defaultInputs: ROIInputs = {
  teamSize: 5,
  avgSalary: 120000,
  projectDuration: 8,
  maintenanceCost: 50000,
  infrastructureCost: 25000
};

export function ROICalculator() {
  const [inputs, setInputs] = useState<ROIInputs>(defaultInputs);
  const [results, setResults] = useState<ROIResults | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);

  const calculateROI = () => {
    setIsCalculating(true);
    
    // Simulate calculation delay for better UX
    setTimeout(() => {
      // Traditional approach costs
      const traditionalDevCost = (inputs.teamSize * inputs.avgSalary * inputs.projectDuration) / 12;
      const traditionalMaintenanceCost = inputs.maintenanceCost * 2; // Higher maintenance
      const traditionalInfraCost = inputs.infrastructureCost * 3; // Higher infrastructure
      const traditionalTotal = traditionalDevCost + traditionalMaintenanceCost + traditionalInfraCost;

      // Nexus approach costs
      const nexusLicenseCost = 50000; // Annual license
      const nexusDevCost = traditionalDevCost * 0.3; // 70% reduction in dev time
      const nexusMaintenanceCost = inputs.maintenanceCost * 0.5; // 50% reduction
      const nexusInfraCost = inputs.infrastructureCost; // Managed infrastructure
      const nexusTotal = nexusLicenseCost + nexusDevCost + nexusMaintenanceCost + nexusInfraCost;

      const savings = traditionalTotal - nexusTotal;
      const roi = (savings / nexusTotal) * 100;
      const paybackPeriod = nexusTotal / (savings / 12); // Months
      const timeToMarket = inputs.projectDuration * 0.25; // 75% faster

      setResults({
        traditionalCost: traditionalTotal,
        nexusCost: nexusTotal,
        savings,
        roi,
        paybackPeriod,
        timeToMarket
      });
      
      setIsCalculating(false);
    }, 1000);
  };

  useEffect(() => {
    calculateROI();
  }, [inputs]);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  return (
    <section className="py-24 bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            ROI Calculator
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Calculate your potential savings and return on investment with the Nexus platform
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Input Panel */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="flex items-center gap-3 mb-6">
              <Calculator className="w-6 h-6 text-blue-600" />
              <h3 className="text-2xl font-bold text-gray-900">Project Parameters</h3>
            </div>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Development Team Size
                </label>
                <div className="relative">
                  <Users className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={inputs.teamSize}
                    onChange={(e) => setInputs({...inputs, teamSize: parseInt(e.target.value) || 1})}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Number of developers on the project</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Average Developer Salary (Annual)
                </label>
                <div className="relative">
                  <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="number"
                    min="50000"
                    max="300000"
                    step="5000"
                    value={inputs.avgSalary}
                    onChange={(e) => setInputs({...inputs, avgSalary: parseInt(e.target.value) || 50000})}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Including benefits and overhead</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Duration (Months)
                </label>
                <div className="relative">
                  <Clock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="number"
                    min="1"
                    max="24"
                    value={inputs.projectDuration}
                    onChange={(e) => setInputs({...inputs, projectDuration: parseInt(e.target.value) || 1})}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Expected development timeline</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Annual Maintenance Cost
                </label>
                <div className="relative">
                  <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="number"
                    min="10000"
                    max="200000"
                    step="5000"
                    value={inputs.maintenanceCost}
                    onChange={(e) => setInputs({...inputs, maintenanceCost: parseInt(e.target.value) || 10000})}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Ongoing support and updates</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Annual Infrastructure Cost
                </label>
                <div className="relative">
                  <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="number"
                    min="5000"
                    max="100000"
                    step="2500"
                    value={inputs.infrastructureCost}
                    onChange={(e) => setInputs({...inputs, infrastructureCost: parseInt(e.target.value) || 5000})}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Cloud hosting and services</p>
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            {/* Cost Comparison */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <div className="flex items-center gap-3 mb-6">
                <TrendingUp className="w-6 h-6 text-green-600" />
                <h3 className="text-2xl font-bold text-gray-900">Cost Analysis</h3>
              </div>

              {isCalculating ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-3 text-gray-600">Calculating...</span>
                </div>
              ) : results ? (
                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-red-50 rounded-lg p-4">
                      <div className="text-sm text-red-600 font-medium mb-1">Traditional Approach</div>
                      <div className="text-2xl font-bold text-red-700">
                        {formatCurrency(results.traditionalCost)}
                      </div>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4">
                      <div className="text-sm text-green-600 font-medium mb-1">With Nexus</div>
                      <div className="text-2xl font-bold text-green-700">
                        {formatCurrency(results.nexusCost)}
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 rounded-lg p-6 text-center">
                    <div className="text-sm text-blue-600 font-medium mb-2">Total Savings</div>
                    <div className="text-3xl font-bold text-blue-700 mb-2">
                      {formatCurrency(results.savings)}
                    </div>
                    <div className="text-lg text-blue-600">
                      {formatPercentage(results.roi)} ROI
                    </div>
                  </div>
                </div>
              ) : null}
            </div>

            {/* Key Metrics */}
            {results && !isCalculating && (
              <div className="bg-white rounded-2xl shadow-xl p-8">
                <h4 className="text-xl font-bold text-gray-900 mb-6">Key Benefits</h4>
                <div className="grid grid-cols-2 gap-6">
                  <div className="text-center">
                    <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                      <Zap className="w-6 h-6 text-purple-600" />
                    </div>
                    <div className="text-2xl font-bold text-gray-900 mb-1">
                      {results.timeToMarket.toFixed(1)} months
                    </div>
                    <div className="text-sm text-gray-600">Time to Market</div>
                  </div>
                  <div className="text-center">
                    <div className="bg-orange-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                      <Clock className="w-6 h-6 text-orange-600" />
                    </div>
                    <div className="text-2xl font-bold text-gray-900 mb-1">
                      {results.paybackPeriod.toFixed(1)} months
                    </div>
                    <div className="text-sm text-gray-600">Payback Period</div>
                  </div>
                </div>
              </div>
            )}

            {/* CTA */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white text-center">
              <h4 className="text-xl font-bold mb-3">Ready to Start Saving?</h4>
              <p className="mb-4 opacity-90">
                Get a personalized ROI analysis for your specific use case
              </p>
              <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                Schedule Consultation
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
