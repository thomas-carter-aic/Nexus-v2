# Job Application System Architecture - Open Source Implementation

**Document ID**: 05-job-application-system-architecture-20250704-220000  
**Date**: July 4, 2025  
**Time**: 22:00:00 UTC  
**Project**: Applied Innovations Corporation - Next.js Application  

## Executive Summary

This document outlines a comprehensive, open-source job application system architecture designed to integrate seamlessly with the existing Next.js application. The solution enables dynamic job posting viewing, application submission, resume upload, and job searching capabilities using only best-of-breed, free, open-source technologies.

## System Requirements

### Core Functionality
- View job postings dynamically
- Fill out and submit job applications
- Upload and manage resumes
- Search and filter job opportunities
- Dynamic "Apply Now" functionality
- Administrative job management interface

### Technical Constraints
- Must use only free, open-source solutions
- Integration with existing Next.js App Router architecture
- Maintain consistency with current portal system design
- Scalable and maintainable codebase

## Recommended Technology Stack

### Core Framework
- **Next.js 15.3.5** (existing) - App Router with API routes
- **TypeScript** (existing) - Type safety and developer experience
- **Tailwind CSS** (existing) - Consistent styling framework

### Database & ORM
- **PostgreSQL** - Robust, free, handles complex queries
- **Prisma ORM** - Type-safe database operations with excellent Next.js integration
- **Installation**: `npm install prisma @prisma/client`

### File Storage Solutions
- **Primary**: MinIO - S3-compatible object storage (self-hosted)
- **Alternative**: AWS S3 (free tier) or Cloudinary (generous free tier)
- **Local Development**: File system storage with organized directory structure

### Form Handling & Validation
- **React Hook Form** - Lightweight, performant form management
- **Zod** - Runtime validation with TypeScript integration
- **Installation**: `npm install react-hook-form @hookform/resolvers zod`

### Search & Filtering
- **PostgreSQL Full-Text Search** - Built-in, no additional dependencies
- **Alternative**: Elasticsearch for advanced search requirements

## Database Schema Design

### Core Entities

```sql
-- Job Postings Table
CREATE TABLE job_postings (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR NOT NULL,
    department VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    type VARCHAR NOT NULL, -- full-time, part-time, contract
    description TEXT NOT NULL,
    requirements TEXT[],
    salary VARCHAR,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Applications Table
CREATE TABLE applications (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id VARCHAR REFERENCES job_postings(id),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    resume_url VARCHAR NOT NULL,
    cover_letter TEXT,
    status VARCHAR DEFAULT 'submitted',
    submitted_at TIMESTAMP DEFAULT NOW()
);
```

### Prisma Schema Implementation

```typescript
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model JobPosting {
  id          String   @id @default(cuid())
  title       String
  department  String
  location    String
  type        String   // full-time, part-time, contract
  description String
  requirements String[]
  salary      String?
  isActive    Boolean  @default(true) @map("is_active")
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")
  
  applications Application[]
  
  @@map("job_postings")
}

model Application {
  id           String   @id @default(cuid())
  jobId        String   @map("job_id")
  firstName    String   @map("first_name")
  lastName     String   @map("last_name")
  email        String
  phone        String
  resumeUrl    String   @map("resume_url")
  coverLetter  String?  @map("cover_letter")
  status       String   @default("submitted")
  submittedAt  DateTime @default(now()) @map("submitted_at")
  
  job JobPosting @relation(fields: [jobId], references: [id])
  
  @@map("applications")
}
```

## API Architecture

### Endpoint Structure

```
/api/jobs/
├── route.ts                 # GET (list jobs), POST (create job)
├── [id]/route.ts           # GET (job details), PUT (update), DELETE
├── [id]/apply/route.ts     # POST (submit application)
└── search/route.ts         # GET (search jobs with filters)

/api/applications/
├── route.ts                # GET (list applications - admin only)
├── [id]/route.ts          # GET (application details), PUT (update status)
└── export/route.ts        # GET (export applications - CSV/Excel)
```

### API Implementation Examples

#### Job Listings API
```typescript
// app/api/jobs/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const department = searchParams.get('department');
  const location = searchParams.get('location');
  const type = searchParams.get('type');
  const search = searchParams.get('search');

  const where = {
    isActive: true,
    ...(department && { department }),
    ...(location && { location }),
    ...(type && { type }),
    ...(search && {
      OR: [
        { title: { contains: search, mode: 'insensitive' } },
        { description: { contains: search, mode: 'insensitive' } }
      ]
    })
  };

  const jobs = await prisma.jobPosting.findMany({
    where,
    orderBy: { createdAt: 'desc' }
  });

  return NextResponse.json(jobs);
}

export async function POST(request: NextRequest) {
  const data = await request.json();
  
  const job = await prisma.jobPosting.create({
    data: {
      title: data.title,
      department: data.department,
      location: data.location,
      type: data.type,
      description: data.description,
      requirements: data.requirements,
      salary: data.salary
    }
  });

  return NextResponse.json(job, { status: 201 });
}
```

#### Application Submission API
```typescript
// app/api/jobs/[id]/apply/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import path from 'path';
import { prisma } from '@/lib/prisma';

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const formData = await request.formData();
    const resume = formData.get('resume') as File;
    
    if (!resume) {
      return NextResponse.json(
        { error: 'Resume file is required' },
        { status: 400 }
      );
    }

    // Validate file type and size
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!allowedTypes.includes(resume.type)) {
      return NextResponse.json(
        { error: 'Invalid file type. Please upload PDF or Word document.' },
        { status: 400 }
      );
    }

    if (resume.size > 5 * 1024 * 1024) { // 5MB limit
      return NextResponse.json(
        { error: 'File size too large. Maximum 5MB allowed.' },
        { status: 400 }
      );
    }

    // Save file
    const bytes = await resume.arrayBuffer();
    const buffer = Buffer.from(bytes);
    
    const filename = `${Date.now()}-${resume.name.replace(/[^a-zA-Z0-9.-]/g, '_')}`;
    const uploadDir = path.join(process.cwd(), 'uploads', 'resumes');
    const filepath = path.join(uploadDir, filename);
    
    // Ensure upload directory exists
    await fs.mkdir(uploadDir, { recursive: true });
    await writeFile(filepath, buffer);

    // Create application record
    const application = await prisma.application.create({
      data: {
        jobId: params.id,
        firstName: formData.get('firstName') as string,
        lastName: formData.get('lastName') as string,
        email: formData.get('email') as string,
        phone: formData.get('phone') as string,
        resumeUrl: `/uploads/resumes/${filename}`,
        coverLetter: formData.get('coverLetter') as string || null,
      },
      include: {
        job: {
          select: {
            title: true,
            department: true
          }
        }
      }
    });

    // Send confirmation email (implement with Nodemailer)
    // await sendApplicationConfirmation(application);

    return NextResponse.json({
      success: true,
      applicationId: application.id,
      message: 'Application submitted successfully'
    });

  } catch (error) {
    console.error('Application submission error:', error);
    return NextResponse.json(
      { error: 'Failed to submit application' },
      { status: 500 }
    );
  }
}
```

## Frontend Implementation

### Directory Structure Integration
```
app/
├── careers/
│   ├── page.tsx                    # Job listings page
│   ├── [id]/
│   │   └── page.tsx               # Job details page
│   ├── components/
│   │   ├── JobCard.tsx
│   │   ├── JobSearch.tsx
│   │   ├── ApplicationModal.tsx
│   │   └── ApplicationForm.tsx
│   └── layout.tsx                 # Careers section layout
├── admin/
│   ├── jobs/
│   │   ├── page.tsx              # Job management dashboard
│   │   ├── [id]/
│   │   │   └── page.tsx          # Edit job posting
│   │   └── applications/
│   │       └── page.tsx          # Application management
│   └── (existing admin structure)
└── api/
    ├── jobs/
    └── applications/
```

### Core Components

#### Job Listings Page
```typescript
// app/careers/page.tsx
import { Suspense } from 'react';
import { JobSearch } from './components/JobSearch';
import { JobGrid } from './components/JobGrid';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

interface SearchParams {
  department?: string;
  location?: string;
  type?: string;
  search?: string;
}

export default async function CareersPage({
  searchParams
}: {
  searchParams: SearchParams;
}) {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Join Our Team
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Discover exciting opportunities to grow your career with Applied Innovations Corporation
          </p>
        </div>

        <JobSearch />
        
        <Suspense fallback={<LoadingSpinner />}>
          <JobGrid searchParams={searchParams} />
        </Suspense>
      </div>
    </div>
  );
}
```

#### Dynamic Application Modal
```typescript
// app/careers/components/ApplicationModal.tsx
'use client';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';

const applicationSchema = z.object({
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),
  email: z.string().email('Valid email is required'),
  phone: z.string().min(10, 'Valid phone number is required'),
  resume: z.instanceof(File, { message: 'Resume is required' }),
  coverLetter: z.string().optional(),
});

type ApplicationFormData = z.infer<typeof applicationSchema>;

interface ApplicationModalProps {
  jobId: string;
  jobTitle: string;
  isOpen: boolean;
  onClose: () => void;
}

export function ApplicationModal({ jobId, jobTitle, isOpen, onClose }: ApplicationModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<ApplicationFormData>({
    resolver: zodResolver(applicationSchema)
  });

  const onSubmit = async (data: ApplicationFormData) => {
    setIsSubmitting(true);
    
    try {
      const formData = new FormData();
      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined) {
          formData.append(key, value);
        }
      });

      const response = await fetch(`/api/jobs/${jobId}/apply`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setSubmitSuccess(true);
        reset();
        setTimeout(() => {
          onClose();
          setSubmitSuccess(false);
        }, 2000);
      } else {
        const error = await response.json();
        throw new Error(error.message || 'Failed to submit application');
      }
    } catch (error) {
      console.error('Application submission error:', error);
      // Handle error (show toast notification)
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitSuccess) {
    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="sm:max-w-md">
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Application Submitted!
            </h3>
            <p className="text-gray-600">
              Thank you for your interest. We'll review your application and get back to you soon.
            </p>
          </div>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Apply for {jobTitle}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="firstName">First Name *</Label>
              <Input
                id="firstName"
                {...register('firstName')}
                className={errors.firstName ? 'border-red-500' : ''}
              />
              {errors.firstName && (
                <p className="text-red-500 text-sm mt-1">{errors.firstName.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="lastName">Last Name *</Label>
              <Input
                id="lastName"
                {...register('lastName')}
                className={errors.lastName ? 'border-red-500' : ''}
              />
              {errors.lastName && (
                <p className="text-red-500 text-sm mt-1">{errors.lastName.message}</p>
              )}
            </div>
          </div>

          <div>
            <Label htmlFor="email">Email Address *</Label>
            <Input
              id="email"
              type="email"
              {...register('email')}
              className={errors.email ? 'border-red-500' : ''}
            />
            {errors.email && (
              <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
            )}
          </div>

          <div>
            <Label htmlFor="phone">Phone Number *</Label>
            <Input
              id="phone"
              type="tel"
              {...register('phone')}
              className={errors.phone ? 'border-red-500' : ''}
            />
            {errors.phone && (
              <p className="text-red-500 text-sm mt-1">{errors.phone.message}</p>
            )}
          </div>

          <div>
            <Label htmlFor="resume">Resume *</Label>
            <Input
              id="resume"
              type="file"
              accept=".pdf,.doc,.docx"
              {...register('resume')}
              className={errors.resume ? 'border-red-500' : ''}
            />
            {errors.resume && (
              <p className="text-red-500 text-sm mt-1">{errors.resume.message}</p>
            )}
            <p className="text-gray-500 text-sm mt-1">
              Accepted formats: PDF, DOC, DOCX (Max 5MB)
            </p>
          </div>

          <div>
            <Label htmlFor="coverLetter">Cover Letter (Optional)</Label>
            <Textarea
              id="coverLetter"
              rows={4}
              {...register('coverLetter')}
              placeholder="Tell us why you're interested in this position..."
            />
          </div>

          <div className="flex justify-end space-x-4 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting}
              className="min-w-[120px]"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Application'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

## Admin Portal Integration

### Job Management Dashboard
```typescript
// app/admin/jobs/page.tsx
import { JobManagementTable } from './components/JobManagementTable';
import { CreateJobButton } from './components/CreateJobButton';
import { JobAnalytics } from './components/JobAnalytics';

export default async function JobManagementPage() {
  const jobs = await fetch('/api/jobs?includeInactive=true').then(res => res.json());
  const applications = await fetch('/api/applications').then(res => res.json());

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Job Management</h1>
          <p className="text-gray-600 mt-2">Manage job postings and applications</p>
        </div>
        <CreateJobButton />
      </div>

      <JobAnalytics jobs={jobs} applications={applications} />
      
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Job Postings</h2>
        </div>
        <JobManagementTable jobs={jobs} />
      </div>
    </div>
  );
}
```

## Security Considerations

### File Upload Security
- File type validation (PDF, DOC, DOCX only)
- File size limits (5MB maximum)
- Virus scanning integration (ClamAV for open-source solution)
- Secure file storage with access controls
- File name sanitization to prevent path traversal

### Data Protection
- Input validation using Zod schemas
- SQL injection prevention through Prisma ORM
- Rate limiting on API endpoints
- CSRF protection for form submissions
- Secure file serving with proper headers

### Access Control
- Admin-only endpoints for job management
- Application data privacy (only accessible to admins and applicant)
- Audit logging for sensitive operations
- Session management and authentication

## Performance Optimization

### Database Optimization
- Proper indexing on frequently queried fields
- Database connection pooling
- Query optimization with Prisma
- Pagination for large result sets

### File Storage Optimization
- CDN integration for resume serving
- Compression for uploaded files
- Lazy loading for job listings
- Caching strategies for job data

### Frontend Performance
- Server-side rendering for SEO
- Image optimization for job-related media
- Code splitting for career section
- Progressive loading for job search results

## Deployment Considerations

### Environment Setup
```bash
# Database setup
DATABASE_URL="postgresql://username:password@localhost:5432/aic_careers"

# File storage
UPLOAD_DIR="/var/www/uploads"
MAX_FILE_SIZE="5242880" # 5MB in bytes

# Email configuration (for notifications)
SMTP_HOST="smtp.example.com"
SMTP_PORT="587"
SMTP_USER="noreply@appliedinnovations.com"
SMTP_PASS="your-smtp-password"
```

### Production Deployment
- Docker containerization for consistent deployment
- Environment variable management
- Database migration scripts
- File storage backup strategies
- Monitoring and logging setup

## Integration Timeline

### Phase 1: Core Infrastructure (Week 1)
- Database schema implementation
- Basic API endpoints
- File upload functionality
- Admin job management interface

### Phase 2: Frontend Development (Week 2)
- Job listings page
- Application modal/form
- Search and filtering
- Responsive design implementation

### Phase 3: Advanced Features (Week 3)
- Email notifications
- Application status tracking
- Analytics and reporting
- Security hardening

### Phase 4: Testing & Deployment (Week 4)
- Comprehensive testing
- Performance optimization
- Production deployment
- Documentation completion

## Maintenance and Monitoring

### Regular Maintenance Tasks
- Database cleanup of old applications
- File storage management
- Security updates and patches
- Performance monitoring and optimization

### Monitoring Metrics
- Application submission rates
- Job posting performance
- System resource usage
- Error rates and response times

## Conclusion

This architecture provides a comprehensive, scalable job application system using only free, open-source technologies. The solution integrates seamlessly with the existing Next.js application while maintaining consistency with the current portal design patterns. The modular approach allows for incremental implementation and future enhancements while ensuring security, performance, and maintainability.

The system leverages the existing infrastructure and design patterns, making it a natural extension of the current application rather than a separate system. This approach minimizes development time while maximizing code reuse and maintaining architectural consistency.

---

**Next Steps**: 
1. Review and approve the proposed architecture
2. Set up development environment with PostgreSQL and Prisma
3. Begin Phase 1 implementation with database schema and basic API endpoints
4. Establish testing protocols and deployment procedures

**Dependencies**: 
- PostgreSQL database setup
- File storage solution configuration
- SMTP service for email notifications
- Development environment preparation
