'use client';

import React, { useState } from 'react';
import InvestorSidebar from './InvestorSidebar';
import InvestorHeader from './InvestorHeader';

interface InvestorLayoutProps {
  children: React.ReactNode;
}

const InvestorLayout: React.FC<InvestorLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      <InvestorSidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      <div className="lg:pl-64">
        <InvestorHeader onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default InvestorLayout;
