import nodemailer from 'nodemailer';
import { Application, JobPosting } from '@prisma/client';

export interface EmailConfig {
  host: string;
  port: number;
  secure: boolean;
  auth: {
    user: string;
    pass: string;
  };
  from: {
    email: string;
    name: string;
  };
}

export interface ApplicationEmailData extends Application {
  job: JobPosting;
}

export class EmailService {
  private transporter: nodemailer.Transporter;
  private config: EmailConfig;

  constructor() {
    this.config = {
      host: process.env.SMTP_HOST || 'smtp.gmail.com',
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER || '',
        pass: process.env.SMTP_PASS || '',
      },
      from: {
        email: process.env.FROM_EMAIL || 'noreply@appliedinnovations.com',
        name: process.env.FROM_NAME || 'Applied Innovations Corporation',
      },
    };

    this.transporter = nodemailer.createTransporter({
      host: this.config.host,
      port: this.config.port,
      secure: this.config.secure,
      auth: this.config.auth,
    });
  }

  /**
   * Verify email configuration
   */
  async verifyConnection(): Promise<boolean> {
    try {
      await this.transporter.verify();
      return true;
    } catch (error) {
      console.error('Email configuration error:', error);
      return false;
    }
  }

  /**
   * Send application confirmation email to applicant
   */
  async sendApplicationConfirmation(applicationData: ApplicationEmailData): Promise<boolean> {
    try {
      const { firstName, lastName, email, job } = applicationData;

      const mailOptions = {
        from: `${this.config.from.name} <${this.config.from.email}>`,
        to: email,
        subject: `Application Received - ${job.title} Position`,
        html: this.generateApplicationConfirmationHTML(applicationData),
        text: this.generateApplicationConfirmationText(applicationData),
      };

      await this.transporter.sendMail(mailOptions);
      return true;
    } catch (error) {
      console.error('Error sending application confirmation:', error);
      return false;
    }
  }

  /**
   * Send new application notification to HR/Admin
   */
  async sendNewApplicationNotification(applicationData: ApplicationEmailData): Promise<boolean> {
    try {
      const adminEmail = process.env.ADMIN_EMAIL || process.env.NOTIFICATION_EMAIL;
      if (!adminEmail) {
        console.warn('No admin email configured for notifications');
        return false;
      }

      const mailOptions = {
        from: `${this.config.from.name} <${this.config.from.email}>`,
        to: adminEmail,
        subject: `New Job Application - ${applicationData.job.title}`,
        html: this.generateNewApplicationNotificationHTML(applicationData),
        text: this.generateNewApplicationNotificationText(applicationData),
      };

      await this.transporter.sendMail(mailOptions);
      return true;
    } catch (error) {
      console.error('Error sending new application notification:', error);
      return false;
    }
  }

  /**
   * Send application status update email
   */
  async sendApplicationStatusUpdate(
    applicationData: ApplicationEmailData,
    newStatus: string,
    message?: string
  ): Promise<boolean> {
    try {
      const { firstName, lastName, email, job } = applicationData;

      const mailOptions = {
        from: `${this.config.from.name} <${this.config.from.email}>`,
        to: email,
        subject: `Application Update - ${job.title} Position`,
        html: this.generateStatusUpdateHTML(applicationData, newStatus, message),
        text: this.generateStatusUpdateText(applicationData, newStatus, message),
      };

      await this.transporter.sendMail(mailOptions);
      return true;
    } catch (error) {
      console.error('Error sending status update:', error);
      return false;
    }
  }

  /**
   * Generate HTML template for application confirmation
   */
  private generateApplicationConfirmationHTML(data: ApplicationEmailData): string {
    const { firstName, lastName, job, submittedAt } = data;
    
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>Application Confirmation</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background-color: #1e40af; color: white; padding: 20px; text-align: center; }
          .content { padding: 20px; background-color: #f9fafb; }
          .footer { padding: 20px; text-align: center; color: #666; font-size: 14px; }
          .button { display: inline-block; padding: 12px 24px; background-color: #1e40af; color: white; text-decoration: none; border-radius: 4px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Application Received</h1>
          </div>
          <div class="content">
            <h2>Dear ${firstName} ${lastName},</h2>
            <p>Thank you for your interest in the <strong>${job.title}</strong> position at Applied Innovations Corporation.</p>
            <p>We have successfully received your application submitted on ${new Date(submittedAt).toLocaleDateString()}.</p>
            
            <h3>What's Next?</h3>
            <ul>
              <li>Our hiring team will review your application and resume</li>
              <li>If your qualifications match our requirements, we'll contact you within 5-7 business days</li>
              <li>You may be invited for an initial phone screening or interview</li>
            </ul>
            
            <p>In the meantime, feel free to explore more opportunities on our careers page.</p>
            <p style="text-align: center;">
              <a href="${process.env.CAREERS_BASE_URL || 'http://localhost:3000/careers'}" class="button">View More Opportunities</a>
            </p>
          </div>
          <div class="footer">
            <p>Applied Innovations Corporation<br>
            Email: ${process.env.FROM_EMAIL}<br>
            This is an automated message, please do not reply.</p>
          </div>
        </div>
      </body>
      </html>
    `;
  }

  /**
   * Generate plain text template for application confirmation
   */
  private generateApplicationConfirmationText(data: ApplicationEmailData): string {
    const { firstName, lastName, job, submittedAt } = data;
    
    return `
Dear ${firstName} ${lastName},

Thank you for your interest in the ${job.title} position at Applied Innovations Corporation.

We have successfully received your application submitted on ${new Date(submittedAt).toLocaleDateString()}.

What's Next?
- Our hiring team will review your application and resume
- If your qualifications match our requirements, we'll contact you within 5-7 business days
- You may be invited for an initial phone screening or interview

In the meantime, feel free to explore more opportunities on our careers page: ${process.env.CAREERS_BASE_URL || 'http://localhost:3000/careers'}

Best regards,
Applied Innovations Corporation
${process.env.FROM_EMAIL}

This is an automated message, please do not reply.
    `;
  }

  /**
   * Generate HTML template for new application notification
   */
  private generateNewApplicationNotificationHTML(data: ApplicationEmailData): string {
    const { firstName, lastName, email, phone, job, resumeUrl, coverLetter, submittedAt } = data;
    
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>New Job Application</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background-color: #059669; color: white; padding: 20px; text-align: center; }
          .content { padding: 20px; background-color: #f9fafb; }
          .info-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
          .info-table th, .info-table td { padding: 10px; border: 1px solid #ddd; text-align: left; }
          .info-table th { background-color: #f3f4f6; }
          .button { display: inline-block; padding: 12px 24px; background-color: #059669; color: white; text-decoration: none; border-radius: 4px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>New Job Application Received</h1>
          </div>
          <div class="content">
            <h2>Application Details</h2>
            <table class="info-table">
              <tr><th>Position</th><td>${job.title}</td></tr>
              <tr><th>Department</th><td>${job.department}</td></tr>
              <tr><th>Applicant Name</th><td>${firstName} ${lastName}</td></tr>
              <tr><th>Email</th><td>${email}</td></tr>
              <tr><th>Phone</th><td>${phone}</td></tr>
              <tr><th>Submitted</th><td>${new Date(submittedAt).toLocaleString()}</td></tr>
              <tr><th>Resume</th><td><a href="${process.env.NEXT_PUBLIC_BASE_URL}${resumeUrl}">Download Resume</a></td></tr>
            </table>
            
            ${coverLetter ? `
            <h3>Cover Letter</h3>
            <div style="background: white; padding: 15px; border-left: 4px solid #059669; margin: 15px 0;">
              ${coverLetter.replace(/\n/g, '<br>')}
            </div>
            ` : ''}
            
            <p style="text-align: center; margin-top: 30px;">
              <a href="${process.env.NEXT_PUBLIC_BASE_URL}/admin/jobs/applications" class="button">Review in Admin Panel</a>
            </p>
          </div>
        </div>
      </body>
      </html>
    `;
  }

  /**
   * Generate plain text template for new application notification
   */
  private generateNewApplicationNotificationText(data: ApplicationEmailData): string {
    const { firstName, lastName, email, phone, job, resumeUrl, coverLetter, submittedAt } = data;
    
    return `
New Job Application Received

Position: ${job.title}
Department: ${job.department}
Applicant: ${firstName} ${lastName}
Email: ${email}
Phone: ${phone}
Submitted: ${new Date(submittedAt).toLocaleString()}
Resume: ${process.env.NEXT_PUBLIC_BASE_URL}${resumeUrl}

${coverLetter ? `Cover Letter:\n${coverLetter}\n` : ''}

Review in Admin Panel: ${process.env.NEXT_PUBLIC_BASE_URL}/admin/jobs/applications
    `;
  }

  /**
   * Generate HTML template for status updates
   */
  private generateStatusUpdateHTML(data: ApplicationEmailData, newStatus: string, message?: string): string {
    const { firstName, lastName, job } = data;
    
    const statusMessages: Record<string, string> = {
      'UNDER_REVIEW': 'Your application is currently under review by our hiring team.',
      'INTERVIEW_SCHEDULED': 'Congratulations! We would like to schedule an interview with you.',
      'INTERVIEWED': 'Thank you for taking the time to interview with us.',
      'OFFER_EXTENDED': 'Congratulations! We are pleased to extend you an offer.',
      'HIRED': 'Welcome to the Applied Innovations Corporation team!',
      'REJECTED': 'Thank you for your interest. We have decided to move forward with other candidates.',
      'WITHDRAWN': 'We have received your request to withdraw your application.'
    };

    const statusMessage = message || statusMessages[newStatus] || 'Your application status has been updated.';
    
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>Application Status Update</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background-color: #7c3aed; color: white; padding: 20px; text-align: center; }
          .content { padding: 20px; background-color: #f9fafb; }
          .status { padding: 15px; background-color: #e0e7ff; border-left: 4px solid #7c3aed; margin: 20px 0; }
          .footer { padding: 20px; text-align: center; color: #666; font-size: 14px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Application Status Update</h1>
          </div>
          <div class="content">
            <h2>Dear ${firstName} ${lastName},</h2>
            <p>We have an update regarding your application for the <strong>${job.title}</strong> position.</p>
            
            <div class="status">
              <h3>Status: ${newStatus.replace(/_/g, ' ')}</h3>
              <p>${statusMessage}</p>
            </div>
            
            <p>If you have any questions, please don't hesitate to contact our HR team.</p>
          </div>
          <div class="footer">
            <p>Applied Innovations Corporation<br>
            Email: ${process.env.FROM_EMAIL}</p>
          </div>
        </div>
      </body>
      </html>
    `;
  }

  /**
   * Generate plain text template for status updates
   */
  private generateStatusUpdateText(data: ApplicationEmailData, newStatus: string, message?: string): string {
    const { firstName, lastName, job } = data;
    
    const statusMessages: Record<string, string> = {
      'UNDER_REVIEW': 'Your application is currently under review by our hiring team.',
      'INTERVIEW_SCHEDULED': 'Congratulations! We would like to schedule an interview with you.',
      'INTERVIEWED': 'Thank you for taking the time to interview with us.',
      'OFFER_EXTENDED': 'Congratulations! We are pleased to extend you an offer.',
      'HIRED': 'Welcome to the Applied Innovations Corporation team!',
      'REJECTED': 'Thank you for your interest. We have decided to move forward with other candidates.',
      'WITHDRAWN': 'We have received your request to withdraw your application.'
    };

    const statusMessage = message || statusMessages[newStatus] || 'Your application status has been updated.';
    
    return `
Dear ${firstName} ${lastName},

We have an update regarding your application for the ${job.title} position.

Status: ${newStatus.replace(/_/g, ' ')}
${statusMessage}

If you have any questions, please don't hesitate to contact our HR team.

Best regards,
Applied Innovations Corporation
${process.env.FROM_EMAIL}
    `;
  }
}

// Export singleton instance
export const emailService = new EmailService();
