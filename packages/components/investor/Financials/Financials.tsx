'use client';

import React, { useState } from 'react';
import { useInvestor } from '../../../contexts/InvestorContext';
import { DollarSign, TrendingUp, TrendingDown, BarChart3, Calendar } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const Financials = () => {
  const { financialData, companyMetrics } = useInvestor();
  const [selectedPeriod, setSelectedPeriod] = useState('quarterly');
  const [activeTab, setActiveTab] = useState('overview');

  const latestData = financialData[0];
  const previousData = financialData[1];

  const getChangePercentage = (current: number, previous: number) => {
    if (!previous) return 0;
    return ((current - previous) / previous) * 100;
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatPercentage = (value: number) => {
    return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`;
  };

  const revenueData = financialData.map(data => ({
    period: data.period,
    revenue: data.revenue / 1000000,
    expenses: data.expenses / 1000000,
    netIncome: data.netIncome / 1000000,
  })).reverse();

  const metricsData = financialData.map(data => ({
    period: data.period,
    arr: data.arr / 1000000,
    mrr: data.mrr / 1000,
    customers: data.customerCount,
    growthRate: data.growthRate,
  })).reverse();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Financial Reports</h1>
        <div className="flex items-center space-x-4">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="quarterly">Quarterly</option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Revenue</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(latestData.revenue)}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center">
            <span className={`text-sm font-medium ${
              getChangePercentage(latestData.revenue, previousData?.revenue) >= 0 
                ? 'text-green-600' 
                : 'text-red-600'
            }`}>
              {formatPercentage(getChangePercentage(latestData.revenue, previousData?.revenue))}
            </span>
            <span className="text-sm text-gray-500 ml-2">from last period</span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Net Income</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(latestData.netIncome)}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center">
            <span className={`text-sm font-medium ${
              getChangePercentage(latestData.netIncome, previousData?.netIncome) >= 0 
                ? 'text-green-600' 
                : 'text-red-600'
            }`}>
              {formatPercentage(getChangePercentage(latestData.netIncome, previousData?.netIncome))}
            </span>
            <span className="text-sm text-gray-500 ml-2">from last period</span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">ARR</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(latestData.arr)}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <BarChart3 className="h-6 w-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center">
            <span className="text-sm font-medium text-green-600">
              {formatPercentage(latestData.growthRate)}
            </span>
            <span className="text-sm text-gray-500 ml-2">growth rate</span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Cash Runway</p>
              <p className="text-2xl font-bold text-gray-900">{latestData.runway}m</p>
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <Calendar className="h-6 w-6 text-orange-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center">
            <span className="text-sm font-medium text-gray-600">
              Burn: {formatCurrency(latestData.burnRate)}/mo
            </span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('overview')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'overview'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Revenue Overview
            </button>
            <button
              onClick={() => setActiveTab('metrics')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'metrics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Key Metrics
            </button>
            <button
              onClick={() => setActiveTab('details')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'details'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Detailed Breakdown
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Revenue vs Expenses</h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={revenueData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="period" />
                      <YAxis tickFormatter={(value) => `$${value}M`} />
                      <Tooltip formatter={(value) => [`$${value}M`, '']} />
                      <Line 
                        type="monotone" 
                        dataKey="revenue" 
                        stroke="#3b82f6" 
                        strokeWidth={3}
                        name="Revenue"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="expenses" 
                        stroke="#ef4444" 
                        strokeWidth={3}
                        name="Expenses"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="netIncome" 
                        stroke="#10b981" 
                        strokeWidth={3}
                        name="Net Income"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'metrics' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">ARR Growth & Customer Acquisition</h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={metricsData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="period" />
                      <YAxis yAxisId="left" tickFormatter={(value) => `$${value}M`} />
                      <YAxis yAxisId="right" orientation="right" />
                      <Tooltip />
                      <Bar yAxisId="left" dataKey="arr" fill="#3b82f6" name="ARR ($M)" />
                      <Line yAxisId="right" type="monotone" dataKey="customers" stroke="#10b981" name="Customers" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'details' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-medium text-gray-900">Financial Health</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Gross Margin</span>
                      <span className="font-medium">{companyMetrics.keyMetrics.grossMargin}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Net Margin</span>
                      <span className="font-medium">{companyMetrics.keyMetrics.netMargin}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Customer LTV</span>
                      <span className="font-medium">{formatCurrency(companyMetrics.keyMetrics.lifetimeValue)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Customer CAC</span>
                      <span className="font-medium">{formatCurrency(companyMetrics.keyMetrics.customerAcquisitionCost)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">LTV/CAC Ratio</span>
                      <span className="font-medium">
                        {(companyMetrics.keyMetrics.lifetimeValue / companyMetrics.keyMetrics.customerAcquisitionCost).toFixed(1)}x
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Churn Rate</span>
                      <span className="font-medium">{companyMetrics.keyMetrics.churnRate}%</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-medium text-gray-900">Latest Period Details</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Revenue</span>
                      <span className="font-medium">{formatCurrency(latestData.revenue)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Expenses</span>
                      <span className="font-medium">{formatCurrency(latestData.expenses)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Net Income</span>
                      <span className="font-medium">{formatCurrency(latestData.netIncome)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Cash Flow</span>
                      <span className="font-medium">{formatCurrency(latestData.cashFlow)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">MRR</span>
                      <span className="font-medium">{formatCurrency(latestData.mrr)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">ARR</span>
                      <span className="font-medium">{formatCurrency(latestData.arr)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Financials;
