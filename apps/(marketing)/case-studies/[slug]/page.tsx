import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { getCaseStudyBySlug, getPublishedCaseStudies, getCaseStudiesByIndustry } from '@/data/case-studies'
import { CaseStudyContent } from '@/components/case-studies/CaseStudyContent'

interface CaseStudyPageProps {
  params: Promise<{
    slug: string
  }>
}

export async function generateMetadata({ params }: CaseStudyPageProps): Promise<Metadata> {
  const { slug } = await params
  const study = getCaseStudyBySlug(slug)
  
  if (!study) {
    return {
      title: 'Case Study Not Found - Applied Innovations Corporation',
    }
  }

  return {
    title: study.seo?.metaTitle || `${study.title} | Applied Innovations Corporation`,
    description: study.seo?.metaDescription || study.excerpt,
    keywords: study.seo?.metaKeywords || study.tags.join(', '),
    openGraph: {
      title: study.title,
      description: study.excerpt,
      type: 'article',
      images: study.featuredImage ? [study.featuredImage.url] : [],
    },
  }
}

export async function generateStaticParams() {
  const studies = getPublishedCaseStudies()
  return studies.map((study) => ({
    slug: study.slug,
  }))
}

export default async function CaseStudyPage({ params }: CaseStudyPageProps) {
  const { slug } = await params
  const study = getCaseStudyBySlug(slug)

  if (!study) {
    notFound()
  }

  // Get related case studies from the same industry
  const relatedStudies = getCaseStudiesByIndustry(study.industry)
    .filter(s => s.id !== study.id)
    .slice(0, 3)

  return (
    <div className="bg-white">
      <div className="section-padding">
        <div className="container">
          <CaseStudyContent 
            study={study}
            relatedStudies={relatedStudies}
          />
        </div>
      </div>
    </div>
  )
}
