import React from 'react';
import { formatDistanceToNow } from 'date-fns';

const RecentActivity = () => {
  // Mock recent activity data
  const activities = [
    {
      id: '1',
      action: 'Project Updated',
      description: 'Customer Service AI Implementation progress updated to 65%',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      type: 'project'
    },
    {
      id: '2',
      action: 'Agent Deployed',
      description: 'Customer Support Bot successfully deployed to production',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
      type: 'agent'
    },
    {
      id: '3',
      action: 'Workflow Executed',
      description: 'Lead Qualification Process completed 25 new leads',
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
      type: 'workflow'
    },
    {
      id: '4',
      action: 'Support Ticket',
      description: 'New support ticket created for response time optimization',
      timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000), // 8 hours ago
      type: 'support'
    }
  ];

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'project': return 'bg-blue-400';
      case 'agent': return 'bg-green-400';
      case 'workflow': return 'bg-purple-400';
      case 'support': return 'bg-orange-400';
      default: return 'bg-gray-400';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
      <div className="space-y-4">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-start space-x-3">
            <div className={`w-2 h-2 rounded-full mt-2 ${getActivityColor(activity.type)}`}></div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">{activity.action}</p>
              <p className="text-sm text-gray-500">{activity.description}</p>
              <p className="text-xs text-gray-400 mt-1">
                {formatDistanceToNow(activity.timestamp, { addSuffix: true })}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentActivity;
