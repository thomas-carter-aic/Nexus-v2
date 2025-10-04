'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { ChevronDown, ChevronRight, Search, X } from 'lucide-react'
import { DocSection, DocArticle } from '@/types/docs'
import { docSections, searchArticles } from '@/data/docs'

interface DocsSidebarProps {
  isOpen: boolean
  onClose: () => void
}

export function DocsSidebar({ isOpen, onClose }: DocsSidebarProps) {
  const pathname = usePathname()
  const [expandedSections, setExpandedSections] = useState<string[]>(['getting-started'])
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<DocArticle[]>([])

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev =>
      prev.includes(sectionId)
        ? prev.filter(id => id !== sectionId)
        : [...prev, sectionId]
    )
  }

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    if (query.trim()) {
      const results = searchArticles(query)
      setSearchResults(results)
    } else {
      setSearchResults([])
    }
  }

  const clearSearch = () => {
    setSearchQuery('')
    setSearchResults([])
  }

  const getIconComponent = (iconName: string) => {
    // This is a simplified icon mapping - you might want to use a proper icon library
    const iconMap: { [key: string]: string } = {
      'Zap': '⚡',
      'Code': '💻',
      'Users': '👥',
      'FileText': '📄'
    }
    return iconMap[iconName] || '📄'
  }

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={`
        fixed top-0 left-0 h-full w-80 bg-white border-r border-secondary-200 z-50 transform transition-transform duration-300 ease-in-out
        lg:relative lg:translate-x-0 lg:z-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-secondary-200">
            <h2 className="text-lg font-semibold text-secondary-900">Documentation</h2>
            <button
              onClick={onClose}
              className="lg:hidden p-1 hover:bg-secondary-100 rounded"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Search */}
          <div className="p-4 border-b border-secondary-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
              <input
                type="text"
                placeholder="Search documentation..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                className="w-full pl-10 pr-10 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
              />
              {searchQuery && (
                <button
                  onClick={clearSearch}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 hover:bg-secondary-100 rounded"
                >
                  <X className="w-3 h-3 text-secondary-400" />
                </button>
              )}
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto">
            {searchResults.length > 0 ? (
              /* Search Results */
              <div className="p-4">
                <h3 className="text-sm font-medium text-secondary-700 mb-3">
                  Search Results ({searchResults.length})
                </h3>
                <div className="space-y-2">
                  {searchResults.map((article) => (
                    <Link
                      key={article.id}
                      href={`/docs/${article.slug}`}
                      onClick={onClose}
                      className={`
                        block p-3 rounded-lg hover:bg-secondary-50 transition-colors
                        ${pathname === `/docs/${article.slug}` ? 'bg-primary-50 border-l-4 border-primary-500' : ''}
                      `}
                    >
                      <div className="text-sm font-medium text-secondary-900">
                        {article.title}
                      </div>
                      <div className="text-xs text-secondary-600 mt-1">
                        {article.description}
                      </div>
                      <div className="flex items-center mt-2 text-xs text-secondary-500">
                        <span className="bg-secondary-100 px-2 py-1 rounded">
                          {article.difficulty}
                        </span>
                        <span className="ml-2">{article.readTime} min read</span>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            ) : (
              /* Navigation */
              <nav className="p-4">
                {docSections.map((section) => (
                  <div key={section.id} className="mb-4">
                    <button
                      onClick={() => toggleSection(section.id)}
                      className="flex items-center justify-between w-full p-2 text-left hover:bg-secondary-50 rounded-lg transition-colors"
                    >
                      <div className="flex items-center">
                        <span className="text-lg mr-3">{getIconComponent(section.icon)}</span>
                        <span className="font-medium text-secondary-900">{section.title}</span>
                      </div>
                      {expandedSections.includes(section.id) ? (
                        <ChevronDown className="w-4 h-4 text-secondary-500" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-secondary-500" />
                      )}
                    </button>
                    
                    {expandedSections.includes(section.id) && (
                      <div className="ml-6 mt-2 space-y-1">
                        {section.articles.map((article) => (
                          <Link
                            key={article.id}
                            href={`/docs/${article.slug}`}
                            onClick={onClose}
                            className={`
                              block p-2 text-sm rounded hover:bg-secondary-50 transition-colors
                              ${pathname === `/docs/${article.slug}` 
                                ? 'bg-primary-50 text-primary-700 font-medium border-l-2 border-primary-500 pl-3' 
                                : 'text-secondary-700 hover:text-secondary-900'
                              }
                            `}
                          >
                            <div className="flex items-center justify-between">
                              <span>{article.title}</span>
                              <div className="flex items-center space-x-2">
                                <span className={`
                                  px-1.5 py-0.5 text-xs rounded
                                  ${article.difficulty === 'beginner' ? 'bg-green-100 text-green-700' :
                                    article.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-red-100 text-red-700'
                                  }
                                `}>
                                  {article.difficulty}
                                </span>
                              </div>
                            </div>
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </nav>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
