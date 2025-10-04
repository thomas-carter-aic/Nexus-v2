import type { Metadata } from 'next';
import { Video, Calendar, Clock, Users, Play, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Webinars - Applied Innovations Corporation',
  description: 'Join our expert-led webinars on AI trends, best practices, and implementation strategies. Register for upcoming sessions or watch on-demand.',
};

const upcomingWebinars = [
  {
    id: 1,
    title: 'AI Governance: Building Ethical and Compliant AI Systems',
    description: 'Learn how to establish robust AI governance frameworks that ensure ethical, compliant, and responsible AI usage.',
    presenter: 'Dr. Sarah Chen, CEO',
    date: '2024-07-15',
    time: '2:00 PM PST',
    duration: '60 minutes',
    attendees: 245,
    topics: ['AI Ethics', 'Governance', 'Compliance', 'Risk Management'],
    featured: true,
  },
  {
    id: 2,
    title: 'Small Business AI: Quick Wins and Cost-Effective Solutions',
    description: 'Discover practical AI applications that small businesses can implement quickly and affordably.',
    presenter: 'James Thompson, VP Client Success',
    date: '2024-07-22',
    time: '11:00 AM PST',
    duration: '45 minutes',
    attendees: 189,
    topics: ['SMB Strategy', 'Cost-Effective AI', 'Quick Implementation'],
    featured: false,
  },
  {
    id: 3,
    title: 'The Future of Healthcare AI: Trends and Opportunities',
    description: 'Explore emerging trends in healthcare AI and identify opportunities for your organization.',
    presenter: 'Dr. Priya Patel, Head of AI Strategy',
    date: '2024-07-29',
    time: '1:00 PM PST',
    duration: '60 minutes',
    attendees: 312,
    topics: ['Healthcare AI', 'Industry Trends', 'Innovation'],
    featured: false,
  },
];

const onDemandWebinars = [
  {
    id: 4,
    title: 'AI Implementation Roadmap: From Strategy to Success',
    description: 'A comprehensive guide to planning and executing successful AI transformation initiatives.',
    presenter: 'Michael Rodriguez, CTO',
    date: '2024-06-20',
    duration: '55 minutes',
    views: 1247,
    topics: ['AI Strategy', 'Implementation', 'Project Management'],
  },
  {
    id: 5,
    title: 'Data Security in AI: Protecting Your Most Valuable Asset',
    description: 'Best practices for securing data in AI systems and maintaining compliance with regulations.',
    presenter: 'Security Team',
    date: '2024-06-10',
    duration: '50 minutes',
    views: 892,
    topics: ['Data Security', 'Privacy', 'Compliance'],
  },
  {
    id: 6,
    title: 'ROI Measurement in AI Projects: Metrics That Matter',
    description: 'Learn how to measure and demonstrate the return on investment of your AI initiatives.',
    presenter: 'Dr. Priya Patel',
    date: '2024-05-25',
    duration: '45 minutes',
    views: 1156,
    topics: ['ROI Analysis', 'Metrics', 'Business Value'],
  },
  {
    id: 7,
    title: 'Building AI-Ready Teams: Skills and Training Strategies',
    description: 'Strategies for developing AI capabilities within your organization and upskilling your workforce.',
    presenter: 'James Thompson',
    date: '2024-05-15',
    duration: '50 minutes',
    views: 743,
    topics: ['Team Development', 'Training', 'Change Management'],
  },
  {
    id: 8,
    title: 'AI in Financial Services: Fraud Detection and Risk Management',
    description: 'Explore AI applications in financial services, focusing on fraud detection and risk assessment.',
    presenter: 'Industry Expert Panel',
    date: '2024-05-05',
    duration: '60 minutes',
    views: 1089,
    topics: ['Financial Services', 'Fraud Detection', 'Risk Management'],
  },
  {
    id: 9,
    title: 'Manufacturing AI: Predictive Maintenance and Quality Control',
    description: 'Discover how AI is transforming manufacturing through predictive maintenance and automated quality control.',
    presenter: 'Dr. Sarah Chen',
    date: '2024-04-20',
    duration: '55 minutes',
    views: 967,
    topics: ['Manufacturing', 'Predictive Maintenance', 'Quality Control'],
  },
];

export default function WebinarsPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-red-600 rounded-2xl mb-6">
              <Video className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Expert Webinars
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Join our expert-led webinars on AI trends, best practices, and implementation strategies. 
              Register for upcoming sessions or watch our on-demand library.
            </p>
          </div>
        </div>
      </section>

      {/* Upcoming Webinars */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Upcoming Webinars</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Register now for our upcoming expert sessions
            </p>
          </div>

          <div className="space-y-8">
            {upcomingWebinars.map((webinar) => (
              <div key={webinar.id} className={`bg-white border rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-shadow ${webinar.featured ? 'border-primary-200 ring-2 ring-primary-100' : 'border-secondary-200'}`}>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
                  <div className="lg:col-span-2">
                    {webinar.featured && (
                      <div className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800 mb-3">
                        Featured Webinar
                      </div>
                    )}
                    
                    <h3 className="text-xl font-bold text-secondary-900 mb-3">
                      {webinar.title}
                    </h3>
                    
                    <p className="text-secondary-600 mb-4">
                      {webinar.description}
                    </p>

                    <div className="flex flex-wrap gap-2 mb-4">
                      {webinar.topics.map((topic, index) => (
                        <span key={index} className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-secondary-100 text-secondary-700">
                          {topic}
                        </span>
                      ))}
                    </div>

                    <div className="flex items-center space-x-6 text-sm text-secondary-600">
                      <div className="flex items-center">
                        <Users className="w-4 h-4 mr-1" />
                        {webinar.presenter}
                      </div>
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        {webinar.duration}
                      </div>
                      <div className="flex items-center">
                        <Users className="w-4 h-4 mr-1" />
                        {webinar.attendees} registered
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col justify-center">
                    <div className="text-center mb-4">
                      <div className="text-2xl font-bold text-primary-600 mb-1">
                        {new Date(webinar.date).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                        })}
                      </div>
                      <div className="text-sm text-secondary-600 mb-2">
                        {new Date(webinar.date).toLocaleDateString('en-US', {
                          year: 'numeric',
                          weekday: 'long',
                        })}
                      </div>
                      <div className="text-sm font-medium text-secondary-900">
                        {webinar.time}
                      </div>
                    </div>
                    
                    <button className="btn-primary w-full">
                      Register Now
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* On-Demand Webinars */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">On-Demand Webinars</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Watch our library of expert sessions anytime
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {onDemandWebinars.map((webinar) => (
              <div key={webinar.id} className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-shadow">
                <div className="h-40 bg-gradient-to-br from-secondary-100 to-primary-100 flex items-center justify-center relative">
                  <Play className="w-12 h-12 text-primary-600" />
                  <div className="absolute top-3 right-3 bg-black bg-opacity-75 text-white text-xs px-2 py-1 rounded">
                    {webinar.duration}
                  </div>
                </div>
                
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-secondary-900 mb-2">
                    {webinar.title}
                  </h3>
                  
                  <p className="text-sm text-secondary-600 mb-4">
                    {webinar.description}
                  </p>

                  <div className="flex flex-wrap gap-1 mb-4">
                    {webinar.topics.slice(0, 2).map((topic, index) => (
                      <span key={index} className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-secondary-100 text-secondary-700">
                        {topic}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center justify-between text-xs text-secondary-600 mb-4">
                    <span>{webinar.presenter}</span>
                    <span>{webinar.views} views</span>
                  </div>

                  <div className="text-xs text-secondary-500 mb-4">
                    {new Date(webinar.date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </div>

                  <button className="btn-secondary w-full text-sm">
                    <Play className="w-4 h-4 mr-2" />
                    Watch Now
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <button className="btn-secondary">
              Load More Webinars
            </button>
          </div>
        </div>
      </section>

      {/* Newsletter Signup */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Never Miss a Webinar
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Subscribe to our newsletter to get notified about upcoming webinars 
            and exclusive AI insights from our experts.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="w-full px-4 py-3 rounded-lg border border-secondary-600 bg-secondary-800 text-white placeholder-secondary-400 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
            <button className="btn-primary whitespace-nowrap">
              Subscribe
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
