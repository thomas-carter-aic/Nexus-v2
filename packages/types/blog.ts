export interface BlogPost {
  id: string
  title: string
  slug: string
  excerpt: string
  content: any // Rich text content
  featuredImage?: {
    id: string
    url: string
    alt: string
    width?: number
    height?: number
  }
  author: {
    id: string
    name: string
    email: string
  }
  category: 'ai-ml' | 'automation' | 'digital-transformation' | 'industry-insights' | 'case-studies' | 'technology' | 'business-strategy'
  tags?: Array<{ tag: string }>
  status: 'draft' | 'published' | 'archived'
  publishedDate?: string
  readTime?: number
  seo?: {
    metaTitle?: string
    metaDescription?: string
    metaKeywords?: string
  }
  createdAt: string
  updatedAt: string
}

export interface BlogPostsResponse {
  docs: BlogPost[]
  totalDocs: number
  limit: number
  totalPages: number
  page: number
  pagingCounter: number
  hasPrevPage: boolean
  hasNextPage: boolean
  prevPage?: number
  nextPage?: number
}

export interface BlogCategory {
  label: string
  value: string
  count?: number
}
