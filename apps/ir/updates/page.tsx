import type { Metadata } from 'next';
import { Calendar, TrendingUp, Users, DollarSign, Award, FileText, ExternalLink } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Company Updates - Investor Relations',
  description: 'Latest company updates, announcements, and communications for Applied Innovations Corporation investors.',
};

const updates = [
  {
    id: 1,
    date: '2024-07-01',
    type: 'earnings',
    title: 'Q2 2024 Earnings Report Released',
    summary: 'Applied Innovations Corporation reports strong Q2 2024 results with 45% revenue growth and expanded client base.',
    content: `We are pleased to announce our Q2 2024 financial results, which demonstrate continued strong growth and market expansion.

Key Highlights:
• Revenue increased 45% year-over-year to $12.3M
• Client base grew to 500+ active customers
• Launched 3 new AI solutions in healthcare and finance
• Achieved 98.5% customer satisfaction rating
• Expanded team by 35% with key hires in R&D and sales

Our Nexus platform continues to gain traction in the enterprise market, with several Fortune 500 companies adopting our AI transformation solutions. We remain confident in our ability to execute on our growth strategy and deliver value to our stakeholders.`,
    attachments: [
      { name: 'Q2 2024 Earnings Report.pdf', size: '2.1 MB' },
      { name: 'Financial Statements.xlsx', size: '856 KB' },
    ],
    tags: ['Earnings', 'Financial Results', 'Growth'],
  },
  {
    id: 2,
    date: '2024-06-15',
    type: 'partnership',
    title: 'Strategic Partnership with Microsoft Azure',
    summary: 'New partnership expands our AI platform capabilities and market reach through Microsoft Azure integration.',
    content: `Applied Innovations Corporation is excited to announce a strategic partnership with Microsoft Azure to enhance our AI platform capabilities and accelerate market expansion.

Partnership Benefits:
• Integration with Azure AI services and infrastructure
• Access to Microsoft's enterprise customer network
• Joint go-to-market initiatives in key verticals
• Enhanced security and compliance capabilities
• Preferred partner status in Azure Marketplace

This partnership positions us to better serve enterprise customers and accelerate our growth in the AI transformation market. We expect this collaboration to contribute significantly to our revenue growth in the coming quarters.`,
    attachments: [
      { name: 'Partnership Announcement.pdf', size: '1.3 MB' },
    ],
    tags: ['Partnership', 'Microsoft', 'Platform'],
  },
  {
    id: 3,
    date: '2024-05-30',
    type: 'product',
    title: 'Nexus 3.0 Platform Launch',
    summary: 'Major platform update introduces advanced AI capabilities, improved user experience, and enterprise-grade security.',
    content: `We are thrilled to announce the launch of Nexus 3.0, our most advanced AI platform to date, featuring significant enhancements in capability, usability, and security.

New Features:
• Advanced multi-modal AI capabilities
• Real-time collaboration tools
• Enhanced security and compliance framework
• Improved user interface and experience
• Advanced analytics and reporting
• API-first architecture for better integrations

Early customer feedback has been overwhelmingly positive, with beta users reporting 40% improvement in productivity and 60% reduction in implementation time. The platform is now available to all customers with a phased rollout plan.`,
    attachments: [
      { name: 'Nexus 3.0 Feature Overview.pdf', size: '3.2 MB' },
      { name: 'Technical Specifications.pdf', size: '1.8 MB' },
    ],
    tags: ['Product Launch', 'Nexus Platform', 'Innovation'],
  },
  {
    id: 4,
    date: '2024-05-15',
    type: 'funding',
    title: 'Series B Funding Round Completed',
    summary: '$25M Series B funding round led by Andreessen Horowitz to accelerate growth and product development.',
    content: `Applied Innovations Corporation has successfully completed a $25 million Series B funding round led by Andreessen Horowitz, with participation from existing investors including Sequoia Capital and Accel Partners.

Funding Details:
• Total raised: $25 million
• Lead investor: Andreessen Horowitz
• Participating investors: Sequoia Capital, Accel Partners
• Post-money valuation: $150 million
• Use of funds: Product development, market expansion, team growth

The funding will be used to accelerate product development, expand our sales and marketing efforts, and grow our engineering team. We plan to use the capital to further develop our AI platform and expand into new market segments.`,
    attachments: [
      { name: 'Series B Announcement.pdf', size: '1.1 MB' },
      { name: 'Investor Presentation.pdf', size: '4.5 MB' },
    ],
    tags: ['Funding', 'Series B', 'Investment'],
  },
  {
    id: 5,
    date: '2024-04-20',
    type: 'award',
    title: 'Named to Forbes AI 50 List',
    summary: 'Applied Innovations Corporation recognized as one of the most promising AI companies by Forbes.',
    content: `We are honored to announce that Applied Innovations Corporation has been named to the Forbes AI 50 list, recognizing the most promising artificial intelligence companies in North America.

Recognition Highlights:
• Selected from over 2,500 AI companies
• Recognized for innovation in enterprise AI transformation
• Highlighted for strong customer growth and satisfaction
• Noted for ethical AI practices and governance
• Featured for technical excellence and platform capabilities

This recognition validates our mission to democratize AI and our commitment to helping businesses transform through artificial intelligence. We thank our customers, partners, and team members who have made this achievement possible.`,
    attachments: [
      { name: 'Forbes AI 50 Article.pdf', size: '892 KB' },
    ],
    tags: ['Award', 'Recognition', 'Forbes'],
  },
];

const getTypeIcon = (type: string) => {
  switch (type) {
    case 'earnings':
      return <DollarSign className="w-5 h-5 text-green-600" />;
    case 'partnership':
      return <Users className="w-5 h-5 text-blue-600" />;
    case 'product':
      return <TrendingUp className="w-5 h-5 text-purple-600" />;
    case 'funding':
      return <DollarSign className="w-5 h-5 text-yellow-600" />;
    case 'award':
      return <Award className="w-5 h-5 text-orange-600" />;
    default:
      return <FileText className="w-5 h-5 text-secondary-600" />;
  }
};

const getTypeBadge = (type: string) => {
  const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";
  switch (type) {
    case 'earnings':
      return `${baseClasses} bg-green-100 text-green-800`;
    case 'partnership':
      return `${baseClasses} bg-blue-100 text-blue-800`;
    case 'product':
      return `${baseClasses} bg-purple-100 text-purple-800`;
    case 'funding':
      return `${baseClasses} bg-yellow-100 text-yellow-800`;
    case 'award':
      return `${baseClasses} bg-orange-100 text-orange-800`;
    default:
      return `${baseClasses} bg-secondary-100 text-secondary-800`;
  }
};

export default function InvestorUpdatesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-secondary-900">Company Updates</h1>
        <p className="text-secondary-600">
          Latest news, announcements, and communications from Applied Innovations Corporation.
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg border border-secondary-200 p-4">
        <div className="flex items-center space-x-4">
          <select className="border border-secondary-300 rounded-lg px-3 py-2 text-sm">
            <option>All Updates</option>
            <option>Earnings</option>
            <option>Partnerships</option>
            <option>Product</option>
            <option>Funding</option>
            <option>Awards</option>
          </select>
          <select className="border border-secondary-300 rounded-lg px-3 py-2 text-sm">
            <option>All Time</option>
            <option>Last 30 days</option>
            <option>Last 90 days</option>
            <option>Last 6 months</option>
            <option>Last year</option>
          </select>
        </div>
      </div>

      {/* Updates List */}
      <div className="space-y-6">
        {updates.map((update) => (
          <div key={update.id} className="bg-white rounded-lg border border-secondary-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                {getTypeIcon(update.type)}
                <div>
                  <h3 className="text-lg font-semibold text-secondary-900">{update.title}</h3>
                  <div className="flex items-center space-x-3 mt-1">
                    <div className="flex items-center text-sm text-secondary-600">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(update.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </div>
                    <span className={getTypeBadge(update.type)}>
                      {update.type.charAt(0).toUpperCase() + update.type.slice(1)}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <p className="text-secondary-700 mb-4">{update.summary}</p>

            <div className="prose prose-sm max-w-none text-secondary-700 mb-6">
              {update.content.split('\n').map((paragraph, index) => (
                <p key={index} className="mb-3 last:mb-0">
                  {paragraph}
                </p>
              ))}
            </div>

            {/* Tags */}
            <div className="flex items-center space-x-2 mb-4">
              {update.tags.map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-secondary-100 text-secondary-700"
                >
                  {tag}
                </span>
              ))}
            </div>

            {/* Attachments */}
            {update.attachments && update.attachments.length > 0 && (
              <div className="border-t border-secondary-200 pt-4">
                <h4 className="text-sm font-medium text-secondary-900 mb-3">Attachments</h4>
                <div className="space-y-2">
                  {update.attachments.map((attachment, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                      <div className="flex items-center">
                        <FileText className="w-4 h-4 text-secondary-600 mr-2" />
                        <div>
                          <p className="text-sm font-medium text-secondary-900">{attachment.name}</p>
                          <p className="text-xs text-secondary-600">{attachment.size}</p>
                        </div>
                      </div>
                      <button className="flex items-center text-sm text-primary-600 hover:text-primary-700">
                        Download
                        <ExternalLink className="w-3 h-3 ml-1" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Load More */}
      <div className="text-center">
        <button className="btn-secondary">
          Load More Updates
        </button>
      </div>
    </div>
  );
}
