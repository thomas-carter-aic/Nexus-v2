import nodemailer from 'nodemailer'
import { promises as fs } from 'fs'
import path from 'path'

export interface EmailAttachment {
  filename: string
  content: Buffer
  contentType: string
}

export interface AssessmentEmailData {
  recipientEmail: string
  recipientName: string
  companyName: string
  overallScore: number
  reportPath: string
  assessmentId: string
}

export class EmailService {
  private transporter: nodemailer.Transporter

  constructor() {
    this.transporter = nodemailer.createTransporter({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    })
  }

  async sendAssessmentReport(data: AssessmentEmailData, pdfBuffer: Buffer): Promise<void> {
    const emailTemplate = await this.generateAssessmentEmailTemplate(data)
    
    const mailOptions = {
      from: {
        name: process.env.EMAIL_FROM_NAME || 'Applied Innovations Corporation',
        address: process.env.EMAIL_FROM || 'noreply@appliedinnovations.com'
      },
      to: data.recipientEmail,
      subject: `Your AI Readiness Assessment Report - ${data.companyName}`,
      html: emailTemplate,
      attachments: [
        {
          filename: `AI-Readiness-Report-${data.companyName.replace(/[^a-zA-Z0-9]/g, '-')}.pdf`,
          content: pdfBuffer,
          contentType: 'application/pdf'
        }
      ]
    }

    await this.transporter.sendMail(mailOptions)
  }

  async sendAssessmentConfirmation(email: string, name: string, companyName: string): Promise<void> {
    const template = await this.generateConfirmationEmailTemplate(name, companyName)
    
    const mailOptions = {
      from: {
        name: process.env.EMAIL_FROM_NAME || 'Applied Innovations Corporation',
        address: process.env.EMAIL_FROM || 'noreply@appliedinnovations.com'
      },
      to: email,
      subject: 'AI Readiness Assessment Received - Report Processing',
      html: template
    }

    await this.transporter.sendMail(mailOptions)
  }

  async sendFollowUpEmail(email: string, name: string, companyName: string, followUpType: string): Promise<void> {
    const template = await this.generateFollowUpEmailTemplate(name, companyName, followUpType)
    
    const mailOptions = {
      from: {
        name: process.env.EMAIL_FROM_NAME || 'Applied Innovations Corporation',
        address: process.env.EMAIL_FROM || 'noreply@appliedinnovations.com'
      },
      to: email,
      subject: this.getFollowUpSubject(followUpType, companyName),
      html: template
    }

    await this.transporter.sendMail(mailOptions)
  }

  private async generateAssessmentEmailTemplate(data: AssessmentEmailData): Promise<string> {
    const readinessLevel = this.getReadinessLevel(data.overallScore)
    const readinessColor = this.getReadinessColor(data.overallScore)
    
    return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your AI Readiness Assessment Report</title>
        <style>
            ${this.getEmailStyles()}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo">
                    <img src="https://appliedinnovations.com/logo.png" alt="Applied Innovations Corporation" />
                </div>
                <h1>Your AI Readiness Assessment Report</h1>
            </div>
            
            <div class="content">
                <div class="greeting">
                    <h2>Hello ${data.recipientName},</h2>
                    <p>Thank you for completing the AI Readiness Assessment for <strong>${data.companyName}</strong>.</p>
                </div>
                
                <div class="score-summary">
                    <div class="score-card">
                        <div class="score-circle" style="border-color: ${readinessColor};">
                            <span class="score-number" style="color: ${readinessColor};">${data.overallScore}</span>
                            <span class="score-label">Overall Score</span>
                        </div>
                        <div class="score-details">
                            <h3 style="color: ${readinessColor};">${readinessLevel}</h3>
                            <p>${this.getReadinessDescription(data.overallScore)}</p>
                        </div>
                    </div>
                </div>
                
                <div class="report-info">
                    <h3>📊 Your Comprehensive Report Includes:</h3>
                    <ul>
                        <li><strong>Detailed Score Breakdown</strong> - Analysis across 8 key AI readiness dimensions</li>
                        <li><strong>Personalized Recommendations</strong> - Specific actions tailored to your organization</li>
                        <li><strong>Industry Benchmarks</strong> - See how you compare to industry peers</li>
                        <li><strong>Implementation Roadmap</strong> - Step-by-step guide for your AI journey</li>
                        <li><strong>Expert Insights</strong> - Professional analysis and strategic guidance</li>
                    </ul>
                </div>
                
                <div class="cta-section">
                    <h3>🚀 Ready to Accelerate Your AI Journey?</h3>
                    <p>Our AI experts are ready to help you implement the recommendations in your report.</p>
                    <div class="cta-buttons">
                        <a href="https://appliedinnovations.com/consultation?ref=assessment&id=${data.assessmentId}" class="btn-primary">
                            Schedule Free Consultation
                        </a>
                        <a href="https://appliedinnovations.com/services/ai-strategy" class="btn-secondary">
                            Explore Our Services
                        </a>
                    </div>
                </div>
                
                <div class="next-steps">
                    <h3>What's Next?</h3>
                    <div class="steps-grid">
                        <div class="step">
                            <div class="step-number">1</div>
                            <div class="step-content">
                                <h4>Review Your Report</h4>
                                <p>Download and review your comprehensive AI readiness assessment report (attached).</p>
                            </div>
                        </div>
                        <div class="step">
                            <div class="step-number">2</div>
                            <div class="step-content">
                                <h4>Identify Priorities</h4>
                                <p>Focus on the high-priority recommendations that will have the biggest impact.</p>
                            </div>
                        </div>
                        <div class="step">
                            <div class="step-number">3</div>
                            <div class="step-content">
                                <h4>Take Action</h4>
                                <p>Start implementing the recommended next steps or contact us for expert guidance.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="support-section">
                    <h3>Need Help Getting Started?</h3>
                    <p>Our team of AI experts is here to support your journey:</p>
                    <div class="contact-info">
                        <div class="contact-item">
                            <strong>📧 Email:</strong> <a href="mailto:ai-experts@appliedinnovations.com">ai-experts@appliedinnovations.com</a>
                        </div>
                        <div class="contact-item">
                            <strong>📞 Phone:</strong> <a href="tel:+15551234567">(555) 123-4567</a>
                        </div>
                        <div class="contact-item">
                            <strong>🌐 Website:</strong> <a href="https://appliedinnovations.com">appliedinnovations.com</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div class="footer-content">
                    <p><strong>Applied Innovations Corporation</strong></p>
                    <p>Transforming businesses through intelligent AI solutions</p>
                    <div class="social-links">
                        <a href="https://linkedin.com/company/applied-innovations">LinkedIn</a> |
                        <a href="https://twitter.com/appliedinnovations">Twitter</a> |
                        <a href="https://appliedinnovations.com/blog">Blog</a>
                    </div>
                    <p class="disclaimer">
                        This assessment report is confidential and intended solely for ${data.companyName}. 
                        Please do not share without permission.
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    `
  }

  private async generateConfirmationEmailTemplate(name: string, companyName: string): Promise<string> {
    return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Assessment Received - Processing Your Report</title>
        <style>
            ${this.getEmailStyles()}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo">
                    <img src="https://appliedinnovations.com/logo.png" alt="Applied Innovations Corporation" />
                </div>
                <h1>Assessment Received!</h1>
            </div>
            
            <div class="content">
                <div class="greeting">
                    <h2>Hello ${name},</h2>
                    <p>Thank you for completing the AI Readiness Assessment for <strong>${companyName}</strong>.</p>
                </div>
                
                <div class="processing-info">
                    <div class="processing-card">
                        <div class="processing-icon">⚙️</div>
                        <h3>Your Report is Being Generated</h3>
                        <p>Our AI analysis engine is processing your responses and generating your personalized AI readiness report.</p>
                        <div class="processing-steps">
                            <div class="processing-step completed">
                                <span class="step-icon">✅</span>
                                <span>Assessment responses received</span>
                            </div>
                            <div class="processing-step active">
                                <span class="step-icon">⚙️</span>
                                <span>Analyzing your AI readiness</span>
                            </div>
                            <div class="processing-step">
                                <span class="step-icon">📊</span>
                                <span>Generating personalized report</span>
                            </div>
                            <div class="processing-step">
                                <span class="step-icon">📧</span>
                                <span>Delivering your report</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="timeline">
                    <h3>What to Expect</h3>
                    <p><strong>📧 Your comprehensive AI readiness report will be delivered to your inbox within the next 5-10 minutes.</strong></p>
                    <p>The report will include:</p>
                    <ul>
                        <li>Your overall AI readiness score and detailed breakdown</li>
                        <li>Personalized recommendations for your organization</li>
                        <li>Industry benchmarks and competitive analysis</li>
                        <li>Implementation roadmap with prioritized next steps</li>
                    </ul>
                </div>
                
                <div class="meanwhile">
                    <h3>In the Meantime...</h3>
                    <p>Explore how Applied Innovations can help accelerate your AI journey:</p>
                    <div class="resource-links">
                        <a href="https://appliedinnovations.com/case-studies" class="resource-link">
                            <strong>📈 Success Stories</strong>
                            <span>See how we've helped organizations like yours</span>
                        </a>
                        <a href="https://appliedinnovations.com/blog/ai-readiness" class="resource-link">
                            <strong>📚 AI Readiness Guide</strong>
                            <span>Learn more about AI implementation best practices</span>
                        </a>
                        <a href="https://appliedinnovations.com/services" class="resource-link">
                            <strong>🛠️ Our Services</strong>
                            <span>Discover our AI consulting and implementation services</span>
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div class="footer-content">
                    <p><strong>Applied Innovations Corporation</strong></p>
                    <p>Questions? Contact us at <a href="mailto:support@appliedinnovations.com">support@appliedinnovations.com</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    `
  }

  private async generateFollowUpEmailTemplate(name: string, companyName: string, followUpType: string): Promise<string> {
    const templates = {
      'consultation-offer': this.getConsultationOfferTemplate(name, companyName),
      'implementation-guide': this.getImplementationGuideTemplate(name, companyName),
      'success-stories': this.getSuccessStoriesTemplate(name, companyName),
      'survey-feedback': this.getSurveyFeedbackTemplate(name, companyName)
    }
    
    return templates[followUpType as keyof typeof templates] || templates['consultation-offer']
  }

  private getConsultationOfferTemplate(name: string, companyName: string): string {
    return `
    <div class="email-container">
        <div class="header">
            <h1>Ready to Take the Next Step?</h1>
        </div>
        <div class="content">
            <h2>Hello ${name},</h2>
            <p>I hope you found your AI Readiness Assessment report valuable for ${companyName}.</p>
            <p>Based on your assessment results, I'd like to offer you a complimentary 30-minute consultation to discuss:</p>
            <ul>
                <li>Your specific AI implementation priorities</li>
                <li>How to address your key readiness gaps</li>
                <li>Potential quick wins for your organization</li>
                <li>Our approach to AI strategy and implementation</li>
            </ul>
            <div class="cta-section">
                <a href="https://appliedinnovations.com/consultation" class="btn-primary">Schedule Your Free Consultation</a>
            </div>
        </div>
    </div>
    `
  }

  private getImplementationGuideTemplate(name: string, companyName: string): string {
    return `
    <div class="email-container">
        <div class="header">
            <h1>Your AI Implementation Roadmap</h1>
        </div>
        <div class="content">
            <h2>Hello ${name},</h2>
            <p>Following up on your AI Readiness Assessment for ${companyName}, I wanted to share some additional resources to help you move forward with your AI initiatives.</p>
            <p>I've prepared a detailed implementation guide that complements your assessment report...</p>
        </div>
    </div>
    `
  }

  private getSuccessStoriesTemplate(name: string, companyName: string): string {
    return `
    <div class="email-container">
        <div class="header">
            <h1>AI Success Stories from Companies Like Yours</h1>
        </div>
        <div class="content">
            <h2>Hello ${name},</h2>
            <p>I thought you might be interested in seeing how other organizations similar to ${companyName} have successfully implemented AI solutions...</p>
        </div>
    </div>
    `
  }

  private getSurveyFeedbackTemplate(name: string, companyName: string): string {
    return `
    <div class="email-container">
        <div class="header">
            <h1>How Was Your Assessment Experience?</h1>
        </div>
        <div class="content">
            <h2>Hello ${name},</h2>
            <p>Thank you for completing the AI Readiness Assessment for ${companyName}. Your feedback helps us improve our assessment process...</p>
        </div>
    </div>
    `
  }

  private getEmailStyles(): string {
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
        background-color: #f5f5f5;
    }
    
    .email-container {
        max-width: 600px;
        margin: 0 auto;
        background: white;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 30px;
        text-align: center;
    }
    
    .header h1 {
        font-size: 28px;
        font-weight: 300;
        margin-top: 20px;
    }
    
    .logo img {
        height: 50px;
        filter: brightness(0) invert(1);
    }
    
    .content {
        padding: 40px 30px;
    }
    
    .greeting h2 {
        color: #2c3e50;
        margin-bottom: 15px;
    }
    
    .score-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin: 30px 0;
        border: 1px solid #e9ecef;
    }
    
    .score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 6px solid;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        background: white;
    }
    
    .score-number {
        font-size: 36px;
        font-weight: bold;
    }
    
    .score-label {
        font-size: 12px;
        opacity: 0.8;
    }
    
    .score-details h3 {
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    .report-info {
        background: #e8f4fd;
        border-left: 4px solid #3498db;
        padding: 25px;
        margin: 30px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .report-info h3 {
        color: #2980b9;
        margin-bottom: 15px;
    }
    
    .report-info ul {
        list-style: none;
        padding-left: 0;
    }
    
    .report-info li {
        padding: 8px 0;
        border-bottom: 1px solid rgba(52, 152, 219, 0.1);
    }
    
    .report-info li:last-child {
        border-bottom: none;
    }
    
    .cta-section {
        text-align: center;
        margin: 40px 0;
        padding: 30px;
        background: #f8f9fa;
        border-radius: 12px;
    }
    
    .cta-section h3 {
        color: #2c3e50;
        margin-bottom: 15px;
    }
    
    .cta-buttons {
        margin-top: 25px;
    }
    
    .btn-primary, .btn-secondary {
        display: inline-block;
        padding: 15px 30px;
        margin: 10px;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .btn-primary {
        background: #3498db;
        color: white;
    }
    
    .btn-primary:hover {
        background: #2980b9;
    }
    
    .btn-secondary {
        background: white;
        color: #3498db;
        border: 2px solid #3498db;
    }
    
    .btn-secondary:hover {
        background: #3498db;
        color: white;
    }
    
    .steps-grid {
        display: grid;
        gap: 20px;
        margin-top: 20px;
    }
    
    .step {
        display: flex;
        align-items: flex-start;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
    
    .step-number {
        background: #3498db;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 15px;
        flex-shrink: 0;
    }
    
    .step-content h4 {
        color: #2c3e50;
        margin-bottom: 8px;
    }
    
    .contact-info {
        margin-top: 20px;
    }
    
    .contact-item {
        padding: 10px 0;
        border-bottom: 1px solid #eee;
    }
    
    .contact-item:last-child {
        border-bottom: none;
    }
    
    .contact-item a {
        color: #3498db;
        text-decoration: none;
    }
    
    .contact-item a:hover {
        text-decoration: underline;
    }
    
    .processing-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin: 30px 0;
    }
    
    .processing-icon {
        font-size: 48px;
        margin-bottom: 20px;
    }
    
    .processing-steps {
        margin-top: 30px;
        text-align: left;
    }
    
    .processing-step {
        display: flex;
        align-items: center;
        padding: 10px 0;
        opacity: 0.5;
    }
    
    .processing-step.completed,
    .processing-step.active {
        opacity: 1;
    }
    
    .processing-step.active {
        font-weight: 600;
        color: #3498db;
    }
    
    .step-icon {
        margin-right: 15px;
        width: 20px;
    }
    
    .resource-links {
        margin-top: 20px;
    }
    
    .resource-link {
        display: block;
        padding: 20px;
        margin-bottom: 15px;
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s ease;
    }
    
    .resource-link:hover {
        border-color: #3498db;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.1);
    }
    
    .resource-link strong {
        color: #3498db;
        display: block;
        margin-bottom: 5px;
    }
    
    .resource-link span {
        color: #666;
        font-size: 14px;
    }
    
    .footer {
        background: #2c3e50;
        color: white;
        padding: 30px;
        text-align: center;
    }
    
    .footer-content p {
        margin-bottom: 10px;
    }
    
    .social-links {
        margin: 20px 0;
    }
    
    .social-links a {
        color: #ecf0f1;
        text-decoration: none;
        margin: 0 10px;
    }
    
    .social-links a:hover {
        color: #3498db;
    }
    
    .disclaimer {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #34495e;
    }
    
    @media (max-width: 600px) {
        .email-container {
            margin: 0;
        }
        
        .content {
            padding: 20px;
        }
        
        .header {
            padding: 30px 20px;
        }
        
        .cta-buttons {
            flex-direction: column;
        }
        
        .btn-primary, .btn-secondary {
            display: block;
            margin: 10px 0;
        }
    }
    `
  }

  private getReadinessLevel(score: number): string {
    if (score >= 85) return 'AI-Ready Leader'
    if (score >= 70) return 'AI-Ready'
    if (score >= 50) return 'AI-Aware'
    return 'AI-Beginner'
  }

  private getReadinessColor(score: number): string {
    if (score >= 85) return '#27ae60'
    if (score >= 70) return '#f39c12'
    if (score >= 50) return '#e67e22'
    return '#e74c3c'
  }

  private getReadinessDescription(score: number): string {
    if (score >= 85) return 'Your organization demonstrates exceptional AI readiness and is positioned to lead in AI adoption.'
    if (score >= 70) return 'Your organization shows strong AI readiness with solid foundations for successful AI implementation.'
    if (score >= 50) return 'Your organization has basic AI awareness but requires focused preparation for successful AI adoption.'
    return 'Your organization is in the early stages of AI readiness and would benefit from comprehensive preparation.'
  }

  private getFollowUpSubject(followUpType: string, companyName: string): string {
    const subjects = {
      'consultation-offer': `Free AI Consultation Available - ${companyName}`,
      'implementation-guide': `Your AI Implementation Roadmap - ${companyName}`,
      'success-stories': `AI Success Stories for Companies Like ${companyName}`,
      'survey-feedback': `Quick Feedback on Your Assessment Experience`
    }
    
    return subjects[followUpType as keyof typeof subjects] || `Follow-up: AI Readiness Assessment - ${companyName}`
  }

  async verifyConnection(): Promise<boolean> {
    try {
      await this.transporter.verify()
      return true
    } catch (error) {
      console.error('Email service connection failed:', error)
      return false
    }
  }
}

export const emailService = new EmailService()
