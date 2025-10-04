'use client';

import React from 'react';
import { useClient } from '../../../contexts/ClientContext';
import OverviewCards from './OverviewCards';
import ProjectProgress from './ProjectProgress';
import RecentActivity from './RecentActivity';
import QuickActions from './QuickActions';

const ClientDashboard = () => {
  const { projects, agents, workflows } = useClient();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Welcome back! Here's what's happening with your projects.
        </div>
      </div>

      <OverviewCards projects={projects} agents={agents} workflows={workflows} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ProjectProgress projects={projects} />
        <QuickActions />
      </div>

      <RecentActivity />
    </div>
  );
};

export default ClientDashboard;
