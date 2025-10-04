import nodemailer from 'nodemailer'
import { prisma } from '../db'
import { suiteCRM } from './suitecrm'
import { ServerContactInput, ContactActivityInput, calculateLeadScore, getPriorityFromScore } from '../validations/contact'

export interface ContactNotification {
  type: 'email' | 'slack' | 'discord'
  recipient: string
  subject?: string
  message: string
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
}

export class ContactService {
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

  async submitContact(data: ServerContactInput): Promise<string> {
    try {
      // Calculate lead score and priority
      const leadScore = calculateLeadScore(data)
      const priority = getPriorityFromScore(leadScore)
      
      // Create contact submission
      const contact = await prisma.contactSubmission.create({
        data: {
          firstName: data.firstName,
          lastName: data.lastName,
          email: data.email,
          phone: data.phone,
          company: data.company,
          jobTitle: data.jobTitle,
          website: data.website,
          service: data.service,
          budget: data.budget,
          timeline: data.timeline,
          message: data.message,
          preferredContact: data.preferredContact || 'EMAIL',
          bestTimeToCall: data.bestTimeToCall,
          source: data.source,
          referrer: data.referrer,
          leadScore,
          priority,
          ipAddress: data.ipAddress,
          userAgent: data.userAgent,
          sessionId: data.sessionId,
          status: 'NEW'
        }
      })

      // Log initial activity
      await this.logActivity({
        contactId: contact.id,
        type: 'FORM_SUBMISSION',
        description: `Contact form submitted with lead score: ${leadScore}`,
        metadata: {
          leadScore,
          priority,
          service: data.service,
          budget: data.budget,
          timeline: data.timeline
        }
      })

      // Send auto-response email
      await this.sendAutoResponse(contact.id)
      
      // Send internal notifications
      await this.sendInternalNotifications(contact.id)
      
      // Sync to CRM
      await this.syncToCRM(contact.id)
      
      // Schedule follow-ups
      await this.scheduleFollowUps(contact.id, priority)
      
      return contact.id
      
    } catch (error) {
      console.error('Contact submission error:', error)
      throw new Error('Failed to submit contact form')
    }
  }

  async sendAutoResponse(contactId: string): Promise<void> {
    try {
      const contact = await prisma.contactSubmission.findUnique({
        where: { id: contactId }
      })
      
      if (!contact) throw new Error('Contact not found')
      
      // Get auto-response template
      const template = await prisma.contactTemplate.findFirst({
        where: { type: 'AUTO_RESPONSE', isActive: true }
      })
      
      const emailContent = this.processTemplate(
        template?.content || this.getDefaultAutoResponseTemplate(),
        {
          firstName: contact.firstName,
          lastName: contact.lastName,
          company: contact.company || 'your organization',
          service: this.getServiceDisplayName(contact.service),
          responseTime: this.getExpectedResponseTime(contact.priority)
        }
      )
      
      await this.transporter.sendMail({
        from: {
          name: process.env.EMAIL_FROM_NAME || 'Applied Innovations Corporation',
          address: process.env.EMAIL_FROM || 'contact@appliedinnovations.com'
        },
        to: contact.email,
        subject: template?.subject || `Thank you for contacting Applied Innovations Corporation`,
        html: emailContent
      })
      
      // Log activity
      await this.logActivity({
        contactId,
        type: 'EMAIL_SENT',
        description: 'Auto-response email sent',
        metadata: { emailType: 'auto-response' }
      })
      
    } catch (error) {
      console.error('Auto-response email error:', error)
      // Don't throw - this shouldn't fail the entire submission
    }
  }

  async sendInternalNotifications(contactId: string): Promise<void> {
    try {
      const contact = await prisma.contactSubmission.findUnique({
        where: { id: contactId }
      })
      
      if (!contact) return
      
      const notifications: ContactNotification[] = []
      
      // Email notification to sales team
      notifications.push({
        type: 'email',
        recipient: process.env.SALES_TEAM_EMAIL || 'sales@appliedinnovations.com',
        subject: `New ${contact.priority} Priority Lead: ${contact.firstName} ${contact.lastName}`,
        message: this.generateInternalNotificationEmail(contact),
        priority: contact.priority
      })
      
      // High priority notifications
      if (contact.priority === 'HIGH' || contact.priority === 'URGENT') {
        // Slack notification
        if (process.env.SLACK_WEBHOOK_URL) {
          notifications.push({
            type: 'slack',
            recipient: process.env.SLACK_WEBHOOK_URL,
            message: this.generateSlackNotification(contact),
            priority: contact.priority
          })
        }
        
        // Additional email for urgent leads
        if (contact.priority === 'URGENT') {
          notifications.push({
            type: 'email',
            recipient: process.env.INTERNAL_NOTIFICATION_EMAIL || 'team@appliedinnovations.com',
            subject: `🚨 URGENT LEAD: ${contact.firstName} ${contact.lastName} from ${contact.company}`,
            message: this.generateUrgentLeadEmail(contact),
            priority: contact.priority
          })
        }
      }
      
      // Send all notifications
      await Promise.all(notifications.map(notification => this.sendNotification(notification)))
      
    } catch (error) {
      console.error('Internal notification error:', error)
    }
  }

  async syncToCRM(contactId: string): Promise<void> {
    try {
      const contact = await prisma.contactSubmission.findUnique({
        where: { id: contactId }
      })
      
      if (!contact) return
      
      // Check if contact already exists in CRM
      let crmContact = await suiteCRM.findContactByEmail(contact.email)
      let crmId: string
      
      if (crmContact) {
        // Update existing contact
        await suiteCRM.updateContact(crmContact.id!, {
          first_name: contact.firstName,
          last_name: contact.lastName,
          phone_work: contact.phone || '',
          account_name: contact.company || '',
          title: contact.jobTitle || '',
          website: contact.website || '',
          lead_source: 'Website Contact Form',
          description: `Contact form inquiry: ${contact.message.substring(0, 200)}...`
        })
        crmId = crmContact.id!
      } else {
        // Create new contact
        crmId = await suiteCRM.createContact({
          email1: contact.email,
          first_name: contact.firstName,
          last_name: contact.lastName,
          phone_work: contact.phone || '',
          account_name: contact.company || '',
          title: contact.jobTitle || '',
          website: contact.website || '',
          lead_source: 'Website Contact Form',
          description: `Contact form inquiry: ${contact.message}`
        })
      }
      
      // Update contact with CRM ID
      await prisma.contactSubmission.update({
        where: { id: contactId },
        data: {
          crmId,
          crmSynced: true
        }
      })
      
      // Log CRM sync activity
      await this.logActivity({
        contactId,
        type: 'CRM_SYNC',
        description: `Contact synced to CRM with ID: ${crmId}`,
        metadata: { crmId, action: crmContact ? 'updated' : 'created' }
      })
      
    } catch (error) {
      console.error('CRM sync error:', error)
      
      // Update contact with sync error
      await prisma.contactSubmission.update({
        where: { id: contactId },
        data: {
          crmSyncError: error instanceof Error ? error.message : 'Unknown CRM sync error'
        }
      })
    }
  }

  async scheduleFollowUps(contactId: string, priority: string): Promise<void> {
    try {
      const followUps = []
      
      // Qualification call follow-up
      const qualificationDelay = this.getQualificationDelay(priority)
      followUps.push({
        contactId,
        type: 'QUALIFICATION_CALL' as const,
        scheduledFor: new Date(Date.now() + qualificationDelay),
        notes: 'Initial qualification call to understand requirements'
      })
      
      // Check-in follow-up
      const checkInDelay = this.getCheckInDelay(priority)
      followUps.push({
        contactId,
        type: 'CHECK_IN' as const,
        scheduledFor: new Date(Date.now() + checkInDelay),
        notes: 'Follow-up check-in if no response to initial contact'
      })
      
      // Create follow-up records
      await Promise.all(followUps.map(followUp => 
        prisma.contactFollowUp.create({ data: followUp })
      ))
      
    } catch (error) {
      console.error('Follow-up scheduling error:', error)
    }
  }

  async logActivity(activity: ContactActivityInput): Promise<void> {
    try {
      await prisma.contactActivity.create({
        data: activity
      })
    } catch (error) {
      console.error('Activity logging error:', error)
    }
  }

  private async sendNotification(notification: ContactNotification): Promise<void> {
    try {
      switch (notification.type) {
        case 'email':
          await this.transporter.sendMail({
            from: {
              name: process.env.EMAIL_FROM_NAME || 'AIC Contact System',
              address: process.env.EMAIL_FROM || 'contact@appliedinnovations.com'
            },
            to: notification.recipient,
            subject: notification.subject || 'New Contact Submission',
            html: notification.message
          })
          break
          
        case 'slack':
          if (process.env.SLACK_WEBHOOK_URL) {
            await fetch(process.env.SLACK_WEBHOOK_URL, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                text: notification.message,
                username: 'AIC Contact Bot',
                icon_emoji: notification.priority === 'URGENT' ? ':rotating_light:' : ':email:'
              })
            })
          }
          break
          
        case 'discord':
          if (process.env.DISCORD_WEBHOOK_URL) {
            await fetch(process.env.DISCORD_WEBHOOK_URL, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                content: notification.message,
                username: 'AIC Contact Bot'
              })
            })
          }
          break
      }
    } catch (error) {
      console.error(`${notification.type} notification error:`, error)
    }
  }

  private processTemplate(template: string, variables: Record<string, string>): string {
    let processed = template
    Object.entries(variables).forEach(([key, value]) => {
      processed = processed.replace(new RegExp(`{{${key}}}`, 'g'), value)
    })
    return processed
  }

  private getDefaultAutoResponseTemplate(): string {
    return `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <h2 style="color: #2563eb;">Thank you for contacting Applied Innovations Corporation!</h2>
      
      <p>Dear {{firstName}},</p>
      
      <p>Thank you for reaching out to us regarding {{service}} for {{company}}. We've received your inquiry and our team is reviewing your requirements.</p>
      
      <p><strong>What happens next:</strong></p>
      <ul>
        <li>One of our AI experts will review your inquiry within {{responseTime}}</li>
        <li>We'll reach out to schedule a consultation to discuss your specific needs</li>
        <li>You'll receive a customized proposal outlining how we can help</li>
      </ul>
      
      <p>In the meantime, feel free to explore our <a href="https://appliedinnovations.com/case-studies">case studies</a> and <a href="https://appliedinnovations.com/resources">resources</a> to learn more about our AI transformation approach.</p>
      
      <p>Best regards,<br>
      The Applied Innovations Team</p>
      
      <hr style="margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;">
      <p style="font-size: 12px; color: #6b7280;">
        Applied Innovations Corporation<br>
        Transforming businesses through intelligent AI solutions<br>
        <a href="https://appliedinnovations.com">appliedinnovations.com</a>
      </p>
    </div>
    `
  }

  private generateInternalNotificationEmail(contact: any): string {
    return `
    <div style="font-family: Arial, sans-serif;">
      <h2 style="color: ${this.getPriorityColor(contact.priority)};">
        New ${contact.priority} Priority Lead
      </h2>
      
      <table style="border-collapse: collapse; width: 100%;">
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Name:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${contact.firstName} ${contact.lastName}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Email:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${contact.email}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Company:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${contact.company || 'Not provided'}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Job Title:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${contact.jobTitle || 'Not provided'}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Phone:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${contact.phone || 'Not provided'}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Service Interest:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${this.getServiceDisplayName(contact.service)}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Budget:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${this.getBudgetDisplayName(contact.budget)}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Timeline:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${this.getTimelineDisplayName(contact.timeline)}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Lead Score:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${contact.leadScore}</td></tr>
      </table>
      
      <h3>Message:</h3>
      <div style="background: #f9fafb; padding: 15px; border-left: 4px solid #2563eb;">
        ${contact.message}
      </div>
      
      <p><a href="${process.env.NEXT_PUBLIC_APP_URL}/admin/contacts/${contact.id}" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View in Admin Dashboard</a></p>
    </div>
    `
  }

  private generateSlackNotification(contact: any): string {
    return `🚨 *New ${contact.priority} Priority Lead*

*${contact.firstName} ${contact.lastName}* from *${contact.company || 'Unknown Company'}*
📧 ${contact.email}
📞 ${contact.phone || 'No phone provided'}
💼 ${contact.jobTitle || 'Unknown role'}
🎯 Interested in: ${this.getServiceDisplayName(contact.service)}
💰 Budget: ${this.getBudgetDisplayName(contact.budget)}
⏰ Timeline: ${this.getTimelineDisplayName(contact.timeline)}
📊 Lead Score: ${contact.leadScore}

*Message:*
> ${contact.message.substring(0, 200)}${contact.message.length > 200 ? '...' : ''}

<${process.env.NEXT_PUBLIC_APP_URL}/admin/contacts/${contact.id}|View in Dashboard>`
  }

  private generateUrgentLeadEmail(contact: any): string {
    return `
    <div style="font-family: Arial, sans-serif; border: 3px solid #dc2626; padding: 20px; background: #fef2f2;">
      <h1 style="color: #dc2626; margin-top: 0;">🚨 URGENT LEAD ALERT</h1>
      
      <p style="font-size: 18px; font-weight: bold;">High-value prospect requires immediate attention!</p>
      
      <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
        <h2>${contact.firstName} ${contact.lastName}</h2>
        <p><strong>Company:</strong> ${contact.company}</p>
        <p><strong>Lead Score:</strong> ${contact.leadScore} (${contact.priority} Priority)</p>
        <p><strong>Budget:</strong> ${this.getBudgetDisplayName(contact.budget)}</p>
        <p><strong>Timeline:</strong> ${this.getTimelineDisplayName(contact.timeline)}</p>
      </div>
      
      <p style="color: #dc2626; font-weight: bold;">Recommended Action: Contact within 1 hour</p>
      
      <a href="${process.env.NEXT_PUBLIC_APP_URL}/admin/contacts/${contact.id}" 
         style="background: #dc2626; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
        VIEW LEAD DETAILS
      </a>
    </div>
    `
  }

  private getServiceDisplayName(service?: string): string {
    const serviceNames = {
      'strategy': 'AI Strategy & Assessment',
      'implementation': 'AI Implementation',
      'governance': 'AI Governance & Compliance',
      'training': 'Team Training & Enablement',
      'innovation': 'AI Innovation Consulting',
      'optimization': 'Performance Optimization',
      'other': 'Other Services'
    }
    return serviceNames[service as keyof typeof serviceNames] || 'Not specified'
  }

  private getBudgetDisplayName(budget?: string): string {
    const budgetNames = {
      'under-50k': 'Under $50K',
      '50k-100k': '$50K - $100K',
      '100k-250k': '$100K - $250K',
      '250k-500k': '$250K - $500K',
      '500k-1m': '$500K - $1M',
      'over-1m': 'Over $1M',
      'not-sure': 'Not Sure'
    }
    return budgetNames[budget as keyof typeof budgetNames] || 'Not specified'
  }

  private getTimelineDisplayName(timeline?: string): string {
    const timelineNames = {
      'immediate': 'Immediate',
      '1-3-months': '1-3 months',
      '3-6-months': '3-6 months',
      '6-12-months': '6-12 months',
      'over-12-months': 'Over 12 months',
      'not-sure': 'Not Sure'
    }
    return timelineNames[timeline as keyof typeof timelineNames] || 'Not specified'
  }

  private getPriorityColor(priority: string): string {
    const colors = {
      'URGENT': '#dc2626',
      'HIGH': '#ea580c',
      'MEDIUM': '#d97706',
      'LOW': '#65a30d'
    }
    return colors[priority as keyof typeof colors] || '#6b7280'
  }

  private getExpectedResponseTime(priority: string): string {
    const responseTimes = {
      'URGENT': '1 hour',
      'HIGH': '4 hours',
      'MEDIUM': '24 hours',
      'LOW': '48 hours'
    }
    return responseTimes[priority as keyof typeof responseTimes] || '24 hours'
  }

  private getQualificationDelay(priority: string): number {
    const delays = {
      'URGENT': 1 * 60 * 60 * 1000, // 1 hour
      'HIGH': 4 * 60 * 60 * 1000,   // 4 hours
      'MEDIUM': 24 * 60 * 60 * 1000, // 24 hours
      'LOW': 48 * 60 * 60 * 1000     // 48 hours
    }
    return delays[priority as keyof typeof delays] || delays.MEDIUM
  }

  private getCheckInDelay(priority: string): number {
    const delays = {
      'URGENT': 24 * 60 * 60 * 1000,  // 1 day
      'HIGH': 3 * 24 * 60 * 60 * 1000, // 3 days
      'MEDIUM': 7 * 24 * 60 * 60 * 1000, // 1 week
      'LOW': 14 * 24 * 60 * 60 * 1000   // 2 weeks
    }
    return delays[priority as keyof typeof delays] || delays.MEDIUM
  }
}

export const contactService = new ContactService()
