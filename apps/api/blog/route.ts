import { NextRequest, NextResponse } from 'next/server'
import { getBlogPosts, getBlogPostsByCategory } from '@/data/blog-posts'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '10')
    const category = searchParams.get('category')
    
    let posts = category ? getBlogPostsByCategory(category) : getBlogPosts()
    
    // Sort by published date (newest first)
    posts = posts.sort((a, b) => 
      new Date(b.publishedDate || b.createdAt).getTime() - 
      new Date(a.publishedDate || a.createdAt).getTime()
    )
    
    // Pagination
    const startIndex = (page - 1) * limit
    const endIndex = startIndex + limit
    const paginatedPosts = posts.slice(startIndex, endIndex)
    
    const response = {
      docs: paginatedPosts,
      totalDocs: posts.length,
      limit,
      totalPages: Math.ceil(posts.length / limit),
      page,
      pagingCounter: startIndex + 1,
      hasPrevPage: page > 1,
      hasNextPage: endIndex < posts.length,
      prevPage: page > 1 ? page - 1 : null,
      nextPage: endIndex < posts.length ? page + 1 : null,
    }
    
    return NextResponse.json(response)
  } catch (error) {
    console.error('Error fetching blog posts:', error)
    return NextResponse.json(
      { error: 'Failed to fetch blog posts' },
      { status: 500 }
    )
  }
}
