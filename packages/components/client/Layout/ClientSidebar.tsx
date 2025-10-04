'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  X, 
  LayoutDashboard, 
  FolderOpen, 
  Bot, 
  Workflow, 
  BarChart3, 
  CreditCard, 
  HelpCircle,
  Bell,
  Settings,
  Brain
} from 'lucide-react';

interface ClientSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const ClientSidebar: React.FC<ClientSidebarProps> = ({ isOpen, onClose }) => {
  const pathname = usePathname();
  
  const navigation = [
    { name: 'Dashboard', href: '/client', icon: LayoutDashboard },
    { name: 'Projects', href: '/client/projects', icon: FolderOpen },
    { name: 'AI Agents', href: '/client/agents', icon: Bot },
    { name: 'Workflows', href: '/client/workflows', icon: Workflow },
    { name: 'Analytics', href: '/client/analytics', icon: BarChart3 },
    { name: 'Billing', href: '/client/billing', icon: CreditCard },
    { name: 'Support', href: '/client/support', icon: HelpCircle },
    { name: 'Notifications', href: '/client/notifications', icon: Bell },
    { name: 'Settings', href: '/client/settings', icon: Settings },
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
            <Brain className="h-8 w-8 text-blue-600 mr-2" />
            <span className="text-xl font-bold text-gray-900">AIC Client</span>
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

        {/* Usage Summary */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <div className="text-sm">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-500">Monthly Usage</span>
              <span className="text-gray-900 font-medium">78%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{ width: '78%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ClientSidebar;
