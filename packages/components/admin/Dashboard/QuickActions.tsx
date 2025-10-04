import React from 'react';
import { Plus, RefreshCw, Settings, Download } from 'lucide-react';

const QuickActions = () => {
  const actions = [
    { label: 'Add New User', icon: Plus, color: 'blue' },
    { label: 'Refresh Data', icon: RefreshCw, color: 'green' },
    { label: 'System Settings', icon: Settings, color: 'gray' },
    { label: 'Export Logs', icon: Download, color: 'purple' }
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-600 hover:bg-blue-700',
      green: 'bg-green-600 hover:bg-green-700',
      gray: 'bg-gray-600 hover:bg-gray-700',
      purple: 'bg-purple-600 hover:bg-purple-700'
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
      <div className="grid grid-cols-2 gap-3">
        {actions.map((action, index) => (
          <button
            key={index}
            className={`flex items-center justify-center p-3 rounded-lg text-white transition-colors ${getColorClasses(action.color)}`}
          >
            <action.icon className="h-5 w-5 mr-2" />
            <span className="text-sm font-medium">{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default QuickActions;
