import type { Metadata } from 'next';
import Link from 'next/link';
import { Book, Search, ArrowRight, Clock, Star } from 'lucide-react';
import { docSections, allArticles } from '@/data/docs';

export const metadata: Metadata = {
  title: 'Documentation - Applied Innovations Corporation',
  description: 'Comprehensive documentation, guides, and API references for the Applied Innovations AI platform and services.',
};

export default function DocsPage() {
  // Get popular articles (first few from each section)
  const popularArticles = docSections.flatMap(section => 
    section.articles.slice(0, 2)
  ).slice(0, 6);

  // Get recent articles (sorted by last updated)
  const recentArticles = [...allArticles]
    .sort((a, b) => new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime())
    .slice(0, 4);

  const getIconComponent = (iconName: string) => {
    const iconMap: { [key: string]: string } = {
      'Zap': '⚡',
      'Code': '💻',
      'Users': '👥',
      'FileText': '📄'
    }
    return iconMap[iconName] || '📄'
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-6">
          <Book className="w-8 h-8 text-primary-600" />
        </div>
        <h1 className="text-4xl font-bold text-secondary-900 mb-4">
          Documentation
        </h1>
        <p className="text-xl text-secondary-600 max-w-3xl mx-auto mb-8">
          Everything you need to know about the Applied Innovations Nexus platform. 
          From quick start guides to advanced API references.
        </p>
        
        {/* Quick Search */}
        <div className="max-w-md mx-auto relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-secondary-400" />
          <input
            type="text"
            placeholder="Search documentation..."
            className="w-full pl-12 pr-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-lg"
          />
        </div>
      </div>

      {/* Documentation Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
        {docSections.map((section) => (
          <div key={section.id} className="bg-white border border-secondary-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-start mb-4">
              <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg mr-4 ${section.color}`}>
                <span className="text-2xl">{getIconComponent(section.icon)}</span>
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                  {section.title}
                </h3>
                <p className="text-secondary-600 mb-4">
                  {section.description}
                </p>
              </div>
            </div>
            
            <div className="space-y-3">
              {section.articles.slice(0, 3).map((article) => (
                <Link
                  key={article.id}
                  href={`/docs/${article.slug}`}
                  className="flex items-center justify-between p-3 hover:bg-secondary-50 rounded-lg transition-colors group"
                >
                  <div className="flex-1">
                    <div className="font-medium text-secondary-900 group-hover:text-primary-600">
                      {article.title}
                    </div>
                    <div className="text-sm text-secondary-600 mt-1">
                      {article.description}
                    </div>
                    <div className="flex items-center mt-2 text-xs text-secondary-500">
                      <Clock className="w-3 h-3 mr-1" />
                      {article.readTime} min
                      <span className={`ml-3 px-2 py-0.5 rounded ${
                        article.difficulty === 'beginner' ? 'bg-green-100 text-green-700' :
                        article.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                        {article.difficulty}
                      </span>
                    </div>
                  </div>
                  <ArrowRight className="w-4 h-4 text-secondary-400 group-hover:text-primary-600 group-hover:translate-x-1 transition-all" />
                </Link>
              ))}
              
              {section.articles.length > 3 && (
                <Link
                  href={`/docs#${section.id}`}
                  className="block text-center py-2 text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  View all {section.articles.length} articles →
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Popular Articles */}
      <div className="mb-16">
        <div className="flex items-center mb-8">
          <Star className="w-6 h-6 text-yellow-500 mr-3" />
          <h2 className="text-2xl font-bold text-secondary-900">Popular Articles</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {popularArticles.map((article) => (
            <Link
              key={article.id}
              href={`/docs/${article.slug}`}
              className="block bg-white border border-secondary-200 rounded-lg p-6 hover:shadow-lg hover:border-primary-300 transition-all group"
            >
              <h3 className="font-semibold text-secondary-900 mb-2 group-hover:text-primary-600">
                {article.title}
              </h3>
              <p className="text-secondary-600 text-sm mb-4 line-clamp-2">
                {article.description}
              </p>
              <div className="flex items-center justify-between text-xs text-secondary-500">
                <div className="flex items-center">
                  <Clock className="w-3 h-3 mr-1" />
                  {article.readTime} min read
                </div>
                <span className={`px-2 py-1 rounded ${
                  article.difficulty === 'beginner' ? 'bg-green-100 text-green-700' :
                  article.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-red-100 text-red-700'
                }`}>
                  {article.difficulty}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Recently Updated */}
      <div className="mb-16">
        <h2 className="text-2xl font-bold text-secondary-900 mb-8">Recently Updated</h2>
        <div className="space-y-4">
          {recentArticles.map((article) => (
            <Link
              key={article.id}
              href={`/docs/${article.slug}`}
              className="flex items-center justify-between p-4 bg-white border border-secondary-200 rounded-lg hover:shadow-md hover:border-primary-300 transition-all group"
            >
              <div className="flex-1">
                <h3 className="font-semibold text-secondary-900 mb-1 group-hover:text-primary-600">
                  {article.title}
                </h3>
                <p className="text-secondary-600 text-sm mb-2">
                  {article.description}
                </p>
                <div className="flex items-center text-xs text-secondary-500">
                  <span>Updated {new Date(article.lastUpdated).toLocaleDateString()}</span>
                  <span className="mx-2">•</span>
                  <Clock className="w-3 h-3 mr-1" />
                  {article.readTime} min read
                  <span className="mx-2">•</span>
                  <span className={`px-2 py-0.5 rounded ${
                    article.difficulty === 'beginner' ? 'bg-green-100 text-green-700' :
                    article.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {article.difficulty}
                  </span>
                </div>
              </div>
              <ArrowRight className="w-5 h-5 text-secondary-400 group-hover:text-primary-600 group-hover:translate-x-1 transition-all ml-4" />
            </Link>
          ))}
        </div>
      </div>

      {/* Quick Links */}
      <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg p-8 text-center">
        <h2 className="text-2xl font-bold text-secondary-900 mb-4">Need Help?</h2>
        <p className="text-secondary-600 mb-6 max-w-2xl mx-auto">
          Can't find what you're looking for? Our support team is here to help you get the most out of the Nexus platform.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/support"
            className="btn-primary"
          >
            Contact Support
          </Link>
          <Link
            href="/consultation"
            className="btn-secondary"
          >
            Schedule Consultation
          </Link>
        </div>
      </div>
    </div>
  );
}
