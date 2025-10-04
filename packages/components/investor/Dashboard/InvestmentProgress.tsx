import React from 'react';
import { FinancialData } from '../../../types/investor';

interface InvestmentProgressProps {
  financials: FinancialData;
}

const InvestmentProgress: React.FC<InvestmentProgressProps> = ({ financials }) => {
  const runwayMonths = Math.floor(financials.runway);
  const runwayProgress = Math.min((runwayMonths / 24) * 100, 100); // Assuming 24 months is full runway

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Financial Health</h3>
      <div className="space-y-4">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Cash Runway</span>
            <span className="text-sm font-semibold text-gray-900">{runwayMonths} months</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className={`h-2 rounded-full ${runwayMonths > 12 ? 'bg-green-600' : runwayMonths > 6 ? 'bg-yellow-600' : 'bg-red-600'}`}
              style={{ width: `${runwayProgress}%` }}
            ></div>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 pt-4">
          <div>
            <p className="text-sm font-medium text-gray-600">Monthly Burn</p>
            <p className="text-lg font-semibold text-gray-900">
              ${(financials.burnRate / 1000).toFixed(0)}K
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">Cash Flow</p>
            <p className={`text-lg font-semibold ${financials.cashFlow > 0 ? 'text-green-600' : 'text-red-600'}`}>
              ${(financials.cashFlow / 1000).toFixed(0)}K
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InvestmentProgress;
