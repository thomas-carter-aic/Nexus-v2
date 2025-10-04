import React from 'react';
import { InvestorUpdate } from '../../../types/investor';
import { formatDistanceToNow } from 'date-fns';

interface RecentUpdatesProps {
  updates: InvestorUpdate[];
}

const RecentUpdates: React.FC<RecentUpdatesProps> = ({ updates }) => {
  const getUpdateTypeColor = (type: string) => {
    switch (type) {
      case 'financial': return 'bg-blue-100 text-blue-800';
      case 'strategic': return 'bg-purple-100 text-purple-800';
      case 'operational': return 'bg-green-100 text-green-800';
      case 'milestone': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Updates</h3>
      <div className="space-y-4">
        {updates.slice(0, 5).map((update) => (
          <div key={update.id} className="border-b border-gray-100 pb-4 last:border-b-0">
            <div className="flex items-start justify-between mb-2">
              <h4 className="text-sm font-medium text-gray-900">{update.title}</h4>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getUpdateTypeColor(update.type)}`}>
                  {update.type}
                </span>
                <span className={`text-xs font-medium ${getPriorityColor(update.priority)}`}>
                  {update.priority}
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600 mb-2">{update.content}</p>
            <div className="flex items-center justify-between text-xs text-gray-400">
              <span>By {update.author}</span>
              <span>{formatDistanceToNow(update.publishDate, { addSuffix: true })}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentUpdates;
