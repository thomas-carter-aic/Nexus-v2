import { CaseStudy, CaseStudyCategory } from '@/types/case-studies'
import { healthcareCaseStudies } from './healthcare'
import { financialCaseStudies } from './financial'

// Additional case studies for other industries
const manufacturingCaseStudies: CaseStudy[] = [
  {
    id: 'smart-manufacturing-optimization',
    title: 'Smart Manufacturing: 40% Efficiency Gain with Predictive Maintenance',
    slug: 'smart-manufacturing-optimization',
    excerpt: 'How a leading automotive manufacturer reduced downtime by 65% and increased overall equipment effectiveness by 40% using AI-powered predictive maintenance.',
    client: {
      name: 'AutoTech Manufacturing',
      industry: 'Manufacturing',
      size: 'enterprise'
    },
    challenge: 'Frequent unexpected equipment failures causing production delays and high maintenance costs.',
    solution: 'Implemented IoT sensors and AI algorithms to predict equipment failures before they occur.',
    results: [
      {
        metric: 'Downtime Reduction',
        value: '65%',
        description: 'Decrease in unplanned equipment downtime'
      },
      {
        metric: 'OEE Improvement',
        value: '40%',
        description: 'Overall Equipment Effectiveness increase'
      },
      {
        metric: 'Maintenance Cost Savings',
        value: '$3.2M',
        description: 'Annual reduction in maintenance expenses'
      }
    ],
    technologies: ['IoT Sensors', 'Predictive Analytics', 'Machine Learning', 'Digital Twin'],
    timeline: '10 months',
    teamSize: '15 specialists',
    tags: ['Predictive Maintenance', 'IoT', 'Manufacturing', 'Industry 4.0'],
    industry: 'Manufacturing',
    useCase: 'Predictive Maintenance',
    status: 'published',
    publishedDate: '2024-04-10T11:00:00Z',
    lastUpdated: '2024-06-15T09:30:00Z',
    readTime: 14,
    difficulty: 'advanced',
    content: `# Smart Manufacturing Case Study Content...`,
    seo: {
      metaTitle: 'Manufacturing AI Case Study: 40% Efficiency Gain | AIC',
      metaDescription: 'Learn how AutoTech Manufacturing achieved 65% downtime reduction and 40% efficiency improvement with AI-powered predictive maintenance.',
      metaKeywords: 'manufacturing AI, predictive maintenance, Industry 4.0, IoT sensors'
    }
  }
]

const retailCaseStudies: CaseStudy[] = [
  {
    id: 'retail-personalization-engine',
    title: 'E-commerce Giant Boosts Revenue 32% with AI Personalization',
    slug: 'retail-personalization-engine',
    excerpt: 'How a major e-commerce platform increased conversion rates by 45% and customer lifetime value by 32% using AI-powered personalization.',
    client: {
      name: 'ShopSmart E-commerce',
      industry: 'Retail',
      size: 'enterprise'
    },
    challenge: 'Low conversion rates and generic customer experience leading to high cart abandonment.',
    solution: 'Developed AI-powered personalization engine for product recommendations and dynamic pricing.',
    results: [
      {
        metric: 'Conversion Rate',
        value: '+45%',
        description: 'Increase in purchase conversion rate'
      },
      {
        metric: 'Revenue Growth',
        value: '32%',
        description: 'Overall revenue increase'
      },
      {
        metric: 'Customer LTV',
        value: '+28%',
        description: 'Improvement in customer lifetime value'
      }
    ],
    technologies: ['Recommendation Systems', 'Deep Learning', 'Real-time Analytics', 'A/B Testing'],
    timeline: '7 months',
    teamSize: '10 specialists',
    tags: ['Personalization', 'E-commerce', 'Recommendation Systems', 'Retail AI'],
    industry: 'Retail',
    useCase: 'Personalization',
    status: 'published',
    publishedDate: '2024-03-22T14:00:00Z',
    lastUpdated: '2024-05-30T16:20:00Z',
    readTime: 11,
    difficulty: 'intermediate',
    content: `# E-commerce Personalization Case Study Content...`,
    seo: {
      metaTitle: 'Retail AI Case Study: 32% Revenue Boost with Personalization | AIC',
      metaDescription: 'Discover how ShopSmart E-commerce increased conversions by 45% and revenue by 32% with AI-powered personalization.',
      metaKeywords: 'retail AI, e-commerce personalization, recommendation systems, conversion optimization'
    }
  }
]

// Combine all case studies
export const allCaseStudies: CaseStudy[] = [
  ...healthcareCaseStudies,
  ...financialCaseStudies,
  ...manufacturingCaseStudies,
  ...retailCaseStudies
]

// Define case study categories
export const caseStudyCategories: CaseStudyCategory[] = [
  {
    id: 'healthcare',
    name: 'Healthcare',
    description: 'AI solutions transforming patient care and medical operations',
    icon: 'Heart',
    color: 'bg-red-100 text-red-600',
    studies: healthcareCaseStudies
  },
  {
    id: 'financial',
    name: 'Financial Services',
    description: 'Fraud detection, risk management, and financial automation',
    icon: 'DollarSign',
    color: 'bg-green-100 text-green-600',
    studies: financialCaseStudies
  },
  {
    id: 'manufacturing',
    name: 'Manufacturing',
    description: 'Smart manufacturing, predictive maintenance, and Industry 4.0',
    icon: 'Settings',
    color: 'bg-blue-100 text-blue-600',
    studies: manufacturingCaseStudies
  },
  {
    id: 'retail',
    name: 'Retail & E-commerce',
    description: 'Personalization, inventory optimization, and customer analytics',
    icon: 'ShoppingCart',
    color: 'bg-purple-100 text-purple-600',
    studies: retailCaseStudies
  }
]

// Helper functions
export function getCaseStudyBySlug(slug: string): CaseStudy | undefined {
  return allCaseStudies.find(study => study.slug === slug && study.status !== 'draft')
}

export function getCaseStudiesByIndustry(industry: string): CaseStudy[] {
  return allCaseStudies.filter(study => 
    study.industry.toLowerCase() === industry.toLowerCase() && 
    study.status !== 'draft'
  )
}

export function getFeaturedCaseStudies(limit: number = 3): CaseStudy[] {
  return allCaseStudies
    .filter(study => study.status === 'featured')
    .sort((a, b) => new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime())
    .slice(0, limit)
}

export function getPublishedCaseStudies(): CaseStudy[] {
  return allCaseStudies
    .filter(study => study.status !== 'draft')
    .sort((a, b) => new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime())
}

export function searchCaseStudies(query: string): CaseStudy[] {
  const searchTerm = query.toLowerCase()
  return allCaseStudies.filter(study => 
    study.status !== 'draft' && (
      study.title.toLowerCase().includes(searchTerm) ||
      study.excerpt.toLowerCase().includes(searchTerm) ||
      study.industry.toLowerCase().includes(searchTerm) ||
      study.useCase.toLowerCase().includes(searchTerm) ||
      study.tags.some(tag => tag.toLowerCase().includes(searchTerm))
    )
  )
}

export function getCaseStudyStats() {
  const published = getPublishedCaseStudies()
  return {
    total: published.length,
    featured: published.filter(s => s.status === 'featured').length,
    industries: [...new Set(published.map(s => s.industry))].length,
    avgReadTime: Math.round(published.reduce((sum, s) => sum + s.readTime, 0) / published.length)
  }
}
