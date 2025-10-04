export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'client' | 'investor';
  status: 'active' | 'inactive' | 'pending';
  createdAt: Date;
  lastLogin?: Date;
  avatar?: string;
}

export interface Agent {
  id: string;
  name: string;
  type: 'chatbot' | 'workflow' | 'analytics' | 'integration';
  status: 'active' | 'inactive' | 'training';
  description: string;
  capabilities: string[];
  createdAt: Date;
  lastUsed?: Date;
  usage: {
    totalInteractions: number;
    successRate: number;
    avgResponseTime: number;
  };
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive' | 'draft';
  type: 'automation' | 'approval' | 'notification' | 'integration';
  steps: WorkflowStep[];
  createdAt: Date;
  lastRun?: Date;
  runCount: number;
  successRate: number;
}

export interface WorkflowStep {
  id: string;
  name: string;
  type: 'action' | 'condition' | 'approval' | 'notification';
  config: Record<string, any>;
  order: number;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  status: 'planning' | 'in-progress' | 'completed' | 'on-hold';
  priority: 'low' | 'medium' | 'high' | 'critical';
  startDate: Date;
  endDate?: Date;
  progress: number;
  team: string[];
  budget?: number;
  spent?: number;
}

export interface Ticket {
  id: string;
  title: string;
  description: string;
  status: 'open' | 'in-progress' | 'resolved' | 'closed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  category: 'technical' | 'billing' | 'feature-request' | 'bug' | 'general';
  createdAt: Date;
  updatedAt: Date;
  assignedTo?: string;
  createdBy: string;
  responses: TicketResponse[];
}

export interface TicketResponse {
  id: string;
  content: string;
  createdAt: Date;
  createdBy: string;
  isInternal: boolean;
}

export interface BillingInfo {
  currentPlan: string;
  billingCycle: 'monthly' | 'yearly';
  nextBillingDate: Date;
  amount: number;
  paymentMethod: {
    type: 'card' | 'bank';
    last4: string;
    expiryDate?: string;
  };
  invoices: Invoice[];
}

export interface Invoice {
  id: string;
  date: Date;
  amount: number;
  status: 'paid' | 'pending' | 'overdue';
  downloadUrl: string;
}

export interface SystemMetrics {
  uptime: number;
  responseTime: number;
  errorRate: number;
  activeUsers: number;
  totalRequests: number;
  systemLoad: number;
}

export interface ActivityLog {
  id: string;
  timestamp: Date;
  user: string;
  action: string;
  resource: string;
  details: string;
  ipAddress: string;
}
