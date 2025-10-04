'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { User, Agent, Workflow, SystemMetrics, ActivityLog } from '../types';

interface AdminContextType {
  // Current user
  currentUser: User | null;
  setCurrentUser: (user: User | null) => void;
  
  // Data states
  users: User[];
  agents: Agent[];
  workflows: Workflow[];
  systemMetrics: SystemMetrics;
  activityLogs: ActivityLog[];
  
  // Loading states
  loading: boolean;
  setLoading: (loading: boolean) => void;
  
  // Actions
  refreshData: () => void;
  updateUser: (user: User) => void;
  updateAgent: (agent: Agent) => void;
  updateWorkflow: (workflow: Workflow) => void;
}

const AdminContext = createContext<AdminContextType | undefined>(undefined);

// Mock data
const mockUsers: User[] = [
  {
    id: '1',
    email: 'admin@appliedinnovation.com',
    name: 'System Administrator',
    role: 'admin',
    status: 'active',
    createdAt: new Date('2024-01-15T10:00:00Z'),
    lastLogin: new Date('2024-01-20T14:30:00Z')
  },
  {
    id: '2',
    email: 'john.doe@company.com',
    name: 'John Doe',
    role: 'client',
    status: 'active',
    createdAt: new Date('2024-01-16T09:15:00Z'),
    lastLogin: new Date('2024-01-20T11:45:00Z')
  }
];

const mockAgents: Agent[] = [
  {
    id: '1',
    name: 'Customer Support Agent',
    type: 'chatbot',
    status: 'active',
    description: 'AI-powered customer support chatbot',
    capabilities: ['natural_language', 'context_awareness', 'multi_turn'],
    createdAt: new Date('2024-01-10T08:00:00Z'),
    lastUsed: new Date('2024-01-20T15:30:00Z'),
    usage: {
      totalInteractions: 1250,
      successRate: 98.5,
      avgResponseTime: 1.2
    }
  },
  {
    id: '2',
    name: 'Data Analysis Agent',
    type: 'analytics',
    status: 'active',
    description: 'Advanced data analysis and reporting agent',
    capabilities: ['data_analysis', 'visualization', 'reporting'],
    createdAt: new Date('2024-01-12T10:30:00Z'),
    lastUsed: new Date('2024-01-20T13:15:00Z'),
    usage: {
      totalInteractions: 890,
      successRate: 96.2,
      avgResponseTime: 2.8
    }
  }
];

const mockWorkflows: Workflow[] = [
  {
    id: '1',
    name: 'Customer Onboarding',
    description: 'Automated customer onboarding process with AI assistance',
    status: 'active',
    type: 'automation',
    steps: [
      { id: '1', name: 'Welcome Email', type: 'notification', config: {}, order: 1 },
      { id: '2', name: 'Document Processing', type: 'action', config: {}, order: 2 },
      { id: '3', name: 'Account Setup', type: 'action', config: {}, order: 3 }
    ],
    createdAt: new Date('2024-01-08T12:00:00Z'),
    lastRun: new Date('2024-01-18T16:45:00Z'),
    runCount: 156,
    successRate: 94.2
  }
];

const mockSystemMetrics: SystemMetrics = {
  uptime: 99.8,
  responseTime: 1.2,
  errorRate: 0.8,
  activeUsers: 1247,
  totalRequests: 15420,
  systemLoad: 45
};

const mockActivityLogs: ActivityLog[] = [
  {
    id: '1',
    timestamp: new Date('2024-01-20T15:30:00Z'),
    user: 'admin@appliedinnovation.com',
    action: 'User Login',
    resource: 'Authentication',
    details: 'Successful login from Chrome browser',
    ipAddress: '192.168.1.100'
  },
  {
    id: '2',
    timestamp: new Date('2024-01-20T14:15:00Z'),
    user: 'admin@appliedinnovation.com',
    action: 'Agent Updated',
    resource: 'Agent/customer-support',
    details: 'Updated model and capabilities',
    ipAddress: '192.168.1.100'
  }
];

export const AdminProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(mockUsers[0]);
  const [users] = useState<User[]>(mockUsers);
  const [agents] = useState<Agent[]>(mockAgents);
  const [workflows] = useState<Workflow[]>(mockWorkflows);
  const [systemMetrics] = useState<SystemMetrics>(mockSystemMetrics);
  const [activityLogs] = useState<ActivityLog[]>(mockActivityLogs);
  const [loading, setLoading] = useState(false);

  const refreshData = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  const updateUser = (user: User) => {
    // Implementation for updating user
    console.log('Updating user:', user);
  };

  const updateAgent = (agent: Agent) => {
    // Implementation for updating agent
    console.log('Updating agent:', agent);
  };

  const updateWorkflow = (workflow: Workflow) => {
    // Implementation for updating workflow
    console.log('Updating workflow:', workflow);
  };

  const value: AdminContextType = {
    currentUser,
    setCurrentUser,
    users,
    agents,
    workflows,
    systemMetrics,
    activityLogs,
    loading,
    setLoading,
    refreshData,
    updateUser,
    updateAgent,
    updateWorkflow
  };

  return (
    <AdminContext.Provider value={value}>
      {children}
    </AdminContext.Provider>
  );
};

export const useAdmin = () => {
  const context = useContext(AdminContext);
  if (context === undefined) {
    throw new Error('useAdmin must be used within an AdminProvider');
  }
  return context;
};
