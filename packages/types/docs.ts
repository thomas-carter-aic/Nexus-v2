export interface DocSection {
  id: string
  title: string
  description: string
  icon: string
  color: string
  order: number
  articles: DocArticle[]
}

export interface DocArticle {
  id: string
  title: string
  description: string
  slug: string
  content: string
  sectionId: string
  order: number
  tags: string[]
  lastUpdated: string
  readTime: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  prerequisites?: string[]
  relatedArticles?: string[]
}

export interface DocNavigation {
  sections: DocSection[]
}

export interface SearchResult {
  article: DocArticle
  section: DocSection
  score: number
  matches: {
    title?: boolean
    description?: boolean
    content?: boolean
    tags?: boolean
  }
}
