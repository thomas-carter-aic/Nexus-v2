import type { Metadata } from 'next';
import { Search, Filter, Download, Eye, AlertTriangle, CheckCircle, XCircle, Clock } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Audit Logs - Admin Portal',
  description: 'System audit logs, security events, and activity tracking for the Applied Innovations platform.',
};

const auditLogs = [
  {
    id: 'AL-001',
    timestamp: '2024-07-04 18:45:23',
    user: 'admin@appliedinnovations.ai',
    action: 'User Login',
    resource: 'Authentication System',
    status: 'success',
    ipAddress: '192.168.1.100',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    details: 'Successful admin login with 2FA',
  },
  {
    id: 'AL-002',
    timestamp: '2024-07-04 18:42:15',
    user: 'john.doe@company.com',
    action: 'Project Created',
    resource: 'Project Management',
    status: 'success',
    ipAddress: '10.0.0.45',
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    details: 'Created new AI project "Customer Analytics Dashboard"',
  },
  {
    id: 'AL-003',
    timestamp: '2024-07-04 18:38:07',
    user: 'system',
    action: 'Backup Completed',
    resource: 'Database',
    status: 'success',
    ipAddress: 'localhost',
    userAgent: 'System Process',
    details: 'Daily database backup completed successfully (2.3GB)',
  },
  {
    id: 'AL-004',
    timestamp: '2024-07-04 18:35:42',
    user: 'sarah.wilson@startup.com',
    action: 'Failed Login',
    resource: 'Authentication System',
    status: 'warning',
    ipAddress: '203.0.113.45',
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
    details: 'Failed login attempt - incorrect password (attempt 2/5)',
  },
  {
    id: 'AL-005',
    timestamp: '2024-07-04 18:32:18',
    user: 'api-service',
    action: 'API Key Generated',
    resource: 'API Management',
    status: 'success',
    ipAddress: '172.16.0.10',
    userAgent: 'Internal Service',
    details: 'New API key generated for OpenAI integration',
  },
  {
    id: 'AL-006',
    timestamp: '2024-07-04 18:28:55',
    user: 'mike.chen@enterprise.com',
    action: 'Data Export',
    resource: 'Data Management',
    status: 'success',
    ipAddress: '192.168.1.75',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    details: 'Exported user analytics data (CSV format, 15,000 records)',
  },
  {
    id: 'AL-007',
    timestamp: '2024-07-04 18:25:33',
    user: 'system',
    action: 'Security Scan',
    resource: 'Security System',
    status: 'warning',
    ipAddress: 'localhost',
    userAgent: 'Security Scanner',
    details: 'Detected 3 potential vulnerabilities in dependencies',
  },
  {
    id: 'AL-008',
    timestamp: '2024-07-04 18:22:11',
    user: 'admin@appliedinnovations.ai',
    action: 'User Permissions Modified',
    resource: 'User Management',
    status: 'success',
    ipAddress: '192.168.1.100',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    details: 'Updated permissions for user: john.doe@company.com',
  },
];

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'success':
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    case 'warning':
      return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
    case 'error':
      return <XCircle className="w-4 h-4 text-red-500" />;
    default:
      return <Clock className="w-4 h-4 text-secondary-400" />;
  }
};

const getStatusBadge = (status: string) => {
  const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";
  switch (status) {
    case 'success':
      return `${baseClasses} bg-green-100 text-green-800`;
    case 'warning':
      return `${baseClasses} bg-yellow-100 text-yellow-800`;
    case 'error':
      return `${baseClasses} bg-red-100 text-red-800`;
    default:
      return `${baseClasses} bg-secondary-100 text-secondary-800`;
  }
};

export default function AdminAuditLogsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-secondary-900">Audit Logs</h1>
          <p className="text-secondary-600">
            System activity logs, security events, and user actions.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary text-sm">
            <Download className="w-4 h-4 mr-2" />
            Export Logs
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg border border-secondary-200 p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              Search
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
              <input
                type="text"
                placeholder="Search logs..."
                className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              Status
            </label>
            <select className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option value="">All Statuses</option>
              <option value="success">Success</option>
              <option value="warning">Warning</option>
              <option value="error">Error</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              Action Type
            </label>
            <select className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option value="">All Actions</option>
              <option value="login">Login/Logout</option>
              <option value="project">Project Actions</option>
              <option value="user">User Management</option>
              <option value="system">System Events</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              Date Range
            </label>
            <select className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option value="today">Today</option>
              <option value="week">Last 7 days</option>
              <option value="month">Last 30 days</option>
              <option value="quarter">Last 90 days</option>
            </select>
          </div>
        </div>
        <div className="mt-4 flex items-center space-x-3">
          <button className="btn-primary text-sm">
            <Filter className="w-4 h-4 mr-2" />
            Apply Filters
          </button>
          <button className="text-sm text-secondary-600 hover:text-secondary-900">
            Clear Filters
          </button>
        </div>
      </div>

      {/* Audit Logs Table */}
      <div className="bg-white rounded-lg border border-secondary-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-secondary-200">
          <h3 className="text-lg font-semibold text-secondary-900">Recent Activity</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-secondary-200">
            <thead className="bg-secondary-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 uppercase tracking-wider">
                  Action
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 uppercase tracking-wider">
                  Resource
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 uppercase tracking-wider">
                  IP Address
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-secondary-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-secondary-200">
              {auditLogs.map((log) => (
                <tr key={log.id} className="hover:bg-secondary-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-900">
                    {log.timestamp}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-secondary-900">{log.user}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {getStatusIcon(log.status)}
                      <span className="ml-2 text-sm text-secondary-900">{log.action}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-600">
                    {log.resource}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={getStatusBadge(log.status)}>
                      {log.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-600">
                    {log.ipAddress}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-primary-600 hover:text-primary-900 mr-3">
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="px-6 py-4 border-t border-secondary-200 flex items-center justify-between">
          <div className="text-sm text-secondary-600">
            Showing 1 to 8 of 1,247 results
          </div>
          <div className="flex items-center space-x-2">
            <button className="px-3 py-1 text-sm border border-secondary-300 rounded hover:bg-secondary-50">
              Previous
            </button>
            <button className="px-3 py-1 text-sm bg-primary-600 text-white rounded">
              1
            </button>
            <button className="px-3 py-1 text-sm border border-secondary-300 rounded hover:bg-secondary-50">
              2
            </button>
            <button className="px-3 py-1 text-sm border border-secondary-300 rounded hover:bg-secondary-50">
              3
            </button>
            <button className="px-3 py-1 text-sm border border-secondary-300 rounded hover:bg-secondary-50">
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
