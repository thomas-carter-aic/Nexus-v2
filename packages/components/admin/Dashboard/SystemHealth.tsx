import React from 'react';
import { SystemMetrics } from '../../../types';

interface SystemHealthProps {
  metrics: SystemMetrics;
}

const SystemHealth: React.FC<SystemHealthProps> = ({ metrics }) => {
  const healthItems = [
    { label: 'Response Time', value: `${metrics.responseTime}s`, status: 'good' },
    { label: 'Error Rate', value: `${metrics.errorRate}%`, status: 'good' },
    { label: 'Uptime', value: `${metrics.uptime}%`, status: 'excellent' },
    { label: 'System Load', value: `${metrics.systemLoad}%`, status: 'good' }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'text-green-600 bg-green-50';
      case 'good': return 'text-blue-600 bg-blue-50';
      case 'warning': return 'text-yellow-600 bg-yellow-50';
      case 'critical': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">System Health</h3>
      <div className="space-y-4">
        {healthItems.map((item, index) => (
          <div key={index} className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600">{item.label}</span>
            <div className="flex items-center space-x-2">
              <span className="text-sm font-semibold text-gray-900">{item.value}</span>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(item.status)}`}>
                {item.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SystemHealth;
