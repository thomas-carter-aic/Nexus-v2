import type { Metadata } from 'next';
import { Settings, Shield, Database, Bell, Users, Key } from 'lucide-react';

export const metadata: Metadata = {
  title: 'System Settings - Admin Portal',
  description: 'Configure system settings, security, and preferences for the Applied Innovations platform.',
};

const settingsCategories = [
  {
    name: 'General Settings',
    description: 'Basic system configuration and preferences',
    icon: Settings,
    settings: [
      { name: 'System Name', value: 'Applied Innovations Platform', type: 'text' },
      { name: 'Default Language', value: 'English', type: 'select' },
      { name: 'Time Zone', value: 'UTC-8 (Pacific)', type: 'select' },
      { name: 'Date Format', value: 'MM/DD/YYYY', type: 'select' },
    ],
  },
  {
    name: 'Security Settings',
    description: 'Authentication, authorization, and security policies',
    icon: Shield,
    settings: [
      { name: 'Two-Factor Authentication', value: 'Enabled', type: 'toggle' },
      { name: 'Session Timeout', value: '30 minutes', type: 'select' },
      { name: 'Password Policy', value: 'Strong', type: 'select' },
      { name: 'Login Attempts', value: '5', type: 'number' },
    ],
  },
  {
    name: 'Database Settings',
    description: 'Database configuration and backup settings',
    icon: Database,
    settings: [
      { name: 'Auto Backup', value: 'Daily', type: 'select' },
      { name: 'Backup Retention', value: '30 days', type: 'select' },
      { name: 'Connection Pool Size', value: '20', type: 'number' },
      { name: 'Query Timeout', value: '30 seconds', type: 'select' },
    ],
  },
  {
    name: 'Notification Settings',
    description: 'Email, SMS, and system notification preferences',
    icon: Bell,
    settings: [
      { name: 'Email Notifications', value: 'Enabled', type: 'toggle' },
      { name: 'SMS Notifications', value: 'Disabled', type: 'toggle' },
      { name: 'System Alerts', value: 'Enabled', type: 'toggle' },
      { name: 'Maintenance Notices', value: 'Enabled', type: 'toggle' },
    ],
  },
];

export default function AdminSettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-secondary-900">System Settings</h1>
        <p className="text-secondary-600">
          Configure system-wide settings, security policies, and preferences.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {settingsCategories.map((category) => (
          <div key={category.name} className="bg-white rounded-lg border border-secondary-200 p-6">
            <div className="flex items-center mb-4">
              <div className="flex items-center justify-center w-10 h-10 bg-primary-100 rounded-lg mr-3">
                <category.icon className="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-secondary-900">{category.name}</h3>
                <p className="text-sm text-secondary-600">{category.description}</p>
              </div>
            </div>

            <div className="space-y-4">
              {category.settings.map((setting) => (
                <div key={setting.name} className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-secondary-900">
                      {setting.name}
                    </label>
                  </div>
                  <div className="flex items-center">
                    {setting.type === 'toggle' ? (
                      <div className="flex items-center">
                        <span className="text-sm text-secondary-600 mr-2">{setting.value}</span>
                        <button
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            setting.value === 'Enabled' ? 'bg-primary-600' : 'bg-secondary-300'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              setting.value === 'Enabled' ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                    ) : (
                      <span className="text-sm text-secondary-900 font-medium">{setting.value}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 pt-4 border-t border-secondary-200">
              <button className="btn-primary text-sm">
                Update {category.name}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* API Keys Section */}
      <div className="bg-white rounded-lg border border-secondary-200 p-6">
        <div className="flex items-center mb-4">
          <div className="flex items-center justify-center w-10 h-10 bg-yellow-100 rounded-lg mr-3">
            <Key className="w-5 h-5 text-yellow-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-secondary-900">API Keys</h3>
            <p className="text-sm text-secondary-600">Manage API keys and integrations</p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
            <div>
              <h4 className="text-sm font-medium text-secondary-900">OpenAI API Key</h4>
              <p className="text-xs text-secondary-600">Used for AI model integrations</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">Active</span>
              <button className="text-sm text-primary-600 hover:text-primary-700">Edit</button>
            </div>
          </div>

          <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
            <div>
              <h4 className="text-sm font-medium text-secondary-900">Webhook Secret</h4>
              <p className="text-xs text-secondary-600">For secure webhook communications</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">Active</span>
              <button className="text-sm text-primary-600 hover:text-primary-700">Edit</button>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <button className="btn-secondary text-sm">
            Add New API Key
          </button>
        </div>
      </div>
    </div>
  );
}
