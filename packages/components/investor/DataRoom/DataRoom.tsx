'use client';

import React, { useState } from 'react';
import { useInvestor } from '../../../contexts/InvestorContext';
import { FileText, Download, Search, Filter, Eye, Lock, Calendar } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const DataRoom = () => {
  const { dataRoomDocuments, downloadDocument } = useInvestor();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterAccessLevel, setFilterAccessLevel] = useState('all');

  const filteredDocuments = dataRoomDocuments.filter(doc => {
    const matchesSearch = doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doc.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === 'all' || doc.category === filterCategory;
    const matchesAccess = filterAccessLevel === 'all' || doc.accessLevel === filterAccessLevel;
    
    return matchesSearch && matchesCategory && matchesAccess;
  });

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'financial':
        return 'bg-green-100 text-green-800';
      case 'legal':
        return 'bg-blue-100 text-blue-800';
      case 'operational':
        return 'bg-purple-100 text-purple-800';
      case 'strategic':
        return 'bg-orange-100 text-orange-800';
      case 'compliance':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getAccessLevelColor = (level: string) => {
    switch (level) {
      case 'public':
        return 'text-green-600';
      case 'restricted':
        return 'text-yellow-600';
      case 'confidential':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return '📄';
      case 'excel':
        return '📊';
      case 'word':
        return '📝';
      case 'presentation':
        return '📋';
      default:
        return '📁';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Data Room</h1>
        <div className="text-sm text-gray-500">
          {filteredDocuments.length} documents available
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <FileText className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-bold text-gray-900">{dataRoomDocuments.length}</p>
              <p className="text-sm text-gray-500">Total Documents</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Download className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-bold text-gray-900">
                {dataRoomDocuments.reduce((sum, doc) => sum + doc.downloadCount, 0)}
              </p>
              <p className="text-sm text-gray-500">Total Downloads</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Lock className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-bold text-gray-900">
                {dataRoomDocuments.filter(doc => doc.accessLevel === 'confidential').length}
              </p>
              <p className="text-sm text-gray-500">Confidential</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Calendar className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-bold text-gray-900">
                {dataRoomDocuments.filter(doc => 
                  (Date.now() - doc.uploadDate.getTime()) < 30 * 24 * 60 * 60 * 1000
                ).length}
              </p>
              <p className="text-sm text-gray-500">Recent (30d)</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search documents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Categories</option>
            <option value="financial">Financial</option>
            <option value="legal">Legal</option>
            <option value="operational">Operational</option>
            <option value="strategic">Strategic</option>
            <option value="compliance">Compliance</option>
          </select>
          
          <select
            value={filterAccessLevel}
            onChange={(e) => setFilterAccessLevel(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Access Levels</option>
            <option value="public">Public</option>
            <option value="restricted">Restricted</option>
            <option value="confidential">Confidential</option>
          </select>
        </div>
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="divide-y divide-gray-200">
          {filteredDocuments.map((document) => (
            <div key={document.id} className="p-6 hover:bg-gray-50">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4 flex-1">
                  <div className="text-2xl">{getFileIcon(document.type)}</div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-medium text-gray-900 truncate">
                        {document.name}
                      </h3>
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getCategoryColor(document.category)}`}>
                        {document.category}
                      </span>
                      <div className="flex items-center">
                        <Lock className={`h-4 w-4 mr-1 ${getAccessLevelColor(document.accessLevel)}`} />
                        <span className={`text-xs font-medium ${getAccessLevelColor(document.accessLevel)}`}>
                          {document.accessLevel}
                        </span>
                      </div>
                    </div>
                    
                    {document.description && (
                      <p className="text-gray-600 mb-3 line-clamp-2">{document.description}</p>
                    )}
                    
                    <div className="flex items-center space-x-6 text-sm text-gray-500">
                      <span>{formatFileSize(document.size)}</span>
                      <span>Uploaded {formatDistanceToNow(document.uploadDate, { addSuffix: true })}</span>
                      <span>Modified {formatDistanceToNow(document.lastModified, { addSuffix: true })}</span>
                      <span>{document.downloadCount} downloads</span>
                    </div>
                    
                    {document.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-3">
                        {document.tags.map((tag, index) => (
                          <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  <button className="p-2 text-gray-400 hover:text-gray-600">
                    <Eye className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => downloadDocument(document.id)}
                    className="p-2 text-blue-600 hover:text-blue-700"
                  >
                    <Download className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DataRoom;
