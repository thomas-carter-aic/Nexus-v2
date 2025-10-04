'use client';

import React from 'react';
import { useInvestor } from '../../../contexts/InvestorContext';
import KeyMetrics from './KeyMetrics';
import PortfolioOverview from './PortfolioOverview';
import RecentUpdates from './RecentUpdates';
import InvestmentProgress from './InvestmentProgress';

const InvestorDashboard = () => {
  const { financialData, companyMetrics, updates } = useInvestor();
  const latestFinancials = financialData[0];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Investor Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date().toLocaleDateString()}
        </div>
      </div>

      <KeyMetrics financials={latestFinancials} metrics={companyMetrics} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PortfolioOverview metrics={companyMetrics} />
        <InvestmentProgress financials={latestFinancials} />
      </div>

      <RecentUpdates updates={updates} />
    </div>
  );
};

export default InvestorDashboard;
