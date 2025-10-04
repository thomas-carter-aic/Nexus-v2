import { AssessmentQuestion } from '@/lib/validations/assessment'

export const assessmentQuestions: AssessmentQuestion[] = [
  // Strategy Category
  {
    id: 'strategy-1',
    category: 'strategy',
    question: 'How would you describe your organization\'s current AI strategy?',
    type: 'multiple-choice',
    options: [
      { value: 'no-strategy', label: 'No formal AI strategy exists', score: 0 },
      { value: 'exploring', label: 'We are exploring AI opportunities', score: 25 },
      { value: 'developing', label: 'We are developing an AI strategy', score: 50 },
      { value: 'defined', label: 'We have a defined AI strategy', score: 75 },
      { value: 'executing', label: 'We are actively executing our AI strategy', score: 100 }
    ],
    weight: 2,
    description: 'Understanding your strategic approach to AI adoption'
  },
  {
    id: 'strategy-2',
    category: 'strategy',
    question: 'What is the primary driver for AI adoption in your organization?',
    type: 'multiple-choice',
    options: [
      { value: 'cost-reduction', label: 'Cost reduction and efficiency', score: 60 },
      { value: 'competitive-advantage', label: 'Competitive advantage', score: 80 },
      { value: 'innovation', label: 'Innovation and new products/services', score: 90 },
      { value: 'customer-experience', label: 'Enhanced customer experience', score: 85 },
      { value: 'compliance', label: 'Regulatory compliance', score: 40 },
      { value: 'unsure', label: 'Not sure/No clear driver', score: 10 }
    ],
    weight: 1.5
  },
  {
    id: 'strategy-3',
    category: 'strategy',
    question: 'How well-defined are your AI use cases and ROI expectations?',
    type: 'scale',
    options: [
      { value: '1', label: 'Not defined at all', score: 0 },
      { value: '2', label: 'Somewhat defined', score: 25 },
      { value: '3', label: 'Moderately defined', score: 50 },
      { value: '4', label: 'Well defined', score: 75 },
      { value: '5', label: 'Very well defined with clear metrics', score: 100 }
    ],
    weight: 1.5
  },

  // Data Category
  {
    id: 'data-1',
    category: 'data',
    question: 'How would you rate the quality and accessibility of your data?',
    type: 'scale',
    options: [
      { value: '1', label: 'Poor quality, difficult to access', score: 0 },
      { value: '2', label: 'Below average', score: 25 },
      { value: '3', label: 'Average quality and accessibility', score: 50 },
      { value: '4', label: 'Good quality and accessibility', score: 75 },
      { value: '5', label: 'Excellent quality, easily accessible', score: 100 }
    ],
    weight: 2,
    description: 'Data quality is fundamental to AI success'
  },
  {
    id: 'data-2',
    category: 'data',
    question: 'What percentage of your data is structured and ready for analysis?',
    type: 'multiple-choice',
    options: [
      { value: '0-20', label: '0-20%', score: 20 },
      { value: '21-40', label: '21-40%', score: 40 },
      { value: '41-60', label: '41-60%', score: 60 },
      { value: '61-80', label: '61-80%', score: 80 },
      { value: '81-100', label: '81-100%', score: 100 }
    ],
    weight: 1.5
  },
  {
    id: 'data-3',
    category: 'data',
    question: 'Do you have established data governance and privacy policies?',
    type: 'boolean',
    options: [
      { value: 'true', label: 'Yes, comprehensive policies in place', score: 100 },
      { value: 'false', label: 'No, limited or no policies', score: 0 }
    ],
    weight: 1.5
  },

  // Technology Category
  {
    id: 'technology-1',
    category: 'technology',
    question: 'How would you describe your current technology infrastructure?',
    type: 'multiple-choice',
    options: [
      { value: 'legacy', label: 'Primarily legacy systems', score: 20 },
      { value: 'mixed', label: 'Mix of legacy and modern systems', score: 50 },
      { value: 'modern', label: 'Mostly modern, cloud-ready systems', score: 80 },
      { value: 'cutting-edge', label: 'Cutting-edge, AI-ready infrastructure', score: 100 }
    ],
    weight: 2
  },
  {
    id: 'technology-2',
    category: 'technology',
    question: 'What is your organization\'s cloud adoption level?',
    type: 'multiple-choice',
    options: [
      { value: 'none', label: 'No cloud adoption', score: 10 },
      { value: 'basic', label: 'Basic cloud services (email, storage)', score: 30 },
      { value: 'moderate', label: 'Moderate cloud adoption', score: 60 },
      { value: 'advanced', label: 'Advanced cloud-native applications', score: 90 },
      { value: 'full', label: 'Fully cloud-native organization', score: 100 }
    ],
    weight: 1.5
  },
  {
    id: 'technology-3',
    category: 'technology',
    question: 'Do you have experience with machine learning or AI tools?',
    type: 'multiple-choice',
    options: [
      { value: 'none', label: 'No experience', score: 0 },
      { value: 'basic', label: 'Basic analytics tools', score: 30 },
      { value: 'intermediate', label: 'Some ML/AI experimentation', score: 60 },
      { value: 'advanced', label: 'Production ML/AI systems', score: 90 },
      { value: 'expert', label: 'Advanced AI/ML capabilities', score: 100 }
    ],
    weight: 2
  },

  // Talent Category
  {
    id: 'talent-1',
    category: 'talent',
    question: 'How would you rate your team\'s AI and data science skills?',
    type: 'scale',
    options: [
      { value: '1', label: 'Very limited skills', score: 0 },
      { value: '2', label: 'Basic skills', score: 25 },
      { value: '3', label: 'Moderate skills', score: 50 },
      { value: '4', label: 'Strong skills', score: 75 },
      { value: '5', label: 'Expert-level skills', score: 100 }
    ],
    weight: 2
  },
  {
    id: 'talent-2',
    category: 'talent',
    question: 'What is your approach to building AI capabilities?',
    type: 'multiple-choice',
    options: [
      { value: 'hire', label: 'Hire new AI talent', score: 70 },
      { value: 'train', label: 'Train existing employees', score: 80 },
      { value: 'partner', label: 'Partner with external experts', score: 60 },
      { value: 'mixed', label: 'Combination of approaches', score: 90 },
      { value: 'none', label: 'No clear approach', score: 10 }
    ],
    weight: 1.5
  },

  // Governance Category
  {
    id: 'governance-1',
    category: 'governance',
    question: 'Do you have AI ethics and governance frameworks in place?',
    type: 'multiple-choice',
    options: [
      { value: 'none', label: 'No frameworks in place', score: 0 },
      { value: 'developing', label: 'Currently developing frameworks', score: 40 },
      { value: 'basic', label: 'Basic frameworks established', score: 70 },
      { value: 'comprehensive', label: 'Comprehensive governance in place', score: 100 }
    ],
    weight: 1.5
  },
  {
    id: 'governance-2',
    category: 'governance',
    question: 'How do you handle AI risk management and compliance?',
    type: 'scale',
    options: [
      { value: '1', label: 'No formal risk management', score: 0 },
      { value: '2', label: 'Basic risk awareness', score: 25 },
      { value: '3', label: 'Moderate risk management', score: 50 },
      { value: '4', label: 'Strong risk management', score: 75 },
      { value: '5', label: 'Comprehensive risk framework', score: 100 }
    ],
    weight: 1.5
  },

  // Culture Category
  {
    id: 'culture-1',
    category: 'culture',
    question: 'How receptive is your organization to AI-driven change?',
    type: 'scale',
    options: [
      { value: '1', label: 'Very resistant to change', score: 0 },
      { value: '2', label: 'Somewhat resistant', score: 25 },
      { value: '3', label: 'Neutral/Mixed reactions', score: 50 },
      { value: '4', label: 'Generally receptive', score: 75 },
      { value: '5', label: 'Very enthusiastic about AI', score: 100 }
    ],
    weight: 1.5
  },
  {
    id: 'culture-2',
    category: 'culture',
    question: 'How data-driven is your decision-making process?',
    type: 'multiple-choice',
    options: [
      { value: 'intuition', label: 'Primarily intuition-based', score: 20 },
      { value: 'mixed', label: 'Mix of data and intuition', score: 50 },
      { value: 'data-informed', label: 'Data-informed decisions', score: 80 },
      { value: 'data-driven', label: 'Fully data-driven culture', score: 100 }
    ],
    weight: 1.5
  }
]

// Category weights for overall score calculation
export const categoryWeights = {
  strategy: 0.20,
  data: 0.20,
  technology: 0.15,
  talent: 0.15,
  governance: 0.10,
  culture: 0.10,
  processes: 0.05,
  infrastructure: 0.05
}

// Scoring thresholds for recommendations
export const scoringThresholds = {
  excellent: 85,
  good: 70,
  fair: 50,
  poor: 30
}

export function calculateCategoryScore(responses: any[], category: string): number {
  const categoryQuestions = assessmentQuestions.filter(q => q.category === category)
  let totalScore = 0
  let totalWeight = 0

  categoryQuestions.forEach(question => {
    const response = responses.find(r => r.questionId === question.id)
    if (response && response.score !== undefined) {
      totalScore += response.score * question.weight
      totalWeight += question.weight
    }
  })

  return totalWeight > 0 ? Math.round(totalScore / totalWeight) : 0
}

export function calculateOverallScore(categoryScores: Record<string, number>): number {
  let weightedScore = 0
  let totalWeight = 0

  Object.entries(categoryScores).forEach(([category, score]) => {
    const weight = categoryWeights[category as keyof typeof categoryWeights] || 0
    weightedScore += score * weight
    totalWeight += weight
  })

  return totalWeight > 0 ? Math.round(weightedScore / totalWeight) : 0
}
