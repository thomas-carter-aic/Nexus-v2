'use client';

import React, { useState } from 'react';
import { useAdmin } from '../../../contexts/AdminContext';
import { Workflow, Plus, Search, Play, Pause, Settings, BarChart3, GitBranch } from 'lucide-react';

const WorkflowManagement = () => {
  const { workflows } = useAdmin();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  const filteredWorkflows = workflows.filter(workflow => {
    const matchesSearch = workflow.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = filterType === 'all' || workflow.type === filterType;
    const matchesStatus = filterStatus === 'all' || workflow.status === filterStatus;
    
    return matchesSearch && matchesType && matchesStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'inactive':
        return 'bg-gray-100 text-gray-800';
      case 'draft':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'automation':
        return 'bg-blue-100 text-blue-800';
      case 'approval':
        return 'bg-purple-100 text-purple-800';
      case 'notification':
        return 'bg-orange-100 text-orange-800';
      case 'integration':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Workflow Management</h1>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center">
          <Plus className="h-4 w-4 mr-2" />
          Create Workflow
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search workflows..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Types</option>
            <option value="automation">Automation</option>
            <option value="approval">Approval</option>
            <option value="notification">Notification</option>
            <option value="integration">Integration</option>
          </select>
          
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="draft">Draft</option>
          </select>
        </div>
      </div>

      {/* Workflows Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredWorkflows.map((workflow) => (
          <div key={workflow.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <GitBranch className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-semibold text-gray-900">{workflow.name}</h3>
                  <p className="text-sm text-gray-500">{workflow.steps.length} steps</p>
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="text-gray-400 hover:text-gray-600">
                  <Settings className="h-4 w-4" />
                </button>
                <button className="text-blue-600 hover:text-blue-700">
                  <BarChart3 className="h-4 w-4" />
                </button>
              </div>
            </div>

            <div className="space-y-3">
              <p className="text-sm text-gray-600">{workflow.description}</p>
              
              <div className="flex items-center justify-between">
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(workflow.type)}`}>
                  {workflow.type}
                </span>
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(workflow.status)}`}>
                  {workflow.status}
                </span>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Total Runs</span>
                  <span className="font-medium">{workflow.runCount.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Success Rate</span>
                  <span className="font-medium text-green-600">{workflow.successRate}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Last Run</span>
                  <span className="font-medium">
                    {workflow.lastRun ? workflow.lastRun.toLocaleDateString() : 'Never'}
                  </span>
                </div>
              </div>

              <div className="pt-3 border-t border-gray-200">
                <div className="mb-3">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Workflow Steps:</h4>
                  <div className="space-y-1">
                    {workflow.steps.slice(0, 3).map((step, index) => (
                      <div key={step.id} className="flex items-center text-xs text-gray-600">
                        <div className="w-4 h-4 bg-gray-200 rounded-full flex items-center justify-center mr-2">
                          <span className="text-xs">{index + 1}</span>
                        </div>
                        {step.name}
                      </div>
                    ))}
                    {workflow.steps.length > 3 && (
                      <div className="text-xs text-gray-500 ml-6">
                        +{workflow.steps.length - 3} more steps
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex space-x-2">
                  {workflow.status === 'active' ? (
                    <button className="flex-1 bg-red-100 text-red-700 px-3 py-2 rounded-md hover:bg-red-200 transition-colors flex items-center justify-center">
                      <Pause className="h-4 w-4 mr-1" />
                      Pause
                    </button>
                  ) : (
                    <button className="flex-1 bg-green-100 text-green-700 px-3 py-2 rounded-md hover:bg-green-200 transition-colors flex items-center justify-center">
                      <Play className="h-4 w-4 mr-1" />
                      Start
                    </button>
                  )}
                  <button className="flex-1 bg-blue-100 text-blue-700 px-3 py-2 rounded-md hover:bg-blue-200 transition-colors">
                    Edit
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WorkflowManagement;
