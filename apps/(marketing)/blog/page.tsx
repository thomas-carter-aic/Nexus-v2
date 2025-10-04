import type { Metadata } from 'next';
import { Calendar, User, ArrowRight, Search, Filter } from 'lucide-react';
import { BlogClient } from '@/components/blog/BlogClient';
import { BlogPost } from '@/types/blog';

export const metadata: Metadata = {
  title: 'News & Insights - Applied Innovations Corporation',
  description: 'Latest news, insights, and thought leadership on AI transformation, industry trends, and best practices.',
};

async function getBlogPosts(): Promise<BlogPost[]> {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_PAYLOAD_URL || 'http://localhost:3000';
    const response = await fetch(`${baseUrl}/api/blog?limit=20`, {
      next: { revalidate: 300 }, // Revalidate every 5 minutes
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch blog posts');
    }
    
    const data = await response.json();
    return data.docs || [];
  } catch (error) {
    console.error('Error fetching blog posts:', error);
    return [];
  }
}

export default async function BlogPage() {
  const blogPosts = await getBlogPosts();

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              News & Insights
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Stay informed with the latest AI trends, best practices, and thought leadership 
              from our team of experts and industry leaders.
            </p>
          </div>
        </div>
      </section>

      {/* Blog Content */}
      <BlogClient initialPosts={blogPosts} />

      {/* Newsletter Signup */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Stay Informed
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Subscribe to our newsletter for the latest AI insights, industry trends, 
            and expert analysis delivered to your inbox.
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
