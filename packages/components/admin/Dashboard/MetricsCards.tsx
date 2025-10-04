import React from 'react';
import { Users, Bot, Workflow, Activity } from 'lucide-react';
import { SystemMetrics } from '../../../types';

interface MetricsCardsProps {
  metrics: SystemMetrics;
}

const MetricsCards: React.FC<MetricsCardsProps> = ({ metrics }) => {
  const cards = [
    {
      title: 'Active Users',
      value: metrics.activeUsers.toLocaleString(),
      icon: Users,
      color: 'blue',
      change: '+12%'
    },
    {
      title: 'System Load',
      value: `${metrics.systemLoad}%`,
      icon: Bot,
      color: 'green',
      change: '-3%'
    },
    {
      title: 'Uptime',
      value: `${metrics.uptime}%`,
      icon: Workflow,
      color: 'purple',
      change: '+0.1%'
    },
    {
      title: 'Total Requests',
      value: metrics.totalRequests.toLocaleString(),
      icon: Activity,
      color: 'orange',
      change: '+8%'
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
            <span className={`text-sm font-medium ${card.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
              {card.change}
            </span>
            <span className="text-sm text-gray-500 ml-2">from last month</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MetricsCards;
