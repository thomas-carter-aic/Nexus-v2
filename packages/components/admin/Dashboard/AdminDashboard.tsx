'use client';

import React from 'react';
import { useAdmin } from '../../../contexts/AdminContext';
import MetricsCards from './MetricsCards';
import SystemHealth from './SystemHealth';
import RecentActivity from './RecentActivity';
import QuickActions from './QuickActions';

const AdminDashboard = () => {
  const { systemMetrics, activityLogs } = useAdmin();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date().toLocaleString()}
        </div>
      </div>

      <MetricsCards metrics={systemMetrics} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SystemHealth metrics={systemMetrics} />
        <QuickActions />
      </div>

      <RecentActivity logs={activityLogs} />
    </div>
  );
};

export default AdminDashboard;
