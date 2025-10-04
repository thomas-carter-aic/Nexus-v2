import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { getArticleBySlug, allArticles } from '@/data/docs'
import { DocsContent } from '@/components/docs/DocsContent'

interface DocsArticlePageProps {
  params: Promise<{
    slug: string
  }>
}

export async function generateMetadata({ params }: DocsArticlePageProps): Promise<Metadata> {
  const { slug } = await params
  const article = getArticleBySlug(slug)
  
  if (!article) {
    return {
      title: 'Article Not Found - Applied Innovations Corporation',
    }
  }

  return {
    title: `${article.title} - Documentation | Applied Innovations Corporation`,
    description: article.description,
    keywords: article.tags.join(', '),
    openGraph: {
      title: article.title,
      description: article.description,
      type: 'article',
    },
  }
}

export async function generateStaticParams() {
  return allArticles.map((article) => ({
    slug: article.slug,
  }))
}

export default async function DocsArticlePage({ params }: DocsArticlePageProps) {
  const { slug } = await params
  const article = getArticleBySlug(slug)

  if (!article) {
    notFound()
  }

  // Find previous and next articles in the same section
  const sectionArticles = allArticles
    .filter(a => a.sectionId === article.sectionId)
    .sort((a, b) => a.order - b.order)
  
  const currentIndex = sectionArticles.findIndex(a => a.id === article.id)
  const previousArticle = currentIndex > 0 ? sectionArticles[currentIndex - 1] : undefined
  const nextArticle = currentIndex < sectionArticles.length - 1 ? sectionArticles[currentIndex + 1] : undefined

  return (
    <DocsContent 
      article={article}
      previousArticle={previousArticle}
      nextArticle={nextArticle}
    />
  )
}
