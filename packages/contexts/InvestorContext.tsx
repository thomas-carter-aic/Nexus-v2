'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { 
  InvestorProfile, 
  FinancialData, 
  CompanyMetrics, 
  DataRoomDocument, 
  PortfolioCompany, 
  InvestorUpdate 
} from '../types/investor';

interface InvestorContextType {
  // Current investor
  currentInvestor: InvestorProfile | null;
  setCurrentInvestor: (investor: InvestorProfile | null) => void;
  
  // Data states
  financialData: FinancialData[];
  companyMetrics: CompanyMetrics;
  dataRoomDocuments: DataRoomDocument[];
  portfolioCompanies: PortfolioCompany[];
  updates: InvestorUpdate[];
  
  // Loading states
  loading: boolean;
  setLoading: (loading: boolean) => void;
  
  // Actions
  refreshData: () => void;
  downloadDocument: (documentId: string) => void;
  markUpdateAsRead: (updateId: string) => void;
}

const InvestorContext = createContext<InvestorContextType | undefined>(undefined);

// Mock data
const mockInvestor: InvestorProfile = {
  id: '1',
  name: 'Strategic Ventures LLC',
  email: 'contact@strategicventures.com',
  type: 'institutional',
  investmentAmount: 2500000,
  investmentDate: new Date('2023-06-15'),
  equityPercentage: 15.5,
  boardSeat: true,
  status: 'active',
  contactInfo: {
    phone: '+1-555-0123',
    address: '123 Investment Ave, New York, NY 10001',
    preferredContact: 'email'
  },
  preferences: {
    reportingFrequency: 'quarterly',
    communicationStyle: 'detailed',
    interests: ['AI/ML', 'Enterprise Software', 'B2B SaaS']
  }
};

const mockFinancialData: FinancialData[] = [
  {
    period: '2024-Q1',
    revenue: 1250000,
    expenses: 890000,
    netIncome: 360000,
    cashFlow: 420000,
    burnRate: 180000,
    runway: 18,
    growthRate: 45.2,
    customerCount: 125,
    arr: 4800000,
    mrr: 400000
  },
  {
    period: '2023-Q4',
    revenue: 1100000,
    expenses: 820000,
    netIncome: 280000,
    cashFlow: 350000,
    burnRate: 190000,
    runway: 16,
    growthRate: 38.7,
    customerCount: 108,
    arr: 4200000,
    mrr: 350000
  },
  {
    period: '2023-Q3',
    revenue: 950000,
    expenses: 750000,
    netIncome: 200000,
    cashFlow: 280000,
    burnRate: 200000,
    runway: 15,
    growthRate: 32.1,
    customerCount: 92,
    arr: 3600000,
    mrr: 300000
  }
];

const mockCompanyMetrics: CompanyMetrics = {
  valuation: 25000000,
  totalFunding: 8500000,
  fundingRounds: [
    {
      id: '1',
      type: 'seed',
      amount: 1500000,
      date: new Date('2022-03-15'),
      leadInvestor: 'Early Stage Capital',
      valuation: { pre: 6000000, post: 7500000 },
      investors: ['Early Stage Capital', 'Angel Investor Group']
    },
    {
      id: '2',
      type: 'series-a',
      amount: 7000000,
      date: new Date('2023-06-15'),
      leadInvestor: 'Strategic Ventures LLC',
      valuation: { pre: 18000000, post: 25000000 },
      investors: ['Strategic Ventures LLC', 'Growth Partners', 'Tech Accelerator Fund']
    }
  ],
  keyMetrics: {
    customerAcquisitionCost: 2500,
    lifetimeValue: 15000,
    churnRate: 3.2,
    grossMargin: 78.5,
    netMargin: 28.8
  },
  milestones: [
    {
      id: '1',
      title: 'Reach $5M ARR',
      description: 'Achieve $5 million in annual recurring revenue',
      targetDate: new Date('2024-06-30'),
      status: 'in-progress',
      category: 'financial',
      impact: 'high'
    },
    {
      id: '2',
      title: 'Enterprise Customer Milestone',
      description: 'Sign 10 enterprise customers (>$50K ARR each)',
      targetDate: new Date('2024-09-30'),
      status: 'pending',
      category: 'market',
      impact: 'critical'
    }
  ]
};

const mockDataRoomDocuments: DataRoomDocument[] = [
  {
    id: '1',
    name: 'Q1 2024 Financial Report',
    category: 'financial',
    type: 'pdf',
    size: 2500000,
    uploadDate: new Date('2024-04-15'),
    lastModified: new Date('2024-04-15'),
    accessLevel: 'restricted',
    downloadCount: 12,
    description: 'Comprehensive financial report for Q1 2024',
    tags: ['quarterly', 'financial', 'revenue', 'expenses']
  },
  {
    id: '2',
    name: 'Product Roadmap 2024',
    category: 'strategic',
    type: 'presentation',
    size: 15000000,
    uploadDate: new Date('2024-01-30'),
    lastModified: new Date('2024-03-15'),
    accessLevel: 'confidential',
    downloadCount: 8,
    description: 'Detailed product development roadmap for 2024',
    tags: ['roadmap', 'product', 'strategy', '2024']
  },
  {
    id: '3',
    name: 'Legal Structure Overview',
    category: 'legal',
    type: 'pdf',
    size: 1200000,
    uploadDate: new Date('2023-12-01'),
    lastModified: new Date('2023-12-01'),
    accessLevel: 'restricted',
    downloadCount: 15,
    description: 'Company legal structure and governance documents',
    tags: ['legal', 'governance', 'structure']
  }
];

const mockPortfolioCompanies: PortfolioCompany[] = [
  {
    id: '1',
    name: 'Applied Innovations Corporation',
    industry: 'AI/ML Enterprise Software',
    stage: 'growth',
    investmentAmount: 2500000,
    currentValuation: 25000000,
    equityPercentage: 15.5,
    investmentDate: new Date('2023-06-15'),
    status: 'active',
    keyMetrics: {
      revenue: 4800000,
      growth: 45.2,
      employees: 45,
      customers: 125
    },
    lastUpdate: new Date('2024-04-15')
  }
];

const mockUpdates: InvestorUpdate[] = [
  {
    id: '1',
    title: 'Q1 2024 Results: Strong Growth Continues',
    content: 'We\'re excited to share our Q1 2024 results, showing 45% year-over-year growth in ARR and successful expansion into the enterprise market.',
    type: 'financial',
    publishDate: new Date('2024-04-15'),
    author: 'CEO',
    attachments: ['q1-2024-report.pdf'],
    readBy: ['investor-1', 'investor-2'],
    priority: 'high'
  },
  {
    id: '2',
    title: 'New Enterprise Partnership Announced',
    content: 'We\'ve signed a strategic partnership with a Fortune 500 company that will significantly expand our market reach.',
    type: 'strategic',
    publishDate: new Date('2024-03-28'),
    author: 'VP of Business Development',
    attachments: [],
    readBy: ['investor-1'],
    priority: 'medium'
  }
];

export const InvestorProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentInvestor, setCurrentInvestor] = useState<InvestorProfile | null>(mockInvestor);
  const [financialData] = useState<FinancialData[]>(mockFinancialData);
  const [companyMetrics] = useState<CompanyMetrics>(mockCompanyMetrics);
  const [dataRoomDocuments] = useState<DataRoomDocument[]>(mockDataRoomDocuments);
  const [portfolioCompanies] = useState<PortfolioCompany[]>(mockPortfolioCompanies);
  const [updates, setUpdates] = useState<InvestorUpdate[]>(mockUpdates);
  const [loading, setLoading] = useState(false);

  const refreshData = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  const downloadDocument = (documentId: string) => {
    console.log('Downloading document:', documentId);
    // Simulate document download
  };

  const markUpdateAsRead = (updateId: string) => {
    setUpdates(prev => 
      prev.map(update => 
        update.id === updateId 
          ? { ...update, readBy: [...update.readBy, 'current-investor'] }
          : update
      )
    );
  };

  const value: InvestorContextType = {
    currentInvestor,
    setCurrentInvestor,
    financialData,
    companyMetrics,
    dataRoomDocuments,
    portfolioCompanies,
    updates,
    loading,
    setLoading,
    refreshData,
    downloadDocument,
    markUpdateAsRead
  };

  return (
    <InvestorContext.Provider value={value}>
      {children}
    </InvestorContext.Provider>
  );
};

export const useInvestor = () => {
  const context = useContext(InvestorContext);
  if (context === undefined) {
    throw new Error('useInvestor must be used within an InvestorProvider');
  }
  return context;
};
