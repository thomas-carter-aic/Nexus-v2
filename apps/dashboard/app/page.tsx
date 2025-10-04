"use client";

import { Button } from "@ultimate-paas/ui";
import { useAuthStore } from "@ultimate-paas/auth";
import { DashboardOverview } from "../components/dashboard-overview";

export default function HomePage() {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Welcome to Ultimate PaaS
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              AI-Native Cloud-Native Platform as a Service
            </p>
          </div>
          <div className="space-y-4">
            <Button className="w-full" onClick={() => window.location.href = '/auth/signin'}>
              Sign In
            </Button>
            <Button variant="outline" className="w-full">
              Learn More
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">
              Dashboard
            </h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                Welcome, {user?.name}
              </span>
              <Button variant="outline" size="sm">
                Profile
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <DashboardOverview />
      </main>
    </div>
  );
}
