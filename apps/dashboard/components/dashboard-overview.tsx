"use client";

import { Button } from "@ultimate-paas/ui";

export function DashboardOverview() {
  const stats = [
    { name: "Total Applications", value: "12", change: "+2.1%" },
    { name: "Active Deployments", value: "8", change: "+4.3%" },
    { name: "Monthly Cost", value: "$2,847", change: "-1.2%" },
    { name: "Success Rate", value: "99.2%", change: "+0.1%" },
  ];

  const microfrontends = [
    {
      name: "Application Management",
      description: "Manage your applications and services",
      url: "http://localhost:3001",
      status: "active",
    },
    {
      name: "Deployment Center",
      description: "Deploy and manage your releases",
      url: "http://localhost:3002",
      status: "active",
    },
    {
      name: "AI Analytics",
      description: "AI-powered insights and analytics",
      url: "http://localhost:3003",
      status: "active",
    },
    {
      name: "Plugin Management",
      description: "Manage platform plugins and extensions",
      url: "http://localhost:3004",
      status: "active",
    },
    {
      name: "Security Center",
      description: "Security settings and compliance",
      url: "http://localhost:3005",
      status: "active",
    },
    {
      name: "Monitoring",
      description: "System monitoring and observability",
      url: "http://localhost:3006",
      status: "active",
    },
  ];

  return (
    <div className="space-y-8">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="text-lg font-medium text-gray-900">
                    {stat.value}
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="text-sm text-gray-900">{stat.change}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Microfrontends Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Platform Services
        </h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {microfrontends.map((service) => (
            <div
              key={service.name}
              className="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium text-gray-900">
                    {service.name}
                  </h3>
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      service.status === "active"
                        ? "bg-green-100 text-green-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {service.status}
                  </span>
                </div>
                <p className="mt-2 text-sm text-gray-600">
                  {service.description}
                </p>
                <div className="mt-4">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => window.open(service.url, "_blank")}
                  >
                    Open Service
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Button className="w-full">Deploy New App</Button>
            <Button variant="outline" className="w-full">
              View Logs
            </Button>
            <Button variant="outline" className="w-full">
              Scale Resources
            </Button>
            <Button variant="outline" className="w-full">
              View Analytics
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
