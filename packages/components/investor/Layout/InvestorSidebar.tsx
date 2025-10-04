'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  X, 
  LayoutDashboard, 
  FileText, 
  DollarSign, 
  Briefcase, 
  Bell,
  Users,
  MessageSquare,
  Calendar,
  Activity,
  TrendingUp
} from 'lucide-react';

interface InvestorSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const InvestorSidebar: React.FC<InvestorSidebarProps> = ({ isOpen, onClose }) => {
  const pathname = usePathname();
  
  const navigation = [
    { name: 'Dashboard', href: '/ir', icon: LayoutDashboard },
    { name: 'Data Room', href: '/ir/data-room', icon: FileText },
    { name: 'Financials', href: '/ir/financials', icon: DollarSign },
    { name: 'Portfolio', href: '/ir/portfolio', icon: Briefcase },
    { name: 'Updates', href: '/ir/updates', icon: Bell },
    { name: 'Board Meetings', href: '/ir/board', icon: Calendar },
    { name: 'Investors', href: '/ir/investors', icon: Users },
    { name: 'Messages', href: '/ir/messages', icon: MessageSquare },
    { name: 'Activity', href: '/ir/activity', icon: Activity },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-gray-600 bg-opacity-75 z-20 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-30 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-blue-600 mr-2" />
            <span className="text-xl font-bold text-gray-900">AIC Investor</span>
          </div>
          <button
            onClick={onClose}
            className="lg:hidden text-gray-400 hover:text-gray-600"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <nav className="mt-6 px-3">
          <div className="space-y-1">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                  onClick={() => onClose()}
                >
                  <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </nav>

        {/* Investment Summary */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <div className="text-sm">
            <div className="flex items-center justify-between mb-1">
              <span className="text-gray-500">Investment</span>
              <span className="text-gray-900 font-medium">$2.5M</span>
            </div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-gray-500">Equity</span>
              <span className="text-gray-900 font-medium">15.5%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-500">Current Value</span>
              <span className="text-green-600 font-medium">$3.9M</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default InvestorSidebar;
