'use client';

import { useState, useMemo } from 'react';
import { Calendar, User, ArrowRight, Search, Filter } from 'lucide-react';
import { BlogPost } from '@/types/blog';
import Link from 'next/link';
import Image from 'next/image';

interface BlogClientProps {
  initialPosts: BlogPost[];
}

const categoryLabels: Record<string, string> = {
  'ai-ml': 'AI & Machine Learning',
  'automation': 'Automation',
  'digital-transformation': 'Digital Transformation',
  'industry-insights': 'Industry Insights',
  'case-studies': 'Case Studies',
  'technology': 'Technology',
  'business-strategy': 'Business Strategy',
};

export function BlogClient({ initialPosts }: BlogClientProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  const filteredPosts = useMemo(() => {
    return initialPosts.filter(post => {
      const matchesSearch = searchTerm === '' || 
        post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.excerpt.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesCategory = selectedCategory === '' || post.category === selectedCategory;
      
      return matchesSearch && matchesCategory;
    });
  }, [initialPosts, searchTerm, selectedCategory]);

  // For demo purposes, we'll consider the first 2 posts as featured
  const featuredPosts = filteredPosts.slice(0, 2);
  const regularPosts = filteredPosts.slice(2);

  const categories = Array.from(new Set(initialPosts.map(post => post.category)));

  return (
    <>
      {/* Search and Filter */}
      <section className="py-8 bg-white border-b border-secondary-200">
        <div className="container">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
              <input
                type="text"
                placeholder="Search articles..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div className="flex items-center space-x-4">
              <select 
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="border border-secondary-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="">All Categories</option>
                {categories.map(category => (
                  <option key={category} value={category}>
                    {categoryLabels[category] || category}
                  </option>
                ))}
              </select>
              <button 
                onClick={() => {
                  setSearchTerm('');
                  setSelectedCategory('');
                }}
                className="btn-secondary text-sm"
              >
                <Filter className="w-4 h-4 mr-2" />
                Clear
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Posts */}
      {featuredPosts.length > 0 && (
        <section className="section-padding bg-white">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-secondary-900 mb-4">Featured Articles</h2>
              <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
                Our most popular and impactful content
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {featuredPosts.map((post) => (
                <article key={post.id} className="bg-white border border-secondary-200 rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-shadow">
                  {post.featuredImage ? (
                    <div className="h-48 relative">
                      <Image
                        src={post.featuredImage.url}
                        alt={post.featuredImage.alt}
                        fill
                        className="object-cover"
                      />
                    </div>
                  ) : (
                    <div className="h-48 bg-gradient-to-br from-primary-100 to-secondary-100"></div>
                  )}
                  <div className="p-6">
                    <div className="flex items-center space-x-4 text-sm text-secondary-600 mb-3">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        {categoryLabels[post.category] || post.category}
                      </span>
                      <div className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {new Date(post.publishedDate || post.createdAt).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                        })}
                      </div>
                      {post.readTime && <span>{post.readTime} min read</span>}
                    </div>
                    
                    <h3 className="text-xl font-bold text-secondary-900 mb-3">
                      {post.title}
                    </h3>
                    
                    <p className="text-secondary-600 mb-4">
                      {post.excerpt}
                    </p>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center text-sm text-secondary-600">
                        <User className="w-4 h-4 mr-1" />
                        {post.author.name}
                      </div>
                      <Link 
                        href={`/blog/${post.slug}`}
                        className="flex items-center text-primary-600 hover:text-primary-700 text-sm font-medium"
                      >
                        Read More
                        <ArrowRight className="w-4 h-4 ml-1" />
                      </Link>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Regular Posts */}
      {regularPosts.length > 0 && (
        <section className="section-padding gradient-bg">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-secondary-900 mb-4">Latest Articles</h2>
              <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
                Stay up to date with our latest insights and analysis
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {regularPosts.map((post) => (
                <article key={post.id} className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-shadow">
                  {post.featuredImage ? (
                    <div className="h-32 relative">
                      <Image
                        src={post.featuredImage.url}
                        alt={post.featuredImage.alt}
                        fill
                        className="object-cover"
                      />
                    </div>
                  ) : (
                    <div className="h-32 bg-gradient-to-br from-secondary-100 to-primary-100"></div>
                  )}
                  <div className="p-6">
                    <div className="flex items-center justify-between text-xs text-secondary-600 mb-3">
                      <span className="inline-flex items-center px-2 py-1 rounded-full bg-secondary-100 text-secondary-700">
                        {categoryLabels[post.category] || post.category}
                      </span>
                      {post.readTime && <span>{post.readTime} min read</span>}
                    </div>
                    
                    <h3 className="text-lg font-semibold text-secondary-900 mb-2">
                      <Link href={`/blog/${post.slug}`} className="hover:text-primary-600">
                        {post.title}
                      </Link>
                    </h3>
                    
                    <p className="text-sm text-secondary-600 mb-4">
                      {post.excerpt}
                    </p>

                    <div className="flex items-center justify-between text-xs text-secondary-600">
                      <span>{post.author.name}</span>
                      <span>{new Date(post.publishedDate || post.createdAt).toLocaleDateString()}</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* No Results */}
      {filteredPosts.length === 0 && (
        <section className="section-padding bg-white">
          <div className="container text-center">
            <h2 className="text-2xl font-bold text-secondary-900 mb-4">No articles found</h2>
            <p className="text-secondary-600 mb-8">
              Try adjusting your search terms or category filter.
            </p>
            <button 
              onClick={() => {
                setSearchTerm('');
                setSelectedCategory('');
              }}
              className="btn-primary"
            >
              Clear Filters
            </button>
          </div>
        </section>
      )}
    </>
  );
}
