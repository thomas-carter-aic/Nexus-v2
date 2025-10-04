import React from 'react';
import { Plus, MessageSquare, BarChart3, Settings } from 'lucide-react';

const QuickActions = () => {
  const actions = [
    { label: 'New Project', icon: Plus, color: 'blue', href: '/client/projects' },
    { label: 'Contact Support', icon: MessageSquare, color: 'green', href: '/client/support' },
    { label: 'View Analytics', icon: BarChart3, color: 'purple', href: '/client/analytics' },
    { label: 'Account Settings', icon: Settings, color: 'gray', href: '/client/settings' }
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-600 hover:bg-blue-700',
      green: 'bg-green-600 hover:bg-green-700',
      purple: 'bg-purple-600 hover:bg-purple-700',
      gray: 'bg-gray-600 hover:bg-gray-700'
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
            onClick={() => window.location.href = action.href}
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
