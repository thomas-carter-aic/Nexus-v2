import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { Calendar, User, Clock, ArrowLeft, Share2 } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';
import { BlogPost } from '@/types/blog';

interface BlogPostPageProps {
  params: Promise<{
    slug: string
  }>
}

async function getBlogPost(slug: string): Promise<BlogPost | null> {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_PAYLOAD_URL || 'http://localhost:3000';
    const response = await fetch(`${baseUrl}/api/blog/${slug}`, {
      next: { revalidate: 300 }, // Revalidate every 5 minutes
    });
    
    if (!response.ok) {
      return null;
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching blog post:', error);
    return null;
  }
}

export async function generateMetadata({ params }: BlogPostPageProps): Promise<Metadata> {
  const { slug } = await params
  const post = await getBlogPost(slug);
  
  if (!post) {
    return {
      title: 'Blog Post Not Found - Applied Innovations Corporation',
    };
  }

  return {
    title: post.seo?.metaTitle || `${post.title} - Applied Innovations Corporation`,
    description: post.seo?.metaDescription || post.excerpt,
    keywords: post.seo?.metaKeywords,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: post.featuredImage ? [post.featuredImage.url] : [],
    },
  };
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

// Helper function to render rich text content
function renderRichText(content: any) {
  // Handle HTML string content
  if (typeof content === 'string') {
    return (
      <div 
        className="prose prose-lg max-w-none prose-headings:text-secondary-900 prose-p:text-secondary-700 prose-a:text-primary-600 prose-strong:text-secondary-900 prose-ul:text-secondary-700 prose-ol:text-secondary-700"
        dangerouslySetInnerHTML={{ __html: content }} 
      />
    );
  }
  
  // Handle Lexical editor format (if needed in the future)
  if (content && content.root && content.root.children) {
    return (
      <div className="prose prose-lg max-w-none">
        {content.root.children.map((child: any, index: number) => (
          <div key={index}>
            {child.children?.map((textNode: any, textIndex: number) => (
              <span key={textIndex}>{textNode.text}</span>
            ))}
          </div>
        ))}
      </div>
    );
  }
  
  return <div className="prose prose-lg max-w-none">Content not available</div>;
}

export default async function BlogPostPage({ params }: BlogPostPageProps) {
  const { slug } = await params
  const post = await getBlogPost(slug);

  if (!post) {
    notFound();
  }

  return (
    <div className="bg-white">
      {/* Header */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <Link 
              href="/blog"
              className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-8"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Blog
            </Link>
            
            <div className="mb-6">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 mb-4">
                {categoryLabels[post.category] || post.category}
              </span>
              
              <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-5xl mb-6">
                {post.title}
              </h1>
              
              <p className="text-xl text-secondary-600 mb-8">
                {post.excerpt}
              </p>
              
              <div className="flex flex-wrap items-center gap-6 text-sm text-secondary-600">
                <div className="flex items-center">
                  <User className="w-4 h-4 mr-2" />
                  {post.author.name}
                </div>
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 mr-2" />
                  {new Date(post.publishedDate || post.createdAt).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </div>
                {post.readTime && (
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-2" />
                    {post.readTime} min read
                  </div>
                )}
                <button className="flex items-center text-primary-600 hover:text-primary-700">
                  <Share2 className="w-4 h-4 mr-2" />
                  Share
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Image */}
      {post.featuredImage && (
        <section className="py-8">
          <div className="container">
            <div className="max-w-4xl mx-auto">
              <div className="relative h-96 rounded-lg overflow-hidden">
                <Image
                  src={post.featuredImage.url}
                  alt={post.featuredImage.alt}
                  fill
                  className="object-cover"
                />
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Content */}
      <section className="section-padding">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <div className="prose prose-lg max-w-none">
              {renderRichText(post.content)}
            </div>
            
            {/* Tags */}
            {post.tags && post.tags.length > 0 && (
              <div className="mt-12 pt-8 border-t border-secondary-200">
                <h3 className="text-lg font-semibold text-secondary-900 mb-4">Tags</h3>
                <div className="flex flex-wrap gap-2">
                  {post.tags.map((tagObj, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-secondary-100 text-secondary-700"
                    >
                      {tagObj.tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Author Bio */}
      <section className="py-16 bg-secondary-50">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg p-8 shadow-sm">
              <h3 className="text-xl font-bold text-secondary-900 mb-4">About the Author</h3>
              <div className="flex items-start space-x-4">
                <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-full flex items-center justify-center">
                  <User className="w-8 h-8 text-secondary-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-secondary-900">{post.author.name}</h4>
                  <p className="text-secondary-600 mt-2">
                    Expert in AI transformation and digital innovation with extensive experience 
                    helping organizations implement cutting-edge technology solutions.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Related Posts CTA */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Explore More Insights
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Discover more articles on AI transformation, industry trends, and best practices.
          </p>
          <Link href="/blog" className="btn-primary">
            View All Articles
          </Link>
        </div>
      </section>
    </div>
  );
}
