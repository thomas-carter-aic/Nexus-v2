import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { JobType } from '@prisma/client';

// GET /api/jobs - List all active job postings with optional filtering
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    // Extract query parameters
    const department = searchParams.get('department');
    const location = searchParams.get('location');
    const type = searchParams.get('type') as JobType | null;
    const search = searchParams.get('search');
    const includeInactive = searchParams.get('includeInactive') === 'true';
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');

    // Build where clause
    const where: any = {};
    
    if (!includeInactive) {
      where.isActive = true;
    }
    
    if (department) {
      where.department = department;
    }
    
    if (location) {
      where.location = {
        contains: location,
        mode: 'insensitive'
      };
    }
    
    if (type && Object.values(JobType).includes(type)) {
      where.type = type;
    }
    
    if (search) {
      where.OR = [
        {
          title: {
            contains: search,
            mode: 'insensitive'
          }
        },
        {
          description: {
            contains: search,
            mode: 'insensitive'
          }
        },
        {
          requirements: {
            hasSome: [search]
          }
        }
      ];
    }

    // Fetch jobs with pagination
    const [jobs, totalCount] = await Promise.all([
      prisma.jobPosting.findMany({
        where,
        orderBy: {
          createdAt: 'desc'
        },
        take: limit,
        skip: offset,
        include: {
          _count: {
            select: {
              applications: true
            }
          }
        }
      }),
      prisma.jobPosting.count({ where })
    ]);

    return NextResponse.json({
      jobs,
      pagination: {
        total: totalCount,
        limit,
        offset,
        hasMore: offset + limit < totalCount
      }
    });

  } catch (error) {
    console.error('Error fetching jobs:', error);
    return NextResponse.json(
      { error: 'Failed to fetch job postings' },
      { status: 500 }
    );
  }
}

// POST /api/jobs - Create a new job posting (Admin only)
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validate required fields
    const requiredFields = ['title', 'department', 'location', 'type', 'description'];
    for (const field of requiredFields) {
      if (!body[field]) {
        return NextResponse.json(
          { error: `Missing required field: ${field}` },
          { status: 400 }
        );
      }
    }

    // Validate job type
    if (!Object.values(JobType).includes(body.type)) {
      return NextResponse.json(
        { error: 'Invalid job type' },
        { status: 400 }
      );
    }

    // Create job posting
    const job = await prisma.jobPosting.create({
      data: {
        title: body.title,
        department: body.department,
        location: body.location,
        type: body.type,
        description: body.description,
        requirements: body.requirements || [],
        salary: body.salary || null,
        benefits: body.benefits || null,
        isActive: body.isActive !== undefined ? body.isActive : true
      }
    });

    return NextResponse.json(job, { status: 201 });

  } catch (error) {
    console.error('Error creating job posting:', error);
    return NextResponse.json(
      { error: 'Failed to create job posting' },
      { status: 500 }
    );
  }
}
