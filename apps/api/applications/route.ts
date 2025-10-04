import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { ApplicationStatus } from '@prisma/client';

// GET /api/applications - List all applications (Admin only)
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    // Extract query parameters
    const jobId = searchParams.get('jobId');
    const status = searchParams.get('status') as ApplicationStatus | null;
    const search = searchParams.get('search');
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');
    const sortBy = searchParams.get('sortBy') || 'submittedAt';
    const sortOrder = searchParams.get('sortOrder') || 'desc';

    // Build where clause
    const where: any = {};
    
    if (jobId) {
      where.jobId = jobId;
    }
    
    if (status && Object.values(ApplicationStatus).includes(status)) {
      where.status = status;
    }
    
    if (search) {
      where.OR = [
        {
          firstName: {
            contains: search,
            mode: 'insensitive'
          }
        },
        {
          lastName: {
            contains: search,
            mode: 'insensitive'
          }
        },
        {
          email: {
            contains: search,
            mode: 'insensitive'
          }
        },
        {
          job: {
            title: {
              contains: search,
              mode: 'insensitive'
            }
          }
        }
      ];
    }

    // Build order by clause
    const orderBy: any = {};
    if (sortBy === 'applicantName') {
      orderBy.firstName = sortOrder;
    } else if (sortBy === 'jobTitle') {
      orderBy.job = { title: sortOrder };
    } else {
      orderBy[sortBy] = sortOrder;
    }

    // Fetch applications with pagination
    const [applications, totalCount] = await Promise.all([
      prisma.application.findMany({
        where,
        orderBy,
        take: limit,
        skip: offset,
        include: {
          job: {
            select: {
              id: true,
              title: true,
              department: true,
              location: true,
              type: true
            }
          }
        }
      }),
      prisma.application.count({ where })
    ]);

    return NextResponse.json({
      applications,
      pagination: {
        total: totalCount,
        limit,
        offset,
        hasMore: offset + limit < totalCount
      }
    });

  } catch (error) {
    console.error('Error fetching applications:', error);
    return NextResponse.json(
      { error: 'Failed to fetch applications' },
      { status: 500 }
    );
  }
}

// POST /api/applications - Bulk operations (Admin only)
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, applicationIds, data } = body;

    if (!action || !applicationIds || !Array.isArray(applicationIds)) {
      return NextResponse.json(
        { error: 'Missing required fields: action, applicationIds' },
        { status: 400 }
      );
    }

    let result;

    switch (action) {
      case 'updateStatus':
        if (!data?.status || !Object.values(ApplicationStatus).includes(data.status)) {
          return NextResponse.json(
            { error: 'Invalid status provided' },
            { status: 400 }
          );
        }

        result = await prisma.application.updateMany({
          where: {
            id: {
              in: applicationIds
            }
          },
          data: {
            status: data.status,
            reviewedAt: new Date(),
            reviewedBy: data.reviewedBy || null,
            notes: data.notes || null
          }
        });

        return NextResponse.json({
          success: true,
          message: `Updated ${result.count} applications`,
          updatedCount: result.count
        });

      case 'delete':
        result = await prisma.application.deleteMany({
          where: {
            id: {
              in: applicationIds
            }
          }
        });

        return NextResponse.json({
          success: true,
          message: `Deleted ${result.count} applications`,
          deletedCount: result.count
        });

      default:
        return NextResponse.json(
          { error: 'Invalid action' },
          { status: 400 }
        );
    }

  } catch (error) {
    console.error('Error performing bulk operation:', error);
    return NextResponse.json(
      { error: 'Failed to perform bulk operation' },
      { status: 500 }
    );
  }
}
