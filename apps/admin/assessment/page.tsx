'use client'

import { useState, useEffect } from 'react'
import { FileText, Users, CheckCircle, XCircle, Clock, AlertTriangle, Download } from 'lucide-react'

interface AssessmentStats {
  total: number
  completed: number
  processing: number
  failed: number
  recentSubmissions: Array<{
    id: string
    email: string
    companyName: string
    overallScore: number
    status: string
    createdAt: string
    reportGenerated: boolean
  }>
}

export default function AssessmentAdminPage() {
  const [stats, setStats] = useState<AssessmentStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock data - replace with actual API call
    setTimeout(() => {
      setStats({
        total: 342,
        completed: 298,
        processing: 12,
        failed: 32,
        recentSubmissions: [
          {
            id: '1',
            email: 'john@company.com',
            companyName: 'Tech Corp',
            overallScore: 78,
            status: 'COMPLETED',
            createdAt: '2024-01-15T10:30:00Z',
            reportGenerated: true
          },
          {
            id: '2',
            email: 'sarah@startup.com',
            companyName: 'AI Startup',
            overallScore: 0,
            status: 'PROCESSING',
            createdAt: '2024-01-15T09:15:00Z',
            reportGenerated: false
          }
        ]
      })
      setLoading(false)
    }, 1000)
  }, [])

  if (loading) {
    return <div className="p-6">Loading...</div>
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Assessment Management</h1>
        <p className="text-gray-600">Monitor AI readiness assessments and report generation</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Assessments</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.total.toLocaleString()}</p>
            </div>
            <FileText className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-green-600">{stats?.completed.toLocaleString()}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Processing</p>
              <p className="text-2xl font-bold text-yellow-600">{stats?.processing.toLocaleString()}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Failed</p>
              <p className="text-2xl font-bold text-red-600">{stats?.failed.toLocaleString()}</p>
            </div>
            <XCircle className="h-8 w-8 text-red-600" />
          </div>
        </div>
      </div>

      {/* Recent Assessments */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Assessments</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {stats?.recentSubmissions.map((assessment) => (
                <tr key={assessment.id}>
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                    {assessment.companyName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                    {assessment.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {assessment.overallScore > 0 ? (
                      <span className="font-medium">{assessment.overallScore}/100</span>
                    ) : (
                      <span className="text-gray-400">Calculating...</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      assessment.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
                      assessment.status === 'PROCESSING' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {assessment.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                    {new Date(assessment.createdAt).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {assessment.reportGenerated && (
                      <button className="text-blue-600 hover:text-blue-800">
                        <Download className="h-4 w-4" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
