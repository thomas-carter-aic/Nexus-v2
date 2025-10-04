import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { fileStorage } from '@/lib/storage';
import { emailService } from '@/lib/email';

// POST /api/jobs/[id]/apply - Submit job application
export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  try {
    // Check if job exists and is active
    const job = await prisma.jobPosting.findUnique({
      where: { id }
    });

    if (!job) {
      return NextResponse.json(
        { error: 'Job posting not found' },
        { status: 404 }
      );
    }

    if (!job.isActive) {
      return NextResponse.json(
        { error: 'This job posting is no longer accepting applications' },
        { status: 400 }
      );
    }

    // Parse form data
    const formData = await request.formData();
    
    // Extract form fields
    const firstName = formData.get('firstName') as string;
    const lastName = formData.get('lastName') as string;
    const email = formData.get('email') as string;
    const phone = formData.get('phone') as string;
    const coverLetter = formData.get('coverLetter') as string;
    const resume = formData.get('resume') as File;

    // Validate required fields
    if (!firstName || !lastName || !email || !phone || !resume) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      );
    }

    // Check for duplicate application
    const existingApplication = await prisma.application.findFirst({
      where: {
        jobId: params.id,
        email: email
      }
    });

    if (existingApplication) {
      return NextResponse.json(
        { error: 'You have already applied for this position' },
        { status: 400 }
      );
    }

    // Upload resume file
    let uploadedFile;
    try {
      uploadedFile = await fileStorage.uploadFile(resume, 'resumes');
    } catch (uploadError) {
      console.error('File upload error:', uploadError);
      return NextResponse.json(
        { error: uploadError instanceof Error ? uploadError.message : 'File upload failed' },
        { status: 400 }
      );
    }

    // Create application record
    const application = await prisma.application.create({
      data: {
        jobId: params.id,
        firstName,
        lastName,
        email,
        phone,
        resumeUrl: uploadedFile.url,
        coverLetter: coverLetter || null,
        status: 'SUBMITTED'
      },
      include: {
        job: true
      }
    });

    // Send confirmation email to applicant
    try {
      await emailService.sendApplicationConfirmation(application);
    } catch (emailError) {
      console.error('Error sending confirmation email:', emailError);
      // Don't fail the application if email fails
    }

    // Send notification email to admin
    try {
      await emailService.sendNewApplicationNotification(application);
    } catch (emailError) {
      console.error('Error sending admin notification:', emailError);
      // Don't fail the application if email fails
    }

    // Return success response (without sensitive data)
    return NextResponse.json({
      success: true,
      applicationId: application.id,
      message: 'Application submitted successfully',
      data: {
        jobTitle: job.title,
        applicantName: `${firstName} ${lastName}`,
        submittedAt: application.submittedAt
      }
    }, { status: 201 });

  } catch (error) {
    console.error('Application submission error:', error);
    
    // Clean up uploaded file if application creation failed
    // This would be implemented based on your file storage solution
    
    return NextResponse.json(
      { error: 'Failed to submit application. Please try again.' },
      { status: 500 }
    );
  }
}
