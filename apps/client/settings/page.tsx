import type { Metadata } from 'next';
import { User, Bell, Shield, Palette, Globe, Key, CreditCard } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Account Settings - Client Portal',
  description: 'Manage your account settings, preferences, and security options.',
};

export default function ClientSettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-secondary-900">Account Settings</h1>
        <p className="text-secondary-600">
          Manage your account preferences, security settings, and notifications.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Settings Navigation */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg border border-secondary-200 p-4">
            <nav className="space-y-2">
              {[
                { name: 'Profile', icon: User, active: true },
                { name: 'Notifications', icon: Bell, active: false },
                { name: 'Security', icon: Shield, active: false },
                { name: 'Appearance', icon: Palette, active: false },
                { name: 'Language & Region', icon: Globe, active: false },
                { name: 'API Keys', icon: Key, active: false },
                { name: 'Billing', icon: CreditCard, active: false },
              ].map((item) => (
                <button
                  key={item.name}
                  className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                    item.active
                      ? 'bg-primary-50 text-primary-700 border border-primary-200'
                      : 'text-secondary-600 hover:text-secondary-900 hover:bg-secondary-50'
                  }`}
                >
                  <item.icon className="w-4 h-4 mr-3" />
                  {item.name}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Settings Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Profile Settings */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Profile Information</h3>
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
                  <User className="w-8 h-8 text-primary-600" />
                </div>
                <div>
                  <button className="btn-secondary text-sm">Change Photo</button>
                  <p className="text-xs text-secondary-600 mt-1">JPG, GIF or PNG. 1MB max.</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    defaultValue="John"
                    className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    defaultValue="Doe"
                    className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  defaultValue="john.doe@company.com"
                  className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-2">
                  Company
                </label>
                <input
                  type="text"
                  defaultValue="Acme Corporation"
                  className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-2">
                  Job Title
                </label>
                <input
                  type="text"
                  defaultValue="Senior Data Scientist"
                  className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-2">
                  Bio
                </label>
                <textarea
                  rows={3}
                  defaultValue="Experienced data scientist with a passion for AI and machine learning. Leading digital transformation initiatives at Acme Corporation."
                  className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-secondary-200">
              <div className="flex items-center space-x-3">
                <button className="btn-primary">Save Changes</button>
                <button className="btn-secondary">Cancel</button>
              </div>
            </div>
          </div>

          {/* Notification Preferences */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Notification Preferences</h3>
            <div className="space-y-4">
              {[
                {
                  title: 'Project Updates',
                  description: 'Get notified when your projects have updates or status changes',
                  email: true,
                  push: true,
                },
                {
                  title: 'AI Agent Alerts',
                  description: 'Receive alerts when your AI agents complete tasks or encounter issues',
                  email: true,
                  push: false,
                },
                {
                  title: 'Billing Notifications',
                  description: 'Important billing and payment notifications',
                  email: true,
                  push: false,
                },
                {
                  title: 'Security Alerts',
                  description: 'Security-related notifications and login alerts',
                  email: true,
                  push: true,
                },
                {
                  title: 'Product Updates',
                  description: 'New features, updates, and platform announcements',
                  email: false,
                  push: false,
                },
              ].map((notification, index) => (
                <div key={index} className="flex items-start justify-between py-4 border-b border-secondary-100 last:border-b-0">
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-secondary-900">{notification.title}</h4>
                    <p className="text-sm text-secondary-600">{notification.description}</p>
                  </div>
                  <div className="flex items-center space-x-6 ml-4">
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        defaultChecked={notification.email}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-secondary-300 rounded"
                      />
                      <label className="ml-2 text-sm text-secondary-700">Email</label>
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        defaultChecked={notification.push}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-secondary-300 rounded"
                      />
                      <label className="ml-2 text-sm text-secondary-700">Push</label>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 pt-4 border-t border-secondary-200">
              <button className="btn-primary">Update Preferences</button>
            </div>
          </div>

          {/* Security Settings */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Security Settings</h3>
            <div className="space-y-6">
              <div>
                <h4 className="text-sm font-medium text-secondary-900 mb-3">Password</h4>
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-secondary-700 mb-1">
                      Current Password
                    </label>
                    <input
                      type="password"
                      className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-secondary-700 mb-1">
                      New Password
                    </label>
                    <input
                      type="password"
                      className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-secondary-700 mb-1">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <button className="btn-primary text-sm">Update Password</button>
                </div>
              </div>

              <div className="border-t border-secondary-200 pt-6">
                <h4 className="text-sm font-medium text-secondary-900 mb-3">Two-Factor Authentication</h4>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-secondary-600">
                      Add an extra layer of security to your account
                    </p>
                    <p className="text-xs text-green-600 mt-1">Currently enabled</p>
                  </div>
                  <button className="btn-secondary text-sm">Configure</button>
                </div>
              </div>

              <div className="border-t border-secondary-200 pt-6">
                <h4 className="text-sm font-medium text-secondary-900 mb-3">Active Sessions</h4>
                <div className="space-y-3">
                  {[
                    { device: 'MacBook Pro', location: 'San Francisco, CA', current: true },
                    { device: 'iPhone 15', location: 'San Francisco, CA', current: false },
                  ].map((session, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                      <div>
                        <p className="text-sm font-medium text-secondary-900">
                          {session.device} {session.current && '(Current)'}
                        </p>
                        <p className="text-xs text-secondary-600">{session.location}</p>
                      </div>
                      {!session.current && (
                        <button className="text-sm text-red-600 hover:text-red-700">
                          Revoke
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
