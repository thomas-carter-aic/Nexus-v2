# Job Application System - Development Setup Guide

This guide will help you set up the complete job application system development environment.

## 🚀 Quick Start

### Automated Setup (Recommended)

Run the automated installation script:

```bash
./install-careers-system.sh
```

This script will:
- ✅ Check system requirements
- ✅ Install dependencies
- ✅ Set up PostgreSQL database
- ✅ Configure environment variables
- ✅ Generate Prisma client
- ✅ Create database schema
- ✅ Seed sample data
- ✅ Create upload directories

### Manual Setup

If you prefer to set up manually or the automated script fails:

#### 1. Install Dependencies

```bash
npm install
```

#### 2. Set Up PostgreSQL Database

```bash
# Run database setup script
./scripts/setup-database.sh

# Or set up manually:
# - Install PostgreSQL
# - Create database: aic_careers
# - Create user: aic_user with password: aic_password
```

#### 3. Configure Environment

```bash
# Copy environment template
cp .env.careers.example .env.local

# Edit .env.local with your configuration
```

#### 4. Set Up Database Schema

```bash
# Generate Prisma client
npm run db:generate

# Push schema to database
npm run db:push

# Seed with sample data
npm run db:seed
```

#### 5. Create Upload Directories

```bash
mkdir -p uploads/resumes uploads/temp
chmod 755 uploads uploads/resumes uploads/temp
```

## 🔧 Configuration

### Environment Variables

Update `.env.local` with your configuration:

```env
# Database
DATABASE_URL="postgresql://aic_user:aic_password@localhost:5432/aic_careers?schema=public"

# File Storage
UPLOAD_DIR="./uploads"
MAX_FILE_SIZE="5242880"  # 5MB

# Email (Gmail SMTP example)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"
FROM_EMAIL="noreply@appliedinnovations.com"

# Admin
ADMIN_EMAIL="admin@appliedinnovations.com"
NOTIFICATION_EMAIL="hr@appliedinnovations.com"
```

### Email Setup (Gmail Example)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in `SMTP_PASS`

## 🚀 Running the Application

### Development Server

```bash
# Start with database generation
npm run careers:dev

# Or standard development
npm run dev
```

Visit:
- Main site: http://localhost:3000
- Careers page: http://localhost:3000/careers
- Admin portal: http://localhost:3000/admin

### Database Management

```bash
# Open Prisma Studio (Database GUI)
npm run db:studio

# Reset database (WARNING: Deletes all data)
npm run db:reset

# Seed database with sample data
npm run db:seed
```

## 📋 Available API Endpoints

### Job Postings

- `GET /api/jobs` - List all jobs (with filtering)
- `POST /api/jobs` - Create new job (Admin)
- `GET /api/jobs/[id]` - Get specific job
- `PUT /api/jobs/[id]` - Update job (Admin)
- `DELETE /api/jobs/[id]` - Delete job (Admin)

### Applications

- `POST /api/jobs/[id]/apply` - Submit application
- `GET /api/applications` - List applications (Admin)
- `POST /api/applications` - Bulk operations (Admin)

### Example API Usage

```bash
# List all jobs
curl http://localhost:3000/api/jobs

# Get specific job
curl http://localhost:3000/api/jobs/[job-id]

# Submit application (multipart/form-data)
curl -X POST http://localhost:3000/api/jobs/[job-id]/apply \
  -F "firstName=John" \
  -F "lastName=Doe" \
  -F "email=john@example.com" \
  -F "phone=555-0123" \
  -F "resume=@/path/to/resume.pdf" \
  -F "coverLetter=I am interested in this position..."
```

## 🧪 Testing

### Manual Testing Checklist

#### Job Listings
- [ ] View job listings at `/careers`
- [ ] Search and filter jobs
- [ ] View individual job details

#### Application Submission
- [ ] Click "Apply Now" on a job
- [ ] Fill out application form
- [ ] Upload resume (PDF/DOC/DOCX)
- [ ] Submit application
- [ ] Receive confirmation email

#### Admin Functions
- [ ] View applications in admin panel
- [ ] Create new job postings
- [ ] Update job posting status
- [ ] Review submitted applications

### Database Testing

```bash
# Check database connection
npm run db:studio

# Verify sample data
psql -h localhost -U aic_user -d aic_careers -c "SELECT COUNT(*) FROM job_postings;"
```

### Email Testing

```bash
# Test email configuration
node -e "
const { emailService } = require('./lib/email.ts');
emailService.verifyConnection().then(result => 
  console.log('Email test:', result ? 'SUCCESS' : 'FAILED')
);
"
```

## 🔍 Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Test connection manually
psql -h localhost -U aic_user -d aic_careers
```

#### File Upload Issues
```bash
# Check upload directory permissions
ls -la uploads/
chmod 755 uploads uploads/resumes uploads/temp
```

#### Email Not Working
- Verify SMTP credentials in `.env.local`
- Check Gmail App Password setup
- Test with a different SMTP provider

#### Prisma Issues
```bash
# Regenerate Prisma client
npm run db:generate

# Reset and recreate database
npm run db:reset
```

### Logs and Debugging

```bash
# View application logs
tail -f dev.log

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-*.log

# Enable Prisma query logging
# Add to .env.local: DATABASE_URL="...?logging=true"
```

## 📁 Project Structure

```
src/
├── app/
│   ├── api/
│   │   ├── jobs/
│   │   │   ├── route.ts              # List/create jobs
│   │   │   ├── [id]/
│   │   │   │   ├── route.ts          # Get/update/delete job
│   │   │   │   └── apply/
│   │   │   │       └── route.ts      # Submit application
│   │   └── applications/
│   │       └── route.ts              # List/manage applications
│   └── careers/                      # Frontend pages (to be implemented)
├── lib/
│   ├── prisma.ts                     # Database client
│   ├── storage.ts                    # File upload service
│   └── email.ts                      # Email service
├── prisma/
│   ├── schema.prisma                 # Database schema
│   └── seed.ts                       # Sample data
└── uploads/                          # File storage
    └── resumes/                      # Resume uploads
```

## 🎯 Next Steps

After successful setup:

1. **Phase 2**: Implement frontend components
   - Job listings page
   - Application modal/form
   - Search and filtering UI

2. **Phase 3**: Add advanced features
   - Application status tracking
   - Email notifications
   - Analytics dashboard

3. **Phase 4**: Production deployment
   - Environment configuration
   - Security hardening
   - Performance optimization

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review the logs for error messages
3. Verify your environment configuration
4. Test individual components (database, email, file upload)

For additional help, refer to the comprehensive documentation in `docs/05-job-application-system-architecture-20250704-220000.md`.
