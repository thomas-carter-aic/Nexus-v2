import { NextRequest, NextResponse } from 'next/server'
import Fuse from 'fuse.js'
import { allArticles, docSections } from '@/data/docs'
import { SearchResult } from '@/types/docs'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const query = searchParams.get('q')
    const limit = parseInt(searchParams.get('limit') || '10')
    const section = searchParams.get('section')

    if (!query || query.trim().length < 2) {
      return NextResponse.json({
        results: [],
        total: 0,
        query: query || ''
      })
    }

    // Filter articles by section if specified
    let articlesToSearch = allArticles
    if (section) {
      articlesToSearch = allArticles.filter(article => article.sectionId === section)
    }

    // Configure Fuse.js for fuzzy search
    const fuse = new Fuse(articlesToSearch, {
      keys: [
        { name: 'title', weight: 0.4 },
        { name: 'description', weight: 0.3 },
        { name: 'content', weight: 0.2 },
        { name: 'tags', weight: 0.1 }
      ],
      threshold: 0.4,
      includeScore: true,
      includeMatches: true,
    })

    const searchResults = fuse.search(query.trim())

    // Transform results
    const results: SearchResult[] = searchResults.slice(0, limit).map(result => {
      const article = result.item
      const section = docSections.find(s => s.id === article.sectionId)!
      
      // Determine what matched
      const matches = {
        title: false,
        description: false,
        content: false,
        tags: false
      }

      if (result.matches) {
        result.matches.forEach(match => {
          if (match.key === 'title') matches.title = true
          if (match.key === 'description') matches.description = true
          if (match.key === 'content') matches.content = true
          if (match.key === 'tags') matches.tags = true
        })
      }

      return {
        article,
        section,
        score: result.score || 0,
        matches
      }
    })

    return NextResponse.json({
      results,
      total: searchResults.length,
      query: query.trim()
    })
  } catch (error) {
    console.error('Error searching documentation:', error)
    return NextResponse.json(
      { error: 'Failed to search documentation' },
      { status: 500 }
    )
  }
}
