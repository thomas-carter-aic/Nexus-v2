'use client'

import { useState } from 'react'
import { Menu } from 'lucide-react'
import { DocsSidebar } from '@/components/docs/DocsSidebar'

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="min-h-screen bg-white">
      <div className="flex">
        {/* Sidebar */}
        <DocsSidebar 
          isOpen={sidebarOpen} 
          onClose={() => setSidebarOpen(false)} 
        />

        {/* Main Content */}
        <div className="flex-1 lg:ml-0">
          {/* Mobile Header */}
          <div className="lg:hidden flex items-center justify-between p-4 border-b border-secondary-200 bg-white sticky top-0 z-30">
            <button
              onClick={() => setSidebarOpen(true)}
              className="p-2 hover:bg-secondary-100 rounded-lg"
            >
              <Menu className="w-5 h-5" />
            </button>
            <h1 className="text-lg font-semibold text-secondary-900">Documentation</h1>
            <div className="w-9" /> {/* Spacer for centering */}
          </div>

          {/* Content */}
          <main className="p-6 lg:p-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  )
}
