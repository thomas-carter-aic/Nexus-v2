import puppeteer from 'puppeteer'
import { promises as fs } from 'fs'
import path from 'path'

export interface AssessmentReportData {
  id: string
  companyName: string
  contactName: string
  email: string
  overallScore: number
  categoryScores: Record<string, number>
  responses: any[]
  createdAt: Date
  recommendations: RecommendationSection[]
  benchmarks: BenchmarkData
}

export interface RecommendationSection {
  category: string
  score: number
  level: 'excellent' | 'good' | 'fair' | 'poor'
  recommendations: string[]
  nextSteps: string[]
  priority: 'high' | 'medium' | 'low'
}

export interface BenchmarkData {
  industryAverage: number
  topPerformers: number
  yourPosition: 'top-quartile' | 'above-average' | 'average' | 'below-average'
}

export class PDFGenerator {
  private browser: puppeteer.Browser | null = null

  async initialize(): Promise<void> {
    if (!this.browser) {
      this.browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      })
    }
  }

  async generateAssessmentReport(data: AssessmentReportData): Promise<Buffer> {
    await this.initialize()
    
    const page = await this.browser!.newPage()
    
    try {
      // Generate HTML content
      const htmlContent = await this.generateReportHTML(data)
      
      // Set content and generate PDF
      await page.setContent(htmlContent, { waitUntil: 'networkidle0' })
      
      const pdfBuffer = await page.pdf({
        format: 'A4',
        printBackground: true,
        margin: {
          top: '20mm',
          right: '15mm',
          bottom: '20mm',
          left: '15mm'
        },
        displayHeaderFooter: true,
        headerTemplate: this.getHeaderTemplate(data),
        footerTemplate: this.getFooterTemplate()
      })
      
      return pdfBuffer
      
    } finally {
      await page.close()
    }
  }

  private async generateReportHTML(data: AssessmentReportData): Promise<string> {
    const template = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Readiness Assessment Report - ${data.companyName}</title>
        <style>
            ${await this.getReportStyles()}
        </style>
    </head>
    <body>
        <div class="report-container">
            ${this.generateCoverPage(data)}
            ${this.generateExecutiveSummary(data)}
            ${this.generateScoreBreakdown(data)}
            ${this.generateRecommendations(data)}
            ${this.generateBenchmarks(data)}
            ${this.generateNextSteps(data)}
            ${this.generateAppendix(data)}
        </div>
    </body>
    </html>
    `
    
    return template
  }

  private generateCoverPage(data: AssessmentReportData): string {
    return `
    <div class="cover-page">
        <div class="header-logo">
            <img src="data:image/svg+xml;base64,${this.getLogoBase64()}" alt="AIC Logo" />
        </div>
        <div class="cover-content">
            <h1 class="report-title">AI Readiness Assessment Report</h1>
            <div class="company-info">
                <h2>${data.companyName}</h2>
                <p class="contact-name">${data.contactName}</p>
                <p class="assessment-date">Assessment Date: ${data.createdAt.toLocaleDateString()}</p>
            </div>
            <div class="overall-score-circle">
                <div class="score-circle score-${this.getScoreLevel(data.overallScore)}">
                    <span class="score-number">${data.overallScore}</span>
                    <span class="score-label">Overall Score</span>
                </div>
            </div>
            <div class="score-interpretation">
                <h3>Your AI Readiness Level: ${this.getReadinessLevel(data.overallScore)}</h3>
                <p>${this.getReadinessDescription(data.overallScore)}</p>
            </div>
        </div>
        <div class="cover-footer">
            <p>Confidential Report - Applied Innovations Corporation</p>
        </div>
    </div>
    <div class="page-break"></div>
    `
  }

  private generateExecutiveSummary(data: AssessmentReportData): string {
    const topStrengths = this.getTopStrengths(data.categoryScores)
    const keyOpportunities = this.getKeyOpportunities(data.categoryScores)
    
    return `
    <div class="executive-summary">
        <h2>Executive Summary</h2>
        <div class="summary-content">
            <p class="summary-intro">
                Based on your comprehensive AI readiness assessment, <strong>${data.companyName}</strong> 
                has achieved an overall readiness score of <strong>${data.overallScore}/100</strong>, 
                indicating a <strong>${this.getReadinessLevel(data.overallScore).toLowerCase()}</strong> 
                level of AI readiness.
            </p>
            
            <div class="summary-highlights">
                <div class="strengths">
                    <h3>Key Strengths</h3>
                    <ul>
                        ${topStrengths.map(strength => `<li>${strength}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="opportunities">
                    <h3>Priority Opportunities</h3>
                    <ul>
                        ${keyOpportunities.map(opp => `<li>${opp}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            <div class="summary-recommendation">
                <h3>Primary Recommendation</h3>
                <p>${this.getPrimaryRecommendation(data.overallScore, data.categoryScores)}</p>
            </div>
        </div>
    </div>
    `
  }

  private generateScoreBreakdown(data: AssessmentReportData): string {
    const categories = Object.entries(data.categoryScores)
    
    return `
    <div class="score-breakdown">
        <h2>Detailed Score Breakdown</h2>
        <div class="category-scores">
            ${categories.map(([category, score]) => `
                <div class="category-item">
                    <div class="category-header">
                        <h3>${this.formatCategoryName(category)}</h3>
                        <span class="category-score score-${this.getScoreLevel(score)}">${score}/100</span>
                    </div>
                    <div class="score-bar">
                        <div class="score-fill score-${this.getScoreLevel(score)}" style="width: ${score}%"></div>
                    </div>
                    <p class="category-description">${this.getCategoryDescription(category)}</p>
                </div>
            `).join('')}
        </div>
        
        <div class="score-chart">
            <h3>AI Readiness Radar</h3>
            <div class="radar-chart">
                ${this.generateRadarChart(data.categoryScores)}
            </div>
        </div>
    </div>
    `
  }

  private generateRecommendations(data: AssessmentReportData): string {
    return `
    <div class="recommendations">
        <h2>Detailed Recommendations</h2>
        ${data.recommendations.map(rec => `
            <div class="recommendation-section priority-${rec.priority}">
                <div class="rec-header">
                    <h3>${this.formatCategoryName(rec.category)}</h3>
                    <span class="priority-badge priority-${rec.priority}">${rec.priority.toUpperCase()} PRIORITY</span>
                </div>
                <div class="rec-content">
                    <div class="current-state">
                        <h4>Current State (Score: ${rec.score}/100)</h4>
                        <p>Your organization is at the <strong>${rec.level}</strong> level in this category.</p>
                    </div>
                    <div class="recommendations-list">
                        <h4>Recommendations</h4>
                        <ul>
                            ${rec.recommendations.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="next-steps">
                        <h4>Immediate Next Steps</h4>
                        <ol>
                            ${rec.nextSteps.map(step => `<li>${step}</li>`).join('')}
                        </ol>
                    </div>
                </div>
            </div>
        `).join('')}
    </div>
    `
  }

  private generateBenchmarks(data: AssessmentReportData): string {
    return `
    <div class="benchmarks">
        <h2>Industry Benchmarks</h2>
        <div class="benchmark-content">
            <div class="benchmark-chart">
                <h3>How You Compare</h3>
                <div class="benchmark-bars">
                    <div class="benchmark-item">
                        <span class="benchmark-label">Your Score</span>
                        <div class="benchmark-bar">
                            <div class="benchmark-fill your-score" style="width: ${data.overallScore}%"></div>
                        </div>
                        <span class="benchmark-value">${data.overallScore}</span>
                    </div>
                    <div class="benchmark-item">
                        <span class="benchmark-label">Industry Average</span>
                        <div class="benchmark-bar">
                            <div class="benchmark-fill industry-avg" style="width: ${data.benchmarks.industryAverage}%"></div>
                        </div>
                        <span class="benchmark-value">${data.benchmarks.industryAverage}</span>
                    </div>
                    <div class="benchmark-item">
                        <span class="benchmark-label">Top Performers</span>
                        <div class="benchmark-bar">
                            <div class="benchmark-fill top-performers" style="width: ${data.benchmarks.topPerformers}%"></div>
                        </div>
                        <span class="benchmark-value">${data.benchmarks.topPerformers}</span>
                    </div>
                </div>
            </div>
            <div class="benchmark-analysis">
                <h3>Benchmark Analysis</h3>
                <p>Your organization ranks in the <strong>${data.benchmarks.yourPosition}</strong> category compared to industry peers.</p>
                ${this.getBenchmarkInsights(data.benchmarks)}
            </div>
        </div>
    </div>
    `
  }

  private generateNextSteps(data: AssessmentReportData): string {
    const timeline = this.generateImplementationTimeline(data.recommendations)
    
    return `
    <div class="next-steps">
        <h2>Implementation Roadmap</h2>
        <div class="roadmap-content">
            <div class="timeline">
                <h3>Recommended Timeline</h3>
                ${timeline}
            </div>
            <div class="support-options">
                <h3>How Applied Innovations Can Help</h3>
                <div class="support-grid">
                    <div class="support-item">
                        <h4>AI Strategy Consulting</h4>
                        <p>Develop a comprehensive AI strategy aligned with your business objectives.</p>
                    </div>
                    <div class="support-item">
                        <h4>Technology Implementation</h4>
                        <p>Deploy AI solutions with our expert technical team.</p>
                    </div>
                    <div class="support-item">
                        <h4>Training & Development</h4>
                        <p>Build internal AI capabilities through targeted training programs.</p>
                    </div>
                    <div class="support-item">
                        <h4>Ongoing Support</h4>
                        <p>Continuous optimization and support for your AI initiatives.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
  }

  private generateAppendix(data: AssessmentReportData): string {
    return `
    <div class="appendix">
        <h2>Appendix</h2>
        <div class="appendix-content">
            <div class="methodology">
                <h3>Assessment Methodology</h3>
                <p>This AI readiness assessment evaluates eight key dimensions of organizational AI readiness:</p>
                <ul>
                    <li><strong>Strategy:</strong> AI vision, goals, and strategic alignment</li>
                    <li><strong>Data:</strong> Data quality, governance, and accessibility</li>
                    <li><strong>Technology:</strong> Infrastructure and technical capabilities</li>
                    <li><strong>Talent:</strong> Skills, expertise, and human resources</li>
                    <li><strong>Governance:</strong> Ethics, compliance, and risk management</li>
                    <li><strong>Culture:</strong> Change readiness and data-driven mindset</li>
                    <li><strong>Processes:</strong> Operational readiness and workflow integration</li>
                    <li><strong>Infrastructure:</strong> Technical foundation and scalability</li>
                </ul>
            </div>
            <div class="scoring">
                <h3>Scoring Framework</h3>
                <ul>
                    <li><strong>85-100:</strong> Excellent - Ready for advanced AI implementation</li>
                    <li><strong>70-84:</strong> Good - Ready for targeted AI initiatives</li>
                    <li><strong>50-69:</strong> Fair - Foundation building required</li>
                    <li><strong>0-49:</strong> Poor - Significant preparation needed</li>
                </ul>
            </div>
            <div class="contact">
                <h3>Next Steps</h3>
                <p>Ready to accelerate your AI journey? Contact Applied Innovations Corporation:</p>
                <ul>
                    <li>Email: info@appliedinnovations.com</li>
                    <li>Phone: (555) 123-4567</li>
                    <li>Website: www.appliedinnovations.com</li>
                </ul>
            </div>
        </div>
    </div>
    `
  }

  private async getReportStyles(): Promise<string> {
    return `
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        background: white;
    }
    
    .report-container {
        max-width: 210mm;
        margin: 0 auto;
    }
    
    .page-break {
        page-break-before: always;
    }
    
    /* Cover Page Styles */
    .cover-page {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .header-logo img {
        height: 60px;
        filter: brightness(0) invert(1);
    }
    
    .report-title {
        font-size: 48px;
        font-weight: 300;
        margin-bottom: 40px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .company-info h2 {
        font-size: 36px;
        margin-bottom: 10px;
    }
    
    .contact-name {
        font-size: 20px;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    
    .assessment-date {
        font-size: 16px;
        opacity: 0.8;
    }
    
    .overall-score-circle {
        margin: 40px 0;
    }
    
    .score-circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 8px solid rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .score-number {
        font-size: 48px;
        font-weight: bold;
    }
    
    .score-label {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .score-interpretation h3 {
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    .cover-footer {
        font-size: 14px;
        opacity: 0.8;
    }
    
    /* Content Styles */
    h2 {
        font-size: 28px;
        color: #2c3e50;
        margin-bottom: 20px;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
    
    h3 {
        font-size: 20px;
        color: #34495e;
        margin-bottom: 15px;
    }
    
    h4 {
        font-size: 16px;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    
    /* Score Styles */
    .score-excellent { color: #27ae60; }
    .score-good { color: #f39c12; }
    .score-fair { color: #e67e22; }
    .score-poor { color: #e74c3c; }
    
    .category-item {
        margin-bottom: 30px;
        padding: 20px;
        border: 1px solid #ecf0f1;
        border-radius: 8px;
        background: #fafafa;
    }
    
    .category-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .category-score {
        font-size: 24px;
        font-weight: bold;
        padding: 5px 15px;
        border-radius: 20px;
        background: white;
    }
    
    .score-bar {
        height: 20px;
        background: #ecf0f1;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 10px;
    }
    
    .score-fill {
        height: 100%;
        transition: width 0.3s ease;
    }
    
    .score-fill.score-excellent { background: #27ae60; }
    .score-fill.score-good { background: #f39c12; }
    .score-fill.score-fair { background: #e67e22; }
    .score-fill.score-poor { background: #e74c3c; }
    
    /* Recommendation Styles */
    .recommendation-section {
        margin-bottom: 30px;
        padding: 25px;
        border-radius: 8px;
        border-left: 5px solid;
    }
    
    .priority-high {
        border-left-color: #e74c3c;
        background: #fdf2f2;
    }
    
    .priority-medium {
        border-left-color: #f39c12;
        background: #fef9e7;
    }
    
    .priority-low {
        border-left-color: #27ae60;
        background: #eafaf1;
    }
    
    .rec-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .priority-badge {
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    
    .priority-badge.priority-high { background: #e74c3c; }
    .priority-badge.priority-medium { background: #f39c12; }
    .priority-badge.priority-low { background: #27ae60; }
    
    /* Benchmark Styles */
    .benchmark-bars {
        margin: 20px 0;
    }
    
    .benchmark-item {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .benchmark-label {
        width: 150px;
        font-weight: 500;
    }
    
    .benchmark-bar {
        flex: 1;
        height: 25px;
        background: #ecf0f1;
        border-radius: 12px;
        overflow: hidden;
        margin: 0 15px;
    }
    
    .benchmark-fill {
        height: 100%;
    }
    
    .benchmark-fill.your-score { background: #3498db; }
    .benchmark-fill.industry-avg { background: #95a5a6; }
    .benchmark-fill.top-performers { background: #27ae60; }
    
    .benchmark-value {
        width: 40px;
        text-align: right;
        font-weight: bold;
    }
    
    /* Support Grid */
    .support-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
    }
    
    .support-item {
        padding: 20px;
        border: 1px solid #ecf0f1;
        border-radius: 8px;
        background: white;
    }
    
    .support-item h4 {
        color: #3498db;
        margin-bottom: 10px;
    }
    
    /* Lists */
    ul, ol {
        margin-left: 20px;
        margin-bottom: 15px;
    }
    
    li {
        margin-bottom: 8px;
    }
    
    /* Spacing */
    .executive-summary,
    .score-breakdown,
    .recommendations,
    .benchmarks,
    .next-steps,
    .appendix {
        padding: 30px;
        margin-bottom: 20px;
    }
    
    @media print {
        .page-break {
            page-break-before: always;
        }
    }
    `
  }

  private getHeaderTemplate(data: AssessmentReportData): string {
    return `
    <div style="font-size: 10px; padding: 5px 15px; width: 100%; display: flex; justify-content: space-between; align-items: center;">
        <span>AI Readiness Assessment - ${data.companyName}</span>
        <span>Applied Innovations Corporation</span>
    </div>
    `
  }

  private getFooterTemplate(): string {
    return `
    <div style="font-size: 10px; padding: 5px 15px; width: 100%; display: flex; justify-content: space-between; align-items: center;">
        <span>Confidential Report</span>
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>
    `
  }

  // Helper methods for content generation
  private getScoreLevel(score: number): string {
    if (score >= 85) return 'excellent'
    if (score >= 70) return 'good'
    if (score >= 50) return 'fair'
    return 'poor'
  }

  private getReadinessLevel(score: number): string {
    if (score >= 85) return 'AI-Ready Leader'
    if (score >= 70) return 'AI-Ready'
    if (score >= 50) return 'AI-Aware'
    return 'AI-Beginner'
  }

  private getReadinessDescription(score: number): string {
    if (score >= 85) return 'Your organization demonstrates exceptional AI readiness and is positioned to lead in AI adoption.'
    if (score >= 70) return 'Your organization shows strong AI readiness with solid foundations for successful AI implementation.'
    if (score >= 50) return 'Your organization has basic AI awareness but requires focused preparation for successful AI adoption.'
    return 'Your organization is in the early stages of AI readiness and would benefit from comprehensive preparation.'
  }

  private formatCategoryName(category: string): string {
    return category.charAt(0).toUpperCase() + category.slice(1).replace(/([A-Z])/g, ' $1')
  }

  private getCategoryDescription(category: string): string {
    const descriptions = {
      strategy: 'AI vision, strategic alignment, and business case development',
      data: 'Data quality, governance, accessibility, and management practices',
      technology: 'Technical infrastructure, tools, and platform readiness',
      talent: 'Skills, expertise, training, and human resource capabilities',
      governance: 'Ethics, compliance, risk management, and oversight frameworks',
      culture: 'Change readiness, data-driven mindset, and organizational adaptability',
      processes: 'Workflow integration, operational readiness, and process optimization',
      infrastructure: 'Technical foundation, scalability, and system architecture'
    }
    return descriptions[category as keyof typeof descriptions] || ''
  }

  private getTopStrengths(categoryScores: Record<string, number>): string[] {
    return Object.entries(categoryScores)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([category, score]) => `Strong ${this.formatCategoryName(category)} foundation (${score}/100)`)
  }

  private getKeyOpportunities(categoryScores: Record<string, number>): string[] {
    return Object.entries(categoryScores)
      .sort(([,a], [,b]) => a - b)
      .slice(0, 3)
      .map(([category, score]) => `Enhance ${this.formatCategoryName(category)} capabilities (${score}/100)`)
  }

  private getPrimaryRecommendation(overallScore: number, categoryScores: Record<string, number>): string {
    const lowestCategory = Object.entries(categoryScores).sort(([,a], [,b]) => a - b)[0]
    
    if (overallScore >= 85) {
      return `Focus on advanced AI implementation and maintaining your competitive edge in ${this.formatCategoryName(lowestCategory[0])}.`
    } else if (overallScore >= 70) {
      return `Prioritize strengthening your ${this.formatCategoryName(lowestCategory[0])} capabilities while beginning targeted AI pilot projects.`
    } else if (overallScore >= 50) {
      return `Build foundational capabilities, particularly in ${this.formatCategoryName(lowestCategory[0])}, before pursuing AI implementation.`
    } else {
      return `Establish fundamental AI readiness across all dimensions, starting with ${this.formatCategoryName(lowestCategory[0])} as the highest priority.`
    }
  }

  private generateRadarChart(categoryScores: Record<string, number>): string {
    // This would generate an SVG radar chart
    // For brevity, returning a placeholder
    return '<div class="radar-placeholder">Radar chart visualization would be generated here</div>'
  }

  private getBenchmarkInsights(benchmarks: BenchmarkData): string {
    const insights = {
      'top-quartile': 'You are performing exceptionally well compared to industry peers and are positioned as an AI leader.',
      'above-average': 'You are performing better than most organizations in your industry with strong AI readiness.',
      'average': 'You are performing at industry average levels with room for improvement in key areas.',
      'below-average': 'You have significant opportunities to improve your AI readiness compared to industry peers.'
    }
    
    return `<p>${insights[benchmarks.yourPosition]}</p>`
  }

  private generateImplementationTimeline(recommendations: RecommendationSection[]): string {
    const highPriority = recommendations.filter(r => r.priority === 'high')
    const mediumPriority = recommendations.filter(r => r.priority === 'medium')
    const lowPriority = recommendations.filter(r => r.priority === 'low')
    
    return `
    <div class="timeline-phases">
        <div class="phase">
            <h4>Phase 1: Immediate (0-3 months)</h4>
            <ul>
                ${highPriority.map(r => `<li>${this.formatCategoryName(r.category)}: ${r.nextSteps[0]}</li>`).join('')}
            </ul>
        </div>
        <div class="phase">
            <h4>Phase 2: Short-term (3-6 months)</h4>
            <ul>
                ${mediumPriority.map(r => `<li>${this.formatCategoryName(r.category)}: ${r.nextSteps[0]}</li>`).join('')}
            </ul>
        </div>
        <div class="phase">
            <h4>Phase 3: Medium-term (6-12 months)</h4>
            <ul>
                ${lowPriority.map(r => `<li>${this.formatCategoryName(r.category)}: ${r.nextSteps[0]}</li>`).join('')}
            </ul>
        </div>
    </div>
    `
  }

  private getLogoBase64(): string {
    // Return base64 encoded logo
    // This would be your actual logo encoded as base64
    return 'PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjUwIj48dGV4dCB4PSI1MCIgeT0iMjUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkFJQzwvdGV4dD48L3N2Zz4='
  }

  async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close()
      this.browser = null
    }
  }
}

export const pdfGenerator = new PDFGenerator()
