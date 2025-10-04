export interface CaseStudy {
  id: string
  title: string
  slug: string
  excerpt: string
  content: string
  client: {
    name: string
    industry: string
    size: 'startup' | 'smb' | 'enterprise' | 'fortune500'
    logo?: string
  }
  challenge: string
  solution: string
  results: {
    metric: string
    value: string
    description: string
  }[]
  technologies: string[]
  timeline: string
  teamSize: string
  featuredImage?: {
    url: string
    alt: string
  }
  gallery?: {
    url: string
    alt: string
    caption?: string
  }[]
  testimonial?: {
    quote: string
    author: string
    title: string
    avatar?: string
  }
  tags: string[]
  industry: string
  useCase: string
  status: 'draft' | 'published' | 'featured'
  publishedDate: string
  lastUpdated: string
  readTime: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  seo?: {
    metaTitle?: string
    metaDescription?: string
    metaKeywords?: string
  }
}

export interface CaseStudyCategory {
  id: string
  name: string
  description: string
  icon: string
  color: string
  studies: CaseStudy[]
}

export interface CaseStudyFilters {
  industry?: string
  useCase?: string
  clientSize?: string
  technology?: string
  difficulty?: string
}

export interface CaseStudySearchResult {
  study: CaseStudy
  score: number
  matches: {
    title?: boolean
    excerpt?: boolean
    content?: boolean
    tags?: boolean
    industry?: boolean
  }
}
