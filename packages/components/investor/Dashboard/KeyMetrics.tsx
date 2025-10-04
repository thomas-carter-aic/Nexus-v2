import React from 'react';
import { DollarSign, TrendingUp, Users, Target } from 'lucide-react';
import { FinancialData, CompanyMetrics } from '../../../types/investor';

interface KeyMetricsProps {
  financials: FinancialData;
  metrics: CompanyMetrics;
}

const KeyMetrics: React.FC<KeyMetricsProps> = ({ financials, metrics }) => {
  const cards = [
    {
      title: 'ARR',
      value: `$${(financials.arr / 1000000).toFixed(1)}M`,
      icon: DollarSign,
      color: 'blue',
      change: `+${financials.growthRate}%`
    },
    {
      title: 'Growth Rate',
      value: `${financials.growthRate}%`,
      icon: TrendingUp,
      color: 'green',
      change: 'YoY'
    },
    {
      title: 'Customers',
      value: financials.customerCount.toString(),
      icon: Users,
      color: 'purple',
      change: '+12 this month'
    },
    {
      title: 'Valuation',
      value: `$${(metrics.valuation / 1000000).toFixed(0)}M`,
      icon: Target,
      color: 'orange',
      change: 'Current'
    }
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-50 text-blue-600',
      green: 'bg-green-50 text-green-600',
      purple: 'bg-purple-50 text-purple-600',
      orange: 'bg-orange-50 text-orange-600'
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{card.title}</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{card.value}</p>
            </div>
            <div className={`p-3 rounded-lg ${getColorClasses(card.color)}`}>
              <card.icon className="h-6 w-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center">
            <span className="text-sm font-medium text-green-600">{card.change}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default KeyMetrics;
