'use client'

import { ReactNode } from 'react'
import { DocArticle } from '@/types/docs'
import { CodeBlock } from './CodeBlock'
import { Clock, Calendar, Tag, ArrowLeft, ArrowRight } from 'lucide-react'
import Link from 'next/link'

interface DocsContentProps {
  article: DocArticle
  previousArticle?: DocArticle
  nextArticle?: DocArticle
}

export function DocsContent({ article, previousArticle, nextArticle }: DocsContentProps) {
  // Parse markdown-like content and convert to JSX
  const parseContent = (content: string): ReactNode => {
    const lines = content.split('\n')
    const elements: ReactNode[] = []
    let currentCodeBlock = ''
    let currentLanguage = ''
    let inCodeBlock = false
    let currentList: string[] = []
    let inList = false

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]

      // Handle code blocks
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          // End code block
          elements.push(
            <CodeBlock key={i} language={currentLanguage}>
              {currentCodeBlock.trim()}
            </CodeBlock>
          )
          currentCodeBlock = ''
          currentLanguage = ''
          inCodeBlock = false
        } else {
          // Start code block
          currentLanguage = line.slice(3).trim()
          inCodeBlock = true
        }
        continue
      }

      if (inCodeBlock) {
        currentCodeBlock += line + '\n'
        continue
      }

      // Handle lists
      if (line.startsWith('- ') || line.startsWith('* ')) {
        if (!inList) {
          inList = true
          currentList = []
        }
        currentList.push(line.slice(2).trim())
        continue
      } else if (inList && line.trim() === '') {
        // Continue list
        continue
      } else if (inList) {
        // End list
        elements.push(
          <ul key={i} className="list-disc list-inside space-y-2 mb-6 text-secondary-700">
            {currentList.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        )
        currentList = []
        inList = false
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
      // Handle inline code
      else if (line.includes('`') && !line.startsWith('```')) {
        const parts = line.split('`')
        const processedParts = parts.map((part, idx) => 
          idx % 2 === 1 ? (
            <code key={idx} className="bg-secondary-100 text-secondary-800 px-1.5 py-0.5 rounded text-sm font-mono">
              {part}
            </code>
          ) : part
        )
        elements.push(
          <p key={i} className="mb-4 text-secondary-700 leading-relaxed">
            {processedParts}
          </p>
        )
      }
      // Handle bold text
      else if (line.includes('**')) {
        const parts = line.split('**')
        const processedParts = parts.map((part, idx) => 
          idx % 2 === 1 ? <strong key={idx} className="font-semibold text-secondary-900">{part}</strong> : part
        )
        elements.push(
          <p key={i} className="mb-4 text-secondary-700 leading-relaxed">
            {processedParts}
          </p>
        )
      }
      // Handle regular paragraphs
      else if (line.trim() && !line.startsWith('#')) {
        elements.push(
          <p key={i} className="mb-4 text-secondary-700 leading-relaxed">
            {line}
          </p>
        )
      }
      // Handle empty lines
      else if (line.trim() === '') {
        elements.push(<div key={i} className="mb-2" />)
      }
    }

    // Handle any remaining list
    if (inList && currentList.length > 0) {
      elements.push(
        <ul key="final-list" className="list-disc list-inside space-y-2 mb-6 text-secondary-700">
          {currentList.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      )
    }

    return elements
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Article Header */}
      <div className="mb-8 pb-8 border-b border-secondary-200">
        <h1 className="text-4xl font-bold text-secondary-900 mb-4">
          {article.title}
        </h1>
        <p className="text-xl text-secondary-600 mb-6">
          {article.description}
        </p>
        
        {/* Article Meta */}
        <div className="flex flex-wrap items-center gap-6 text-sm text-secondary-600">
          <div className="flex items-center">
            <Clock className="w-4 h-4 mr-2" />
            {article.readTime} min read
          </div>
          <div className="flex items-center">
            <Calendar className="w-4 h-4 mr-2" />
            Updated {new Date(article.lastUpdated).toLocaleDateString()}
          </div>
          <div className={`
            px-3 py-1 rounded-full text-xs font-medium
            ${article.difficulty === 'beginner' ? 'bg-green-100 text-green-700' :
              article.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
              'bg-red-100 text-red-700'
            }
          `}>
            {article.difficulty}
          </div>
        </div>

        {/* Tags */}
        {article.tags.length > 0 && (
          <div className="flex items-center mt-4">
            <Tag className="w-4 h-4 mr-2 text-secondary-500" />
            <div className="flex flex-wrap gap-2">
              {article.tags.map((tag, index) => (
                <span
                  key={index}
                  className="bg-secondary-100 text-secondary-700 px-2 py-1 rounded text-xs"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Prerequisites */}
        {article.prerequisites && article.prerequisites.length > 0 && (
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="text-sm font-semibold text-blue-900 mb-2">Prerequisites</h3>
            <p className="text-sm text-blue-800">
              Before reading this article, make sure you're familiar with:{' '}
              {article.prerequisites.join(', ')}
            </p>
          </div>
        )}
      </div>

      {/* Article Content */}
      <div className="prose prose-lg max-w-none">
        {parseContent(article.content)}
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center mt-12 pt-8 border-t border-secondary-200">
        <div className="flex-1">
          {previousArticle && (
            <Link
              href={`/docs/${previousArticle.slug}`}
              className="flex items-center text-primary-600 hover:text-primary-700 group"
            >
              <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
              <div>
                <div className="text-sm text-secondary-600">Previous</div>
                <div className="font-medium">{previousArticle.title}</div>
              </div>
            </Link>
          )}
        </div>
        
        <div className="flex-1 text-right">
          {nextArticle && (
            <Link
              href={`/docs/${nextArticle.slug}`}
              className="flex items-center justify-end text-primary-600 hover:text-primary-700 group"
            >
              <div className="text-right">
                <div className="text-sm text-secondary-600">Next</div>
                <div className="font-medium">{nextArticle.title}</div>
              </div>
              <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
          )}
        </div>
      </div>

      {/* Related Articles */}
      {article.relatedArticles && article.relatedArticles.length > 0 && (
        <div className="mt-12 p-6 bg-secondary-50 rounded-lg">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">Related Articles</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {article.relatedArticles.map((relatedSlug, index) => (
              <Link
                key={index}
                href={`/docs/${relatedSlug}`}
                className="block p-4 bg-white rounded border hover:border-primary-300 hover:shadow-sm transition-all"
              >
                <div className="font-medium text-secondary-900">Related Article {index + 1}</div>
                <div className="text-sm text-secondary-600 mt-1">Click to read more</div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
