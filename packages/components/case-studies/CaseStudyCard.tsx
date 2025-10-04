'use client'

import Link from 'next/link'
import Image from 'next/image'
import { Clock, ArrowRight, Building, TrendingUp } from 'lucide-react'
import { CaseStudy } from '@/types/case-studies'

interface CaseStudyCardProps {
  study: CaseStudy
  featured?: boolean
}

export function CaseStudyCard({ study, featured = false }: CaseStudyCardProps) {
  const cardClasses = featured 
    ? "bg-white border-2 border-primary-200 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 group"
    : "bg-white border border-secondary-200 rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 group"

  return (
    <div className={cardClasses}>
      {/* Featured Image */}
      {study.featuredImage && (
        <div className={`relative ${featured ? 'h-64' : 'h-48'} overflow-hidden`}>
          <Image
            src={study.featuredImage.url}
            alt={study.featuredImage.alt}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
          />
          {featured && (
            <div className="absolute top-4 left-4">
              <span className="bg-primary-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                Featured
              </span>
            </div>
          )}
          <div className="absolute top-4 right-4">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              study.difficulty === 'beginner' ? 'bg-green-100 text-green-700' :
              study.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
              'bg-red-100 text-red-700'
            }`}>
              {study.difficulty}
            </span>
          </div>
        </div>
      )}

      <div className={`p-${featured ? '8' : '6'}`}>
        {/* Client Info */}
        <div className="flex items-center mb-4">
          <Building className="w-4 h-4 text-secondary-500 mr-2" />
          <span className="text-sm text-secondary-600">
            {study.client.name} • {study.client.industry}
          </span>
          <span className={`ml-auto px-2 py-1 rounded text-xs font-medium ${
            study.client.size === 'startup' ? 'bg-blue-100 text-blue-700' :
            study.client.size === 'smb' ? 'bg-green-100 text-green-700' :
            study.client.size === 'enterprise' ? 'bg-purple-100 text-purple-700' :
            'bg-orange-100 text-orange-700'
          }`}>
            {study.client.size.toUpperCase()}
          </span>
        </div>

        {/* Title */}
        <h3 className={`font-bold text-secondary-900 mb-3 group-hover:text-primary-600 transition-colors ${
          featured ? 'text-2xl' : 'text-xl'
        }`}>
          {study.title}
        </h3>

        {/* Excerpt */}
        <p className={`text-secondary-600 mb-4 ${featured ? 'text-base' : 'text-sm'}`}>
          {study.excerpt}
        </p>

        {/* Key Results */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {study.results.slice(0, 2).map((result, index) => (
            <div key={index} className="text-center p-3 bg-secondary-50 rounded-lg">
              <div className="flex items-center justify-center mb-1">
                <TrendingUp className="w-4 h-4 text-primary-600 mr-1" />
                <span className="text-lg font-bold text-primary-600">
                  {result.value}
                </span>
              </div>
              <p className="text-xs text-secondary-600">{result.metric}</p>
            </div>
          ))}
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {study.tags.slice(0, 3).map((tag, index) => (
            <span
              key={index}
              className="bg-secondary-100 text-secondary-700 px-2 py-1 rounded text-xs"
            >
              {tag}
            </span>
          ))}
          {study.tags.length > 3 && (
            <span className="text-secondary-500 text-xs">
              +{study.tags.length - 3} more
            </span>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between">
          <div className="flex items-center text-sm text-secondary-600">
            <Clock className="w-4 h-4 mr-1" />
            {study.readTime} min read
          </div>
          <Link
            href={`/case-studies/${study.slug}`}
            className="flex items-center text-primary-600 hover:text-primary-700 font-medium text-sm group-hover:translate-x-1 transition-transform"
          >
            Read Full Case Study
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
        </div>
      </div>
    </div>
  )
}
