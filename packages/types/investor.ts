export interface InvestorProfile {
  id: string;
  name: string;
  email: string;
  type: 'individual' | 'institutional' | 'strategic';
  investmentAmount: number;
  investmentDate: Date;
  equityPercentage: number;
  boardSeat: boolean;
  status: 'active' | 'inactive';
  contactInfo: {
    phone?: string;
    address?: string;
    preferredContact: 'email' | 'phone' | 'both';
  };
  preferences: {
    reportingFrequency: 'monthly' | 'quarterly' | 'annually';
    communicationStyle: 'detailed' | 'summary' | 'minimal';
    interests: string[];
  };
}

export interface FinancialData {
  period: string;
  revenue: number;
  expenses: number;
  netIncome: number;
  cashFlow: number;
  burnRate: number;
  runway: number;
  growthRate: number;
  customerCount: number;
  arr: number; // Annual Recurring Revenue
  mrr: number; // Monthly Recurring Revenue
}

export interface CompanyMetrics {
  valuation: number;
  totalFunding: number;
  fundingRounds: FundingRound[];
  keyMetrics: {
    customerAcquisitionCost: number;
    lifetimeValue: number;
    churnRate: number;
    grossMargin: number;
    netMargin: number;
  };
  milestones: Milestone[];
}

export interface FundingRound {
  id: string;
  type: 'seed' | 'series-a' | 'series-b' | 'series-c' | 'bridge' | 'ipo';
  amount: number;
  date: Date;
  leadInvestor: string;
  valuation: {
    pre: number;
    post: number;
  };
  investors: string[];
}

export interface Milestone {
  id: string;
  title: string;
  description: string;
  targetDate: Date;
  completedDate?: Date;
  status: 'pending' | 'in-progress' | 'completed' | 'delayed';
  category: 'financial' | 'product' | 'market' | 'operational' | 'strategic';
  impact: 'low' | 'medium' | 'high' | 'critical';
}

export interface DataRoomDocument {
  id: string;
  name: string;
  category: 'financial' | 'legal' | 'operational' | 'strategic' | 'compliance';
  type: 'pdf' | 'excel' | 'word' | 'presentation' | 'other';
  size: number;
  uploadDate: Date;
  lastModified: Date;
  accessLevel: 'public' | 'restricted' | 'confidential';
  downloadCount: number;
  description?: string;
  tags: string[];
}

export interface PortfolioCompany {
  id: string;
  name: string;
  industry: string;
  stage: 'seed' | 'early' | 'growth' | 'mature';
  investmentAmount: number;
  currentValuation: number;
  equityPercentage: number;
  investmentDate: Date;
  status: 'active' | 'exited' | 'written-off';
  keyMetrics: {
    revenue: number;
    growth: number;
    employees: number;
    customers: number;
  };
  lastUpdate: Date;
  exitDetails?: {
    date: Date;
    type: 'acquisition' | 'ipo' | 'merger';
    amount: number;
    multiple: number;
  };
}

export interface InvestorUpdate {
  id: string;
  title: string;
  content: string;
  type: 'financial' | 'operational' | 'strategic' | 'milestone' | 'general';
  publishDate: Date;
  author: string;
  attachments: string[];
  readBy: string[];
  priority: 'low' | 'medium' | 'high';
}

export interface BoardMeeting {
  id: string;
  title: string;
  date: Date;
  duration: number;
  location: string;
  type: 'regular' | 'special' | 'annual';
  status: 'scheduled' | 'in-progress' | 'completed' | 'cancelled';
  attendees: {
    required: string[];
    optional: string[];
    actual?: string[];
  };
  agenda: AgendaItem[];
  materials: string[];
  minutes?: string;
  actionItems: ActionItem[];
}

export interface AgendaItem {
  id: string;
  title: string;
  description: string;
  presenter: string;
  duration: number;
  order: number;
  type: 'presentation' | 'discussion' | 'vote' | 'report';
}

export interface ActionItem {
  id: string;
  description: string;
  assignedTo: string;
  dueDate: Date;
  status: 'pending' | 'in-progress' | 'completed' | 'overdue';
  priority: 'low' | 'medium' | 'high';
  createdAt: Date;
}
