import type { Metadata } from 'next';
import Link from 'next/link';
import { Search, Filter, TrendingUp, Building, Clock } from 'lucide-react';
import { CaseStudyCard } from '@/components/case-studies/CaseStudyCard';
import { getFeaturedCaseStudies, getPublishedCaseStudies, caseStudyCategories, getCaseStudyStats } from '@/data/case-studies';

export const metadata: Metadata = {
  title: 'Case Studies - Applied Innovations Corporation',
  description: 'Explore real-world AI transformation success stories. See how our clients achieved measurable results with AI solutions across healthcare, finance, manufacturing, and retail.',
  keywords: 'AI case studies, AI success stories, AI transformation, healthcare AI, fintech AI, manufacturing AI, retail AI',
};

export default function CaseStudiesPage() {
  const featuredStudies = getFeaturedCaseStudies(3);
  const allStudies = getPublishedCaseStudies();
  const stats = getCaseStudyStats();

  const getIconComponent = (iconName: string) => {
    const iconMap: { [key: string]: string } = {
      'Heart': '❤️',
      'DollarSign': '💰',
      'Settings': '⚙️',
      'ShoppingCart': '🛒'
    }
    return iconMap[iconName] || '📊'
  }

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Success Stories
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Discover how leading organizations are transforming their businesses with AI. 
              Real results, measurable impact, proven solutions.
            </p>
            
            {/* Stats */}
            <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">{stats.total}</div>
                <div className="text-sm text-secondary-600">Case Studies</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">{stats.industries}</div>
                <div className="text-sm text-secondary-600">Industries</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">{stats.featured}</div>
                <div className="text-sm text-secondary-600">Featured</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">{stats.avgReadTime}</div>
                <div className="text-sm text-secondary-600">Avg Read Time</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Search and Filter */}
      <section className="py-8 bg-white border-b border-secondary-200">
        <div className="container">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
              <input
                type="text"
                placeholder="Search case studies..."
                className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div className="flex items-center space-x-4">
              <select className="border border-secondary-300 rounded-lg px-3 py-2 text-sm">
                <option>All Industries</option>
                <option>Healthcare</option>
                <option>Financial Services</option>
                <option>Manufacturing</option>
                <option>Retail</option>
              </select>
              <select className="border border-secondary-300 rounded-lg px-3 py-2 text-sm">
                <option>All Company Sizes</option>
                <option>Startup</option>
                <option>SMB</option>
                <option>Enterprise</option>
                <option>Fortune 500</option>
              </select>
              <button className="btn-secondary text-sm">
                <Filter className="w-4 h-4 mr-2" />
                Filter
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Case Studies */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Featured Success Stories</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Our most impactful AI transformations delivering exceptional business results
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
            {featuredStudies.map((study) => (
              <CaseStudyCard key={study.id} study={study} featured={true} />
            ))}
          </div>
        </div>
      </section>

      {/* Industry Categories */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Solutions by Industry</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Explore AI transformations across different industries and use cases
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {caseStudyCategories.map((category) => (
              <div key={category.id} className="bg-white rounded-lg p-6 text-center hover:shadow-lg transition-shadow">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full mb-4 ${category.color}`}>
                  <span className="text-3xl">{getIconComponent(category.icon)}</span>
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                  {category.name}
                </h3>
                <p className="text-secondary-600 text-sm mb-4">
                  {category.description}
                </p>
                <div className="text-2xl font-bold text-primary-600 mb-2">
                  {category.studies.length}
                </div>
                <div className="text-xs text-secondary-500 mb-4">
                  Case Studies Available
                </div>
                <Link
                  href={`/case-studies?industry=${category.id}`}
                  className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  View Studies →
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* All Case Studies */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">All Case Studies</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Browse our complete collection of AI transformation success stories
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {allStudies.slice(0, 9).map((study) => (
              <CaseStudyCard key={study.id} study={study} />
            ))}
          </div>

          {allStudies.length > 9 && (
            <div className="text-center mt-12">
              <button className="btn-primary">
                Load More Case Studies
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Results Showcase */}
      <section className="section-padding bg-secondary-900 text-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Proven Results Across Industries</h2>
            <p className="text-lg text-secondary-300 max-w-2xl mx-auto">
              Our AI solutions deliver measurable business impact for organizations of all sizes
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <TrendingUp className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <div className="text-3xl font-bold text-white mb-2">89%</div>
              <div className="text-secondary-300">Average Efficiency Gain</div>
            </div>
            <div className="text-center">
              <Building className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <div className="text-3xl font-bold text-white mb-2">$12M+</div>
              <div className="text-secondary-300">Total Cost Savings</div>
            </div>
            <div className="text-center">
              <Clock className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <div className="text-3xl font-bold text-white mb-2">65%</div>
              <div className="text-secondary-300">Faster Processing</div>
            </div>
            <div className="text-center">
              <TrendingUp className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <div className="text-3xl font-bold text-white mb-2">98%</div>
              <div className="text-secondary-300">Client Satisfaction</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-gradient-to-r from-primary-50 to-secondary-50">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-secondary-900 mb-6">
            Ready to Write Your Success Story?
          </h2>
          <p className="text-lg text-secondary-600 mb-8 max-w-2xl mx-auto">
            Join the growing number of organizations transforming their business with AI. 
            Let's discuss how we can help you achieve similar results.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/consultation" className="btn-primary">
              Schedule Free Consultation
            </Link>
            <Link href="/contact" className="btn-secondary">
              Contact Our Team
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
