import React from 'react';
import { ActivityLog } from '../../../types';
import { formatDistanceToNow } from 'date-fns';

interface RecentActivityProps {
  logs: ActivityLog[];
}

const RecentActivity: React.FC<RecentActivityProps> = ({ logs }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
      <div className="space-y-4">
        {logs.slice(0, 10).map((log) => (
          <div key={log.id} className="flex items-start space-x-3">
            <div className="w-2 h-2 bg-blue-400 rounded-full mt-2"></div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">
                {log.action} - {log.resource}
              </p>
              <p className="text-sm text-gray-500">{log.details}</p>
              <div className="flex items-center mt-1 text-xs text-gray-400">
                <span>{log.user}</span>
                <span className="mx-2">•</span>
                <span>{formatDistanceToNow(log.timestamp, { addSuffix: true })}</span>
                <span className="mx-2">•</span>
                <span>{log.ipAddress}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentActivity;
