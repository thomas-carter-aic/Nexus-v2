import type { Metadata } from 'next';
import { Calendar, Clock, Users, FileText, Video, Download, Lock, CheckCircle } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Board Meetings - Investor Relations',
  description: 'Board meeting schedules, materials, and minutes for Applied Innovations Corporation investors.',
};

const upcomingMeetings = [
  {
    id: 1,
    date: '2024-07-15',
    time: '10:00 AM PST',
    type: 'Regular Board Meeting',
    location: 'Virtual (Zoom)',
    status: 'scheduled',
    agenda: [
      'Q2 2024 Financial Review',
      'Product Roadmap Update',
      'Strategic Partnership Discussion',
      'Hiring and Compensation Review',
      'Risk Management Update',
    ],
    materials: [
      { name: 'Board Package Q2 2024.pdf', size: '3.2 MB', uploaded: true },
      { name: 'Financial Statements.xlsx', size: '1.1 MB', uploaded: true },
      { name: 'Product Roadmap.pdf', size: '2.8 MB', uploaded: false },
    ],
    attendees: [
      'Sarah Chen (CEO)',
      'Michael Rodriguez (CTO)',
      'Board Members (5)',
      'Observers (2)',
    ],
  },
  {
    id: 2,
    date: '2024-08-20',
    time: '2:00 PM PST',
    type: 'Special Board Meeting',
    location: 'San Francisco Office',
    status: 'scheduled',
    agenda: [
      'Series C Funding Discussion',
      'Market Expansion Strategy',
      'Acquisition Opportunities',
    ],
    materials: [],
    attendees: [
      'Sarah Chen (CEO)',
      'Board Members (5)',
      'Investment Advisors (2)',
    ],
  },
];

const pastMeetings = [
  {
    id: 3,
    date: '2024-06-10',
    time: '10:00 AM PST',
    type: 'Regular Board Meeting',
    location: 'Virtual (Zoom)',
    status: 'completed',
    duration: '2h 15m',
    materials: [
      { name: 'Board Minutes June 2024.pdf', size: '892 KB' },
      { name: 'Q1 Financial Review.pdf', size: '2.1 MB' },
      { name: 'Partnership Proposal.pdf', size: '1.8 MB' },
    ],
    decisions: [
      'Approved Q1 2024 financial statements',
      'Authorized Microsoft Azure partnership',
      'Approved hiring plan for Q3 2024',
      'Ratified stock option grants',
    ],
    attendees: [
      'Sarah Chen (CEO)',
      'Michael Rodriguez (CTO)',
      'Board Members (5)',
      'Legal Counsel (1)',
    ],
  },
  {
    id: 4,
    date: '2024-04-15',
    time: '10:00 AM PST',
    type: 'Regular Board Meeting',
    location: 'San Francisco Office',
    status: 'completed',
    duration: '2h 30m',
    materials: [
      { name: 'Board Minutes April 2024.pdf', size: '756 KB' },
      { name: 'Annual Strategic Plan.pdf', size: '4.2 MB' },
      { name: 'Compensation Review.pdf', size: '1.3 MB' },
    ],
    decisions: [
      'Approved 2024 strategic plan',
      'Authorized Series B funding round',
      'Approved executive compensation adjustments',
      'Established audit committee charter',
    ],
    attendees: [
      'Sarah Chen (CEO)',
      'Michael Rodriguez (CTO)',
      'Board Members (5)',
      'External Auditor (1)',
    ],
  },
  {
    id: 5,
    date: '2024-02-12',
    time: '10:00 AM PST',
    type: 'Special Board Meeting',
    location: 'Virtual (Zoom)',
    status: 'completed',
    duration: '1h 45m',
    materials: [
      { name: 'Board Minutes February 2024.pdf', size: '623 KB' },
      { name: 'Acquisition Analysis.pdf', size: '3.1 MB' },
    ],
    decisions: [
      'Approved acquisition of DataFlow Analytics',
      'Authorized integration budget',
      'Established integration timeline',
    ],
    attendees: [
      'Sarah Chen (CEO)',
      'Board Members (4)',
      'M&A Advisor (1)',
    ],
  },
];

const getStatusBadge = (status: string) => {
  const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";
  switch (status) {
    case 'scheduled':
      return `${baseClasses} bg-blue-100 text-blue-800`;
    case 'completed':
      return `${baseClasses} bg-green-100 text-green-800`;
    case 'cancelled':
      return `${baseClasses} bg-red-100 text-red-800`;
    default:
      return `${baseClasses} bg-secondary-100 text-secondary-800`;
  }
};

export default function BoardMeetingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-secondary-900">Board Meetings</h1>
        <p className="text-secondary-600">
          Board meeting schedules, materials, and minutes for Applied Innovations Corporation.
        </p>
      </div>

      {/* Upcoming Meetings */}
      <div className="bg-white rounded-lg border border-secondary-200 p-6">
        <h2 className="text-lg font-semibold text-secondary-900 mb-4">Upcoming Meetings</h2>
        <div className="space-y-6">
          {upcomingMeetings.map((meeting) => (
            <div key={meeting.id} className="border border-secondary-200 rounded-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-secondary-900">{meeting.type}</h3>
                  <div className="flex items-center space-x-4 mt-2 text-sm text-secondary-600">
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(meeting.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </div>
                    <div className="flex items-center">
                      <Clock className="w-4 h-4 mr-1" />
                      {meeting.time}
                    </div>
                    <div className="flex items-center">
                      <Video className="w-4 h-4 mr-1" />
                      {meeting.location}
                    </div>
                  </div>
                </div>
                <span className={getStatusBadge(meeting.status)}>
                  {meeting.status.charAt(0).toUpperCase() + meeting.status.slice(1)}
                </span>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-sm font-medium text-secondary-900 mb-3">Agenda</h4>
                  <ul className="space-y-2">
                    {meeting.agenda.map((item, index) => (
                      <li key={index} className="flex items-start text-sm text-secondary-700">
                        <span className="w-4 h-4 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">
                          {index + 1}
                        </span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-secondary-900 mb-3">Meeting Materials</h4>
                  <div className="space-y-2">
                    {meeting.materials.length > 0 ? (
                      meeting.materials.map((material, index) => (
                        <div key={index} className="flex items-center justify-between p-2 bg-secondary-50 rounded">
                          <div className="flex items-center">
                            <FileText className="w-4 h-4 text-secondary-600 mr-2" />
                            <div>
                              <p className="text-sm font-medium text-secondary-900">{material.name}</p>
                              <p className="text-xs text-secondary-600">{material.size}</p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            {material.uploaded ? (
                              <CheckCircle className="w-4 h-4 text-green-500" />
                            ) : (
                              <Clock className="w-4 h-4 text-yellow-500" />
                            )}
                            {material.uploaded && (
                              <button className="text-sm text-primary-600 hover:text-primary-700">
                                <Download className="w-4 h-4" />
                              </button>
                            )}
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-secondary-600 italic">Materials will be uploaded 48 hours before the meeting</p>
                    )}
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-secondary-200">
                <h4 className="text-sm font-medium text-secondary-900 mb-2">Expected Attendees</h4>
                <div className="flex items-center space-x-4 text-sm text-secondary-600">
                  <Users className="w-4 h-4" />
                  <span>{meeting.attendees.join(', ')}</span>
                </div>
              </div>

              <div className="mt-4 flex items-center space-x-3">
                <button className="btn-primary text-sm">
                  Add to Calendar
                </button>
                <button className="btn-secondary text-sm">
                  Join Meeting
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Past Meetings */}
      <div className="bg-white rounded-lg border border-secondary-200 p-6">
        <h2 className="text-lg font-semibold text-secondary-900 mb-4">Past Meetings</h2>
        <div className="space-y-6">
          {pastMeetings.map((meeting) => (
            <div key={meeting.id} className="border border-secondary-200 rounded-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-secondary-900">{meeting.type}</h3>
                  <div className="flex items-center space-x-4 mt-2 text-sm text-secondary-600">
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(meeting.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </div>
                    <div className="flex items-center">
                      <Clock className="w-4 h-4 mr-1" />
                      {meeting.duration}
                    </div>
                  </div>
                </div>
                <span className={getStatusBadge(meeting.status)}>
                  {meeting.status.charAt(0).toUpperCase() + meeting.status.slice(1)}
                </span>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-sm font-medium text-secondary-900 mb-3">Key Decisions</h4>
                  <ul className="space-y-2">
                    {meeting.decisions.map((decision, index) => (
                      <li key={index} className="flex items-start text-sm text-secondary-700">
                        <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                        {decision}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-secondary-900 mb-3">Meeting Materials</h4>
                  <div className="space-y-2">
                    {meeting.materials.map((material, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-secondary-50 rounded">
                        <div className="flex items-center">
                          <FileText className="w-4 h-4 text-secondary-600 mr-2" />
                          <div>
                            <p className="text-sm font-medium text-secondary-900">{material.name}</p>
                            <p className="text-xs text-secondary-600">{material.size}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Lock className="w-3 h-3 text-secondary-400" />
                          <button className="text-sm text-primary-600 hover:text-primary-700">
                            <Download className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-secondary-200">
                <h4 className="text-sm font-medium text-secondary-900 mb-2">Attendees</h4>
                <div className="flex items-center space-x-4 text-sm text-secondary-600">
                  <Users className="w-4 h-4" />
                  <span>{meeting.attendees.join(', ')}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Meeting Archive */}
      <div className="text-center">
        <button className="btn-secondary">
          View Meeting Archive
        </button>
      </div>
    </div>
  );
}
