import type { Metadata } from 'next';
import { FileText, Download, Calendar, User, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Whitepapers - Applied Innovations Corporation',
  description: 'Download our comprehensive whitepapers on AI strategy, implementation best practices, and industry insights.',
};

const whitepapers = [
  {
    id: 1,
    title: 'The Executive\'s Guide to AI Transformation',
    description: 'A comprehensive guide for business leaders on planning and executing successful AI transformation initiatives.',
    author: 'Dr. Sarah Chen',
    date: '2024-06-01',
    pages: 32,
    category: 'Strategy',
    featured: true,
    topics: ['AI Strategy', 'Digital Transformation', 'Leadership', 'ROI Analysis'],
  },
  {
    id: 2,
    title: 'Building Ethical AI: Framework for Responsible Implementation',
    description: 'Best practices and frameworks for implementing AI systems that are fair, transparent, and aligned with ethical principles.',
    author: 'Michael Rodriguez',
    date: '2024-05-15',
    pages: 28,
    category: 'Ethics',
    featured: true,
    topics: ['AI Ethics', 'Governance', 'Compliance', 'Risk Management'],
  },
  {
    id: 3,
    title: 'AI in Healthcare: Opportunities and Challenges',
    description: 'Exploring the transformative potential of AI in healthcare while addressing regulatory and implementation challenges.',
    author: 'Dr. Priya Patel',
    date: '2024-04-20',
    pages: 24,
    category: 'Industry',
    featured: false,
    topics: ['Healthcare AI', 'Regulatory Compliance', 'Patient Privacy', 'Clinical Applications'],
  },
  {
    id: 4,
    title: 'Small Business AI: Getting Started Without Breaking the Bank',
    description: 'Practical strategies for small and medium businesses to implement AI solutions cost-effectively.',
    author: 'James Thompson',
    date: '2024-04-10',
    pages: 20,
    category: 'SMB',
    featured: false,
    topics: ['SMB Strategy', 'Cost-Effective AI', 'Implementation', 'Quick Wins'],
  },
  {
    id: 5,
    title: 'The Future of Work: AI and Human Collaboration',
    description: 'How AI is reshaping the workplace and strategies for successful human-AI collaboration.',
    author: 'Dr. Sarah Chen',
    date: '2024-03-25',
    pages: 26,
    category: 'Future of Work',
    featured: false,
    topics: ['Future of Work', 'Human-AI Collaboration', 'Workforce Development', 'Change Management'],
  },
  {
    id: 6,
    title: 'Data Security in AI Systems: Best Practices Guide',
    description: 'Comprehensive security practices for protecting data in AI implementations and maintaining compliance.',
    author: 'Michael Rodriguez',
    date: '2024-03-10',
    pages: 30,
    category: 'Security',
    featured: false,
    topics: ['Data Security', 'Privacy Protection', 'Compliance', 'Risk Mitigation'],
  },
];

export default function WhitepapersPage() {
  const featuredPapers = whitepapers.filter(paper => paper.featured);
  const regularPapers = whitepapers.filter(paper => !paper.featured);

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl mb-6">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Whitepapers
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Download our comprehensive whitepapers on AI strategy, implementation best practices, 
              and industry insights from our team of experts.
            </p>
          </div>
        </div>
      </section>

      {/* Featured Whitepapers */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Featured Whitepapers</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Our most popular and impactful research and insights
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {featuredPapers.map((paper) => (
              <div key={paper.id} className="bg-white border border-secondary-200 rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-shadow">
                <div className="h-48 bg-gradient-to-br from-primary-100 to-secondary-100 flex items-center justify-center">
                  <div className="text-center">
                    <FileText className="w-16 h-16 text-primary-600 mx-auto mb-3" />
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      {paper.category}
                    </span>
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex items-center space-x-4 text-sm text-secondary-600 mb-3">
                    <div className="flex items-center">
                      <User className="w-4 h-4 mr-1" />
                      {paper.author}
                    </div>
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(paper.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </div>
                    <span>{paper.pages} pages</span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-secondary-900 mb-3">
                    {paper.title}
                  </h3>
                  
                  <p className="text-secondary-600 mb-4">
                    {paper.description}
                  </p>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {paper.topics.map((topic, index) => (
                      <span key={index} className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-secondary-100 text-secondary-700">
                        {topic}
                      </span>
                    ))}
                  </div>

                  <button className="btn-primary w-full">
                    <Download className="w-4 h-4 mr-2" />
                    Download Whitepaper
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* All Whitepapers */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">All Whitepapers</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Browse our complete collection of research and insights
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {regularPapers.map((paper) => (
              <div key={paper.id} className="bg-white rounded-lg p-6 shadow-sm hover:shadow-lg transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                    {paper.category}
                  </span>
                  <span className="text-xs text-secondary-500">{paper.pages} pages</span>
                </div>
                
                <h3 className="text-lg font-semibold text-secondary-900 mb-2">
                  {paper.title}
                </h3>
                
                <p className="text-sm text-secondary-600 mb-4">
                  {paper.description}
                </p>

                <div className="flex items-center justify-between text-xs text-secondary-600 mb-4">
                  <span>{paper.author}</span>
                  <span>{new Date(paper.date).toLocaleDateString()}</span>
                </div>

                <div className="flex flex-wrap gap-1 mb-4">
                  {paper.topics.slice(0, 2).map((topic, index) => (
                    <span key={index} className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-secondary-100 text-secondary-700">
                      {topic}
                    </span>
                  ))}
                  {paper.topics.length > 2 && (
                    <span className="text-xs text-secondary-500">+{paper.topics.length - 2} more</span>
                  )}
                </div>

                <button className="btn-secondary w-full text-sm">
                  <Download className="w-4 h-4 mr-2" />
                  Download
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Signup */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Stay Updated
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Subscribe to our newsletter to be notified when we publish new whitepapers 
            and research insights.
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
