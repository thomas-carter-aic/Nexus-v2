import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// GET /api/jobs/[id] - Get specific job posting
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  try {
    const job = await prisma.jobPosting.findUnique({
      where: {
        id
      },
      include: {
        _count: {
          select: {
            applications: true
          }
        }
      }
    });

    if (!job) {
      return NextResponse.json(
        { error: 'Job posting not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(job);

  } catch (error) {
    console.error('Error fetching job:', error);
    return NextResponse.json(
      { error: 'Failed to fetch job posting' },
      { status: 500 }
    );
  }
}

// PUT /api/jobs/[id] - Update job posting (Admin only)
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();

    // Check if job exists
    const existingJob = await prisma.jobPosting.findUnique({
      where: { id: params.id }
    });

    if (!existingJob) {
      return NextResponse.json(
        { error: 'Job posting not found' },
        { status: 404 }
      );
    }

    // Update job posting
    const updatedJob = await prisma.jobPosting.update({
      where: {
        id: params.id
      },
      data: {
        ...(body.title && { title: body.title }),
        ...(body.department && { department: body.department }),
        ...(body.location && { location: body.location }),
        ...(body.type && { type: body.type }),
        ...(body.description && { description: body.description }),
        ...(body.requirements && { requirements: body.requirements }),
        ...(body.salary !== undefined && { salary: body.salary }),
        ...(body.benefits !== undefined && { benefits: body.benefits }),
        ...(body.isActive !== undefined && { isActive: body.isActive }),
        updatedAt: new Date()
      }
    });

    return NextResponse.json(updatedJob);

  } catch (error) {
    console.error('Error updating job:', error);
    return NextResponse.json(
      { error: 'Failed to update job posting' },
      { status: 500 }
    );
  }
}

// DELETE /api/jobs/[id] - Delete job posting (Admin only)
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // Check if job exists
    const existingJob = await prisma.jobPosting.findUnique({
      where: { id: params.id },
      include: {
        _count: {
          select: {
            applications: true
          }
        }
      }
    });

    if (!existingJob) {
      return NextResponse.json(
        { error: 'Job posting not found' },
        { status: 404 }
      );
    }

    // Check if there are applications
    if (existingJob._count.applications > 0) {
      return NextResponse.json(
        { error: 'Cannot delete job posting with existing applications. Consider deactivating instead.' },
        { status: 400 }
      );
    }

    // Delete job posting
    await prisma.jobPosting.delete({
      where: {
        id: params.id
      }
    });

    return NextResponse.json(
      { message: 'Job posting deleted successfully' },
      { status: 200 }
    );

  } catch (error) {
    console.error('Error deleting job:', error);
    return NextResponse.json(
      { error: 'Failed to delete job posting' },
      { status: 500 }
    );
  }
}
