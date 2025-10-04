'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { User, Project, Agent, Workflow, Ticket, BillingInfo } from '../types';

interface ClientContextType {
  // Current user
  currentUser: User | null;
  setCurrentUser: (user: User | null) => void;
  
  // Data states
  projects: Project[];
  agents: Agent[];
  workflows: Workflow[];
  tickets: Ticket[];
  billing: BillingInfo | null;
  
  // Loading states
  loading: boolean;
  setLoading: (loading: boolean) => void;
  
  // Actions
  refreshData: () => void;
  createProject: (project: Omit<Project, 'id'>) => void;
  updateProject: (project: Project) => void;
  createAgent: (agent: Omit<Agent, 'id'>) => void;
  updateAgent: (agent: Agent) => void;
  createWorkflow: (workflow: Omit<Workflow, 'id'>) => void;
  updateWorkflow: (workflow: Workflow) => void;
  createTicket: (ticket: Omit<Ticket, 'id'>) => void;
}

const ClientContext = createContext<ClientContextType | undefined>(undefined);

// Mock data
const mockProjects: Project[] = [
  {
    id: '1',
    name: 'Customer Service AI Implementation',
    description: 'Deploy AI-powered customer service chatbot with natural language processing',
    status: 'in-progress',
    priority: 'high',
    startDate: new Date('2024-01-15'),
    endDate: new Date('2024-04-15'),
    progress: 65,
    team: ['Sarah Johnson', 'Mike Chen', 'Alex Rodriguez'],
    budget: 150000,
    spent: 97500
  },
  {
    id: '2',
    name: 'Data Analytics Transformation',
    description: 'Implement AI-driven analytics platform for business intelligence',
    status: 'in-progress',
    priority: 'medium',
    startDate: new Date('2024-02-01'),
    endDate: new Date('2024-06-01'),
    progress: 35,
    team: ['David Kim', 'Lisa Wang', 'Tom Brown'],
    budget: 200000,
    spent: 70000
  }
];

const mockAgents: Agent[] = [
  {
    id: '1',
    name: 'Customer Support Bot',
    type: 'chatbot',
    status: 'active',
    description: 'AI agent for handling customer inquiries and support requests',
    capabilities: ['natural_language', 'context_awareness', 'multi_turn', 'sentiment_analysis'],
    createdAt: new Date('2024-01-20T10:00:00Z'),
    lastUsed: new Date('2024-01-20T15:30:00Z'),
    usage: {
      totalInteractions: 2450,
      successRate: 96.8,
      avgResponseTime: 1.2
    }
  },
  {
    id: '2',
    name: 'Sales Analytics Agent',
    type: 'analytics',
    status: 'active',
    description: 'AI agent for analyzing sales data and generating insights',
    capabilities: ['data_analysis', 'visualization', 'reporting', 'forecasting'],
    createdAt: new Date('2024-01-25T14:00:00Z'),
    lastUsed: new Date('2024-01-20T12:15:00Z'),
    usage: {
      totalInteractions: 890,
      successRate: 98.2,
      avgResponseTime: 2.8
    }
  }
];

const mockWorkflows: Workflow[] = [
  {
    id: '1',
    name: 'Lead Qualification Process',
    description: 'Automated lead scoring and qualification workflow',
    status: 'active',
    type: 'automation',
    steps: [
      { id: '1', name: 'Data Collection', type: 'action', config: {}, order: 1 },
      { id: '2', name: 'Scoring Algorithm', type: 'condition', config: {}, order: 2 },
      { id: '3', name: 'Notification', type: 'notification', config: {}, order: 3 }
    ],
    createdAt: new Date('2024-01-10'),
    lastRun: new Date('2024-01-20T14:30:00Z'),
    runCount: 1250,
    successRate: 94.5
  }
];

const mockTickets: Ticket[] = [
  {
    id: '1',
    title: 'Agent Response Time Optimization',
    description: 'Looking to improve response times for our customer support agent',
    status: 'in-progress',
    priority: 'medium',
    category: 'technical',
    createdAt: new Date('2024-01-18T10:30:00Z'),
    updatedAt: new Date('2024-01-19T14:20:00Z'),
    assignedTo: 'Sarah Johnson',
    createdBy: 'john.smith@company.com',
    responses: [
      {
        id: '1',
        content: 'We\'ve noticed our customer support agent response times have increased. Can you help optimize performance?',
        createdAt: new Date('2024-01-18T10:30:00Z'),
        createdBy: 'john.smith@company.com',
        isInternal: false
      },
      {
        id: '2',
        content: 'I\'ll analyze the current configuration and provide optimization recommendations within 24 hours.',
        createdAt: new Date('2024-01-18T11:15:00Z'),
        createdBy: 'sarah.johnson@appliedinnovation.com',
        isInternal: false
      }
    ]
  }
];

const mockBilling: BillingInfo = {
  currentPlan: 'Professional',
  billingCycle: 'monthly',
  nextBillingDate: new Date('2024-02-01'),
  amount: 1247.80,
  paymentMethod: {
    type: 'card',
    last4: '4242',
    expiryDate: '12/26'
  },
  invoices: [
    {
      id: '1',
      date: new Date('2024-01-01'),
      amount: 1247.80,
      status: 'paid',
      downloadUrl: '/invoices/2024-01.pdf'
    },
    {
      id: '2',
      date: new Date('2023-12-01'),
      amount: 1089.50,
      status: 'paid',
      downloadUrl: '/invoices/2023-12.pdf'
    }
  ]
};

export const ClientProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>({
    id: '1',
    email: 'john.smith@company.com',
    name: 'John Smith',
    role: 'client',
    status: 'active',
    createdAt: new Date('2024-01-01'),
    lastLogin: new Date('2024-01-20T15:30:00Z')
  });
  
  const [projects] = useState<Project[]>(mockProjects);
  const [agents] = useState<Agent[]>(mockAgents);
  const [workflows] = useState<Workflow[]>(mockWorkflows);
  const [tickets] = useState<Ticket[]>(mockTickets);
  const [billing] = useState<BillingInfo | null>(mockBilling);
  const [loading, setLoading] = useState(false);

  const refreshData = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  const createProject = (project: Omit<Project, 'id'>) => {
    console.log('Creating project:', project);
  };

  const updateProject = (project: Project) => {
    console.log('Updating project:', project);
  };

  const createAgent = (agent: Omit<Agent, 'id'>) => {
    console.log('Creating agent:', agent);
  };

  const updateAgent = (agent: Agent) => {
    console.log('Updating agent:', agent);
  };

  const createWorkflow = (workflow: Omit<Workflow, 'id'>) => {
    console.log('Creating workflow:', workflow);
  };

  const updateWorkflow = (workflow: Workflow) => {
    console.log('Updating workflow:', workflow);
  };

  const createTicket = (ticket: Omit<Ticket, 'id'>) => {
    console.log('Creating support ticket:', ticket);
  };

  const value: ClientContextType = {
    currentUser,
    setCurrentUser,
    projects,
    agents,
    workflows,
    tickets,
    billing,
    loading,
    setLoading,
    refreshData,
    createProject,
    updateProject,
    createAgent,
    updateAgent,
    createWorkflow,
    updateWorkflow,
    createTicket
  };

  return (
    <ClientContext.Provider value={value}>
      {children}
    </ClientContext.Provider>
  );
};

export const useClient = () => {
  const context = useContext(ClientContext);
  if (context === undefined) {
    throw new Error('useClient must be used within a ClientProvider');
  }
  return context;
};
