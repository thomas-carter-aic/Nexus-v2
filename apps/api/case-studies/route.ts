import { NextRequest, NextResponse } from 'next/server'
import { getPublishedCaseStudies, getFeaturedCaseStudies, getCaseStudiesByIndustry } from '@/data/case-studies'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const featured = searchParams.get('featured') === 'true'
    const industry = searchParams.get('industry')
    const limit = parseInt(searchParams.get('limit') || '10')
    const offset = parseInt(searchParams.get('offset') || '0')

    let studies = getPublishedCaseStudies()

    // Filter by featured
    if (featured) {
      studies = getFeaturedCaseStudies()
    }

    // Filter by industry
    if (industry) {
      studies = getCaseStudiesByIndustry(industry)
    }

    // Apply pagination
    const paginatedStudies = studies.slice(offset, offset + limit)

    return NextResponse.json({
      studies: paginatedStudies,
      total: studies.length,
      limit,
      offset,
      hasMore: offset + limit < studies.length
    })
  } catch (error) {
    console.error('Error fetching case studies:', error)
    return NextResponse.json(
      { error: 'Failed to fetch case studies' },
      { status: 500 }
    )
  }
}
