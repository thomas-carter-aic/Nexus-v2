import type { Metadata } from 'next';
import { TrendingUp, Users, Brain, Activity, Calendar, Download, BarChart3, LineChart as LineChartIcon, PieChart as PieChartIcon } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Analytics - Admin Portal',
  description: 'System analytics, usage metrics, and performance insights for the Applied Innovations platform.',
};

const usageData = [
  { month: 'Jan', users: 1200, aiRequests: 15000, projects: 450 },
  { month: 'Feb', users: 1350, aiRequests: 18000, projects: 520 },
  { month: 'Mar', users: 1500, aiRequests: 22000, projects: 680 },
  { month: 'Apr', users: 1650, aiRequests: 25000, projects: 750 },
  { month: 'May', users: 1800, aiRequests: 28000, projects: 820 },
  { month: 'Jun', users: 1950, aiRequests: 32000, projects: 900 },
];

const aiModelUsage = [
  { name: 'GPT-4', value: 45, color: '#3b82f6' },
  { name: 'Claude', value: 30, color: '#10b981' },
  { name: 'Gemini', value: 15, color: '#f59e0b' },
  { name: 'Custom Models', value: 10, color: '#8b5cf6' },
];

const performanceData = [
  { time: '00:00', responseTime: 120, uptime: 99.9 },
  { time: '04:00', responseTime: 110, uptime: 99.8 },
  { time: '08:00', responseTime: 150, uptime: 99.9 },
  { time: '12:00', responseTime: 180, uptime: 99.7 },
  { time: '16:00', responseTime: 160, uptime: 99.8 },
  { time: '20:00', responseTime: 140, uptime: 99.9 },
];

const stats = [
  {
    name: 'Total Users',
    value: '1,950',
    change: '+12.5%',
    changeType: 'increase',
    icon: Users,
  },
  {
    name: 'AI Requests',
    value: '32,000',
    change: '+18.2%',
    changeType: 'increase',
    icon: Brain,
  },
  {
    name: 'Active Projects',
    value: '900',
    change: '+9.8%',
    changeType: 'increase',
    icon: Activity,
  },
  {
    name: 'Avg Response Time',
    value: '145ms',
    change: '-5.2%',
    changeType: 'decrease',
    icon: TrendingUp,
  },
];

export default function AdminAnalyticsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-secondary-900">Analytics Dashboard</h1>
          <p className="text-secondary-600">
            System performance metrics and usage analytics.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <select className="border border-secondary-300 rounded-lg px-3 py-2 text-sm">
            <option>Last 30 days</option>
            <option>Last 90 days</option>
            <option>Last 6 months</option>
            <option>Last year</option>
          </select>
          <button className="btn-secondary text-sm">
            <Download className="w-4 h-4 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white rounded-lg border border-secondary-200 p-6">
            <div className="flex items-center">
              <div className="flex items-center justify-center w-10 h-10 bg-primary-100 rounded-lg">
                <stat.icon className="w-5 h-5 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-secondary-600">{stat.name}</p>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-secondary-900">{stat.value}</p>
                  <span
                    className={`ml-2 text-sm font-medium ${
                      stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {stat.change}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Usage Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-secondary-200 p-6">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">Usage Trends</h3>
          <div className="h-64 flex items-center justify-center bg-secondary-50 rounded-lg">
            <div className="text-center">
              <LineChartIcon className="w-12 h-12 text-secondary-400 mx-auto mb-2" />
              <p className="text-secondary-600">Interactive chart showing user and project growth over time</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-secondary-200 p-6">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">AI Model Usage</h3>
          <div className="h-64 flex items-center justify-center bg-secondary-50 rounded-lg">
            <div className="text-center">
              <PieChartIcon className="w-12 h-12 text-secondary-400 mx-auto mb-2" />
              <p className="text-secondary-600">Distribution of AI model usage across the platform</p>
            </div>
          </div>
        </div>
      </div>

      {/* AI Requests Over Time */}
      <div className="bg-white rounded-lg border border-secondary-200 p-6">
        <h3 className="text-lg font-semibold text-secondary-900 mb-4">AI Requests Over Time</h3>
        <div className="h-96 flex items-center justify-center bg-secondary-50 rounded-lg">
          <div className="text-center">
            <BarChart3 className="w-12 h-12 text-secondary-400 mx-auto mb-2" />
            <p className="text-secondary-600">Monthly AI request volume and trends</p>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="bg-white rounded-lg border border-secondary-200 p-6">
        <h3 className="text-lg font-semibold text-secondary-900 mb-4">System Performance</h3>
        <div className="h-64 flex items-center justify-center bg-secondary-50 rounded-lg">
          <div className="text-center">
            <LineChartIcon className="w-12 h-12 text-secondary-400 mx-auto mb-2" />
            <p className="text-secondary-600">Response time and uptime metrics over 24 hours</p>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg border border-secondary-200 p-6">
        <h3 className="text-lg font-semibold text-secondary-900 mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {[
            { time: '2 minutes ago', event: 'New user registration', user: 'john.doe@company.com' },
            { time: '5 minutes ago', event: 'AI workflow completed', user: 'Project Alpha' },
            { time: '12 minutes ago', event: 'System backup completed', user: 'System' },
            { time: '18 minutes ago', event: 'New project created', user: 'sarah.wilson@startup.com' },
            { time: '25 minutes ago', event: 'API key generated', user: 'admin@company.com' },
          ].map((activity, index) => (
            <div key={index} className="flex items-center justify-between py-3 border-b border-secondary-100 last:border-b-0">
              <div className="flex items-center">
                <div className="w-2 h-2 bg-primary-500 rounded-full mr-3"></div>
                <div>
                  <p className="text-sm font-medium text-secondary-900">{activity.event}</p>
                  <p className="text-xs text-secondary-600">{activity.user}</p>
                </div>
              </div>
              <span className="text-xs text-secondary-500">{activity.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
