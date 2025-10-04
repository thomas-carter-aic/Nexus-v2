import { PrismaClient, JobType } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seed...');

  // Create sample job postings
  const jobPostings = [
    {
      title: 'Senior Software Engineer',
      department: 'Engineering',
      location: 'Remote',
      type: JobType.FULL_TIME,
      description: `We are seeking a Senior Software Engineer to join our dynamic team. You will be responsible for designing, developing, and maintaining high-quality software solutions that drive our business forward.

Key Responsibilities:
• Design and develop scalable web applications
• Collaborate with cross-functional teams to define and implement new features
• Write clean, maintainable, and efficient code
• Participate in code reviews and mentor junior developers
• Troubleshoot and debug applications
• Stay up-to-date with emerging technologies and industry trends`,
      requirements: [
        'Bachelor\'s degree in Computer Science or related field',
        '5+ years of experience in software development',
        'Proficiency in JavaScript, TypeScript, React, and Node.js',
        'Experience with cloud platforms (AWS, Azure, or GCP)',
        'Strong understanding of database design and SQL',
        'Experience with version control systems (Git)',
        'Excellent problem-solving and communication skills'
      ],
      salary: '$120,000 - $160,000',
      benefits: 'Comprehensive health insurance, 401(k) matching, flexible PTO, remote work options, professional development budget'
    },
    {
      title: 'Product Manager',
      department: 'Product',
      location: 'New York, NY',
      type: JobType.FULL_TIME,
      description: `Join our Product team as a Product Manager and help shape the future of our AI-powered solutions. You will work closely with engineering, design, and business teams to deliver exceptional products.

Key Responsibilities:
• Define product strategy and roadmap
• Gather and prioritize product requirements
• Work closely with engineering teams to deliver products
• Analyze market trends and competitive landscape
• Collaborate with stakeholders across the organization
• Monitor product performance and user feedback`,
      requirements: [
        'Bachelor\'s degree in Business, Engineering, or related field',
        '3+ years of product management experience',
        'Experience with AI/ML products preferred',
        'Strong analytical and problem-solving skills',
        'Excellent communication and leadership abilities',
        'Experience with product management tools (Jira, Confluence, etc.)',
        'Understanding of software development lifecycle'
      ],
      salary: '$110,000 - $140,000',
      benefits: 'Health insurance, dental and vision coverage, 401(k) matching, stock options, flexible work arrangements'
    },
    {
      title: 'UX/UI Designer',
      department: 'Design',
      location: 'San Francisco, CA',
      type: JobType.FULL_TIME,
      description: `We are looking for a talented UX/UI Designer to create amazing user experiences for our AI-powered applications. You will be responsible for the entire design process from concept to implementation.

Key Responsibilities:
• Design user interfaces for web and mobile applications
• Create wireframes, prototypes, and high-fidelity mockups
• Conduct user research and usability testing
• Collaborate with product managers and developers
• Maintain and evolve our design system
• Present design concepts to stakeholders`,
      requirements: [
        'Bachelor\'s degree in Design, HCI, or related field',
        '4+ years of UX/UI design experience',
        'Proficiency in design tools (Figma, Sketch, Adobe Creative Suite)',
        'Strong portfolio demonstrating design process and outcomes',
        'Experience with user research and testing methodologies',
        'Understanding of front-end development principles',
        'Excellent visual design and typography skills'
      ],
      salary: '$95,000 - $125,000',
      benefits: 'Full health benefits, creative workspace, design conference budget, flexible hours, remote work options'
    },
    {
      title: 'Data Scientist',
      department: 'Data Science',
      location: 'Boston, MA',
      type: JobType.FULL_TIME,
      description: `Join our Data Science team to help build and improve our AI models and analytics capabilities. You will work with large datasets to extract insights and build predictive models.

Key Responsibilities:
• Develop and deploy machine learning models
• Analyze large datasets to identify trends and patterns
• Collaborate with engineering teams to implement ML solutions
• Create data visualizations and reports
• Design and conduct A/B tests
• Stay current with latest ML/AI research and techniques`,
      requirements: [
        'Master\'s or PhD in Data Science, Statistics, or related field',
        '3+ years of experience in data science or machine learning',
        'Proficiency in Python, R, and SQL',
        'Experience with ML frameworks (TensorFlow, PyTorch, scikit-learn)',
        'Strong statistical analysis and modeling skills',
        'Experience with cloud platforms and big data tools',
        'Excellent communication skills for presenting findings'
      ],
      salary: '$130,000 - $170,000',
      benefits: 'Comprehensive benefits package, research budget, conference attendance, flexible work schedule'
    },
    {
      title: 'DevOps Engineer',
      department: 'Engineering',
      location: 'Austin, TX',
      type: JobType.FULL_TIME,
      description: `We are seeking a DevOps Engineer to help build and maintain our cloud infrastructure and deployment pipelines. You will work to ensure our systems are scalable, reliable, and secure.

Key Responsibilities:
• Design and maintain CI/CD pipelines
• Manage cloud infrastructure (AWS/Azure/GCP)
• Implement monitoring and alerting systems
• Automate deployment and scaling processes
• Ensure security best practices
• Collaborate with development teams on infrastructure needs`,
      requirements: [
        'Bachelor\'s degree in Computer Science or related field',
        '4+ years of DevOps or infrastructure experience',
        'Experience with containerization (Docker, Kubernetes)',
        'Proficiency in Infrastructure as Code (Terraform, CloudFormation)',
        'Strong scripting skills (Python, Bash, PowerShell)',
        'Experience with monitoring tools (Prometheus, Grafana, ELK stack)',
        'Knowledge of security best practices'
      ],
      salary: '$115,000 - $145,000',
      benefits: 'Health insurance, 401(k) matching, home office stipend, professional certifications budget'
    },
    {
      title: 'Marketing Intern',
      department: 'Marketing',
      location: 'Remote',
      type: JobType.INTERNSHIP,
      description: `Join our Marketing team as an intern and gain hands-on experience in digital marketing, content creation, and campaign management. This is a great opportunity for students or recent graduates.

Key Responsibilities:
• Assist with social media content creation and management
• Support email marketing campaigns
• Help with market research and competitive analysis
• Create marketing materials and presentations
• Assist with event planning and coordination
• Learn about marketing automation tools`,
      requirements: [
        'Currently pursuing or recently completed degree in Marketing, Communications, or related field',
        'Strong written and verbal communication skills',
        'Familiarity with social media platforms',
        'Basic knowledge of design tools (Canva, Adobe Creative Suite) preferred',
        'Analytical mindset and attention to detail',
        'Enthusiasm for learning and taking on new challenges',
        'Ability to work independently and as part of a team'
      ],
      salary: '$20 - $25 per hour',
      benefits: 'Flexible schedule, mentorship program, potential for full-time offer, remote work options'
    }
  ];

  console.log('Creating job postings...');
  
  for (const job of jobPostings) {
    const created = await prisma.jobPosting.create({
      data: job
    });
    console.log(`✅ Created job posting: ${created.title}`);
  }

  console.log('🎉 Database seed completed successfully!');
}

main()
  .catch((e) => {
    console.error('❌ Error during database seed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
