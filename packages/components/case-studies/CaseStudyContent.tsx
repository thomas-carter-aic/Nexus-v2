'use client'

import { ReactNode } from 'react'
import Image from 'next/image'
import { Clock, Calendar, Tag, ArrowLeft, Building, TrendingUp, Users, Timer, Quote } from 'lucide-react'
import Link from 'next/link'
import { CaseStudy } from '@/types/case-studies'
import { CodeBlock } from '@/components/docs/CodeBlock'

interface CaseStudyContentProps {
  study: CaseStudy
  relatedStudies?: CaseStudy[]
}

export function CaseStudyContent({ study, relatedStudies = [] }: CaseStudyContentProps) {
  // Parse markdown-like content and convert to JSX (similar to docs content parser)
  const parseContent = (content: string): ReactNode => {
    const lines = content.split('\n')
    const elements: ReactNode[] = []
    let currentCodeBlock = ''
    let currentLanguage = ''
    let inCodeBlock = false

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]

      // Handle code blocks
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          elements.push(
            <CodeBlock key={i} language={currentLanguage}>
              {currentCodeBlock.trim()}
            </CodeBlock>
          )
          currentCodeBlock = ''
          currentLanguage = ''
          inCodeBlock = false
        } else {
          currentLanguage = line.slice(3).trim()
          inCodeBlock = true
        }
        continue
      }

      if (inCodeBlock) {
        currentCodeBlock += line + '\n'
        continue
      }

      // Handle headings
      if (line.startsWith('# ')) {
        elements.push(
          <h1 key={i} className="text-3xl font-bold text-secondary-900 mb-6 mt-8 first:mt-0">
            {line.slice(2)}
          </h1>
        )
      } else if (line.startsWith('## ')) {
        elements.push(
          <h2 key={i} className="text-2xl font-semibold text-secondary-900 mb-4 mt-8">
            {line.slice(3)}
          </h2>
        )
      } else if (line.startsWith('### ')) {
        elements.push(
          <h3 key={i} className="text-xl font-semibold text-secondary-900 mb-3 mt-6">
            {line.slice(4)}
          </h3>
        )
      } else if (line.startsWith('#### ')) {
        elements.push(
          <h4 key={i} className="text-lg font-semibold text-secondary-900 mb-2 mt-4">
            {line.slice(5)}
          </h4>
        )
      }
      // Handle regular paragraphs and other content
      else if (line.trim() && !line.startsWith('#')) {
        // Handle bold text
        if (line.includes('**')) {
          const parts = line.split('**')
          const processedParts = parts.map((part, idx) => 
            idx % 2 === 1 ? <strong key={idx} className="font-semibold text-secondary-900">{part}</strong> : part
          )
          elements.push(
            <p key={i} className="mb-4 text-secondary-700 leading-relaxed">
              {processedParts}
            </p>
          )
        } else {
          elements.push(
            <p key={i} className="mb-4 text-secondary-700 leading-relaxed">
              {line}
            </p>
          )
        }
      }
    }

    return elements
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Back Navigation */}
      <div className="mb-8">
        <Link
          href="/case-studies"
          className="inline-flex items-center text-primary-600 hover:text-primary-700 group"
        >
          <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
          Back to Case Studies
        </Link>
      </div>

      {/* Header */}
      <div className="mb-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <h1 className="text-4xl font-bold text-secondary-900 mb-6">
              {study.title}
            </h1>
            <p className="text-xl text-secondary-600 mb-6">
              {study.excerpt}
            </p>
            
            {/* Meta Information */}
            <div className="flex flex-wrap items-center gap-6 text-sm text-secondary-600 mb-8">
              <div className="flex items-center">
                <Building className="w-4 h-4 mr-2" />
                {study.client.name}
              </div>
              <div className="flex items-center">
                <Clock className="w-4 h-4 mr-2" />
                {study.readTime} min read
              </div>
              <div className="flex items-center">
                <Calendar className="w-4 h-4 mr-2" />
                {new Date(study.publishedDate).toLocaleDateString()}
              </div>
              <div className="flex items-center">
                <Users className="w-4 h-4 mr-2" />
                {study.teamSize}
              </div>
              <div className="flex items-center">
                <Timer className="w-4 h-4 mr-2" />
                {study.timeline}
              </div>
            </div>

            {/* Tags */}
            <div className="flex items-center mb-8">
              <Tag className="w-4 h-4 mr-2 text-secondary-500" />
              <div className="flex flex-wrap gap-2">
                {study.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="bg-secondary-100 text-secondary-700 px-3 py-1 rounded-full text-sm"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Client Info Card */}
            <div className="bg-white border border-secondary-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-secondary-900 mb-4">Client Overview</h3>
              <div className="space-y-3">
                <div>
                  <span className="text-sm text-secondary-600">Company:</span>
                  <p className="font-medium text-secondary-900">{study.client.name}</p>
                </div>
                <div>
                  <span className="text-sm text-secondary-600">Industry:</span>
                  <p className="font-medium text-secondary-900">{study.client.industry}</p>
                </div>
                <div>
                  <span className="text-sm text-secondary-600">Size:</span>
                  <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                    study.client.size === 'startup' ? 'bg-blue-100 text-blue-700' :
                    study.client.size === 'smb' ? 'bg-green-100 text-green-700' :
                    study.client.size === 'enterprise' ? 'bg-purple-100 text-purple-700' :
                    'bg-orange-100 text-orange-700'
                  }`}>
                    {study.client.size.toUpperCase()}
                  </span>
                </div>
                <div>
                  <span className="text-sm text-secondary-600">Use Case:</span>
                  <p className="font-medium text-secondary-900">{study.useCase}</p>
                </div>
              </div>
            </div>

            {/* Key Results */}
            <div className="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-secondary-900 mb-4">Key Results</h3>
              <div className="space-y-4">
                {study.results.map((result, index) => (
                  <div key={index} className="flex items-start">
                    <TrendingUp className="w-5 h-5 text-primary-600 mr-3 mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="text-2xl font-bold text-primary-600 mb-1">
                        {result.value}
                      </div>
                      <div className="text-sm font-medium text-secondary-900 mb-1">
                        {result.metric}
                      </div>
                      <div className="text-xs text-secondary-600">
                        {result.description}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Featured Image */}
      {study.featuredImage && (
        <div className="mb-12">
          <div className="relative h-96 rounded-lg overflow-hidden">
            <Image
              src={study.featuredImage.url}
              alt={study.featuredImage.alt}
              fill
              className="object-cover"
            />
          </div>
        </div>
      )}

      {/* Challenge, Solution, Results Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-red-900 mb-3">The Challenge</h3>
          <p className="text-red-800 text-sm">{study.challenge}</p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">Our Solution</h3>
          <p className="text-blue-800 text-sm">{study.solution}</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-green-900 mb-3">Technologies Used</h3>
          <div className="flex flex-wrap gap-1">
            {study.technologies.map((tech, index) => (
              <span
                key={index}
                className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs"
              >
                {tech}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="prose prose-lg max-w-none mb-12">
        {parseContent(study.content)}
      </div>

      {/* Testimonial */}
      {study.testimonial && (
        <div className="bg-secondary-900 text-white rounded-lg p-8 mb-12">
          <Quote className="w-8 h-8 text-primary-400 mb-4" />
          <blockquote className="text-xl italic mb-6">
            "{study.testimonial.quote}"
          </blockquote>
          <div className="flex items-center">
            {study.testimonial.avatar && (
              <div className="relative w-12 h-12 rounded-full overflow-hidden mr-4">
                <Image
                  src={study.testimonial.avatar}
                  alt={study.testimonial.author}
                  fill
                  className="object-cover"
                />
              </div>
            )}
            <div>
              <div className="font-semibold">{study.testimonial.author}</div>
              <div className="text-secondary-300 text-sm">{study.testimonial.title}</div>
            </div>
          </div>
        </div>
      )}

      {/* Image Gallery */}
      {study.gallery && study.gallery.length > 0 && (
        <div className="mb-12">
          <h3 className="text-2xl font-semibold text-secondary-900 mb-6">Project Gallery</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {study.gallery.map((image, index) => (
              <div key={index} className="relative">
                <div className="relative h-64 rounded-lg overflow-hidden">
                  <Image
                    src={image.url}
                    alt={image.alt}
                    fill
                    className="object-cover"
                  />
                </div>
                {image.caption && (
                  <p className="text-sm text-secondary-600 mt-2 text-center">
                    {image.caption}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Related Case Studies */}
      {relatedStudies.length > 0 && (
        <div className="border-t border-secondary-200 pt-12">
          <h3 className="text-2xl font-semibold text-secondary-900 mb-8">Related Case Studies</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {relatedStudies.map((relatedStudy) => (
              <Link
                key={relatedStudy.id}
                href={`/case-studies/${relatedStudy.slug}`}
                className="block bg-white border border-secondary-200 rounded-lg p-6 hover:shadow-lg transition-shadow"
              >
                <h4 className="font-semibold text-secondary-900 mb-2 hover:text-primary-600">
                  {relatedStudy.title}
                </h4>
                <p className="text-sm text-secondary-600 mb-3">
                  {relatedStudy.excerpt.substring(0, 100)}...
                </p>
                <div className="flex items-center text-xs text-secondary-500">
                  <span>{relatedStudy.client.industry}</span>
                  <span className="mx-2">•</span>
                  <span>{relatedStudy.readTime} min read</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-lg p-8 text-center mt-12">
        <h3 className="text-2xl font-bold mb-4">Ready to Transform Your Business?</h3>
        <p className="text-lg mb-6 opacity-90">
          Let's discuss how AI can drive similar results for your organization.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/consultation" className="btn-white">
            Schedule Consultation
          </Link>
          <Link href="/case-studies" className="btn-outline-white">
            View More Case Studies
          </Link>
        </div>
      </div>
    </div>
  )
}
