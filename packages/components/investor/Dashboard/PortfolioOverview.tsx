import React from 'react';
import { CompanyMetrics } from '../../../types/investor';

interface PortfolioOverviewProps {
  metrics: CompanyMetrics;
}

const PortfolioOverview: React.FC<PortfolioOverviewProps> = ({ metrics }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Portfolio Overview</h3>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-600">Total Investment</span>
          <span className="text-sm font-semibold text-gray-900">
            ${(metrics.totalFunding / 1000000).toFixed(1)}M
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-600">Current Valuation</span>
          <span className="text-sm font-semibold text-gray-900">
            ${(metrics.valuation / 1000000).toFixed(0)}M
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-600">Funding Rounds</span>
          <span className="text-sm font-semibold text-gray-900">
            {metrics.fundingRounds.length}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-600">Gross Margin</span>
          <span className="text-sm font-semibold text-green-600">
            {metrics.keyMetrics.grossMargin}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default PortfolioOverview;
