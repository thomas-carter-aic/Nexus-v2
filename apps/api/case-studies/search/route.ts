import { NextRequest, NextResponse } from 'next/server'
import Fuse from 'fuse.js'
import { getPublishedCaseStudies } from '@/data/case-studies'
import { CaseStudySearchResult } from '@/types/case-studies'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const query = searchParams.get('q')
    const limit = parseInt(searchParams.get('limit') || '10')
    const industry = searchParams.get('industry')
    const clientSize = searchParams.get('clientSize')
    const useCase = searchParams.get('useCase')

    let studies = getPublishedCaseStudies()

    // Apply filters
    if (industry) {
      studies = studies.filter(study => 
        study.industry.toLowerCase() === industry.toLowerCase()
      )
    }

    if (clientSize) {
      studies = studies.filter(study => 
        study.client.size.toLowerCase() === clientSize.toLowerCase()
      )
    }

    if (useCase) {
      studies = studies.filter(study => 
        study.useCase.toLowerCase().includes(useCase.toLowerCase())
      )
    }

    // If no search query, return filtered results
    if (!query || query.trim().length < 2) {
      return NextResponse.json({
        results: studies.slice(0, limit).map(study => ({
          study,
          score: 1,
          matches: {}
        })),
        total: studies.length,
        query: query || '',
        filters: { industry, clientSize, useCase }
      })
    }

    // Configure Fuse.js for fuzzy search
    const fuse = new Fuse(studies, {
      keys: [
        { name: 'title', weight: 0.4 },
        { name: 'excerpt', weight: 0.3 },
        { name: 'industry', weight: 0.1 },
        { name: 'useCase', weight: 0.1 },
        { name: 'tags', weight: 0.1 }
      ],
      threshold: 0.4,
      includeScore: true,
      includeMatches: true,
    })

    const searchResults = fuse.search(query.trim())

    // Transform results
    const results: CaseStudySearchResult[] = searchResults.slice(0, limit).map(result => {
      const study = result.item
      
      // Determine what matched
      const matches = {
        title: false,
        excerpt: false,
        content: false,
        tags: false,
        industry: false
      }

      if (result.matches) {
        result.matches.forEach(match => {
          if (match.key === 'title') matches.title = true
          if (match.key === 'excerpt') matches.excerpt = true
          if (match.key === 'content') matches.content = true
          if (match.key === 'tags') matches.tags = true
          if (match.key === 'industry') matches.industry = true
        })
      }

      return {
        study,
        score: result.score || 0,
        matches
      }
    })

    return NextResponse.json({
      results,
      total: searchResults.length,
      query: query.trim(),
      filters: { industry, clientSize, useCase }
    })
  } catch (error) {
    console.error('Error searching case studies:', error)
    return NextResponse.json(
      { error: 'Failed to search case studies' },
      { status: 500 }
    )
  }
}
