import type { Metadata } from 'next';
import { MapPin, Clock, DollarSign, Users, Heart, Zap, Award, Coffee } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Careers - Applied Innovations Corporation',
  description: 'Join our team of AI experts and help shape the future of artificial intelligence. Explore career opportunities at Applied Innovations Corporation.',
};

const openPositions = [
  {
    id: 1,
    title: 'Senior AI Engineer',
    department: 'Engineering',
    location: 'San Francisco, CA / Remote',
    type: 'Full-time',
    salary: '$150,000 - $200,000',
    description: 'Lead the development of cutting-edge AI solutions and work with our platform engineering team to build scalable AI systems.',
    requirements: [
      '5+ years of experience in AI/ML development',
      'Expertise in Python, TensorFlow, PyTorch',
      'Experience with cloud platforms (AWS, Azure, GCP)',
      'Strong understanding of MLOps practices',
    ],
    posted: '2024-07-01',
  },
  {
    id: 2,
    title: 'AI Solutions Architect',
    department: 'Solutions',
    location: 'New York, NY / Remote',
    type: 'Full-time',
    salary: '$140,000 - $180,000',
    description: 'Design and architect AI solutions for enterprise clients, working closely with our consulting team to deliver transformative results.',
    requirements: [
      '7+ years of enterprise software architecture experience',
      'Deep knowledge of AI/ML technologies and frameworks',
      'Experience with enterprise integration patterns',
      'Strong client-facing and communication skills',
    ],
    posted: '2024-06-28',
  },
  {
    id: 3,
    title: 'Data Scientist',
    department: 'Data Science',
    location: 'Austin, TX / Remote',
    type: 'Full-time',
    salary: '$120,000 - $160,000',
    description: 'Analyze complex datasets, build predictive models, and derive actionable insights to drive business value for our clients.',
    requirements: [
      '3+ years of data science experience',
      'Proficiency in Python, R, SQL',
      'Experience with statistical modeling and machine learning',
      'Strong analytical and problem-solving skills',
    ],
    posted: '2024-06-25',
  },
  {
    id: 4,
    title: 'AI Product Manager',
    department: 'Product',
    location: 'San Francisco, CA',
    type: 'Full-time',
    salary: '$130,000 - $170,000',
    description: 'Drive product strategy and roadmap for our AI platform, working with engineering and design teams to deliver exceptional user experiences.',
    requirements: [
      '5+ years of product management experience',
      'Background in AI/ML or enterprise software',
      'Experience with agile development methodologies',
      'Strong analytical and strategic thinking skills',
    ],
    posted: '2024-06-20',
  },
  {
    id: 5,
    title: 'DevOps Engineer',
    department: 'Engineering',
    location: 'Remote',
    type: 'Full-time',
    salary: '$110,000 - $150,000',
    description: 'Build and maintain our cloud infrastructure, CI/CD pipelines, and deployment systems to support our growing AI platform.',
    requirements: [
      '4+ years of DevOps/SRE experience',
      'Expertise in Kubernetes, Docker, Terraform',
      'Experience with cloud platforms and monitoring tools',
      'Strong automation and scripting skills',
    ],
    posted: '2024-06-15',
  },
  {
    id: 6,
    title: 'AI Ethics Researcher',
    department: 'Research',
    location: 'Boston, MA / Remote',
    type: 'Full-time',
    salary: '$100,000 - $140,000',
    description: 'Research and develop ethical AI frameworks, ensuring our solutions are responsible, fair, and transparent.',
    requirements: [
      'PhD in AI Ethics, Philosophy, or related field',
      'Experience in AI bias detection and mitigation',
      'Strong research and writing skills',
      'Knowledge of AI governance frameworks',
    ],
    posted: '2024-06-10',
  },
];

const benefits = [
  {
    icon: Heart,
    title: 'Health & Wellness',
    description: 'Comprehensive health, dental, and vision insurance plus wellness programs',
  },
  {
    icon: DollarSign,
    title: 'Competitive Compensation',
    description: 'Market-leading salaries, equity participation, and performance bonuses',
  },
  {
    icon: Clock,
    title: 'Flexible Work',
    description: 'Remote-first culture with flexible hours and unlimited PTO',
  },
  {
    icon: Zap,
    title: 'Learning & Development',
    description: '$5,000 annual learning budget and conference attendance support',
  },
  {
    icon: Coffee,
    title: 'Great Perks',
    description: 'Free meals, gym membership, and top-tier equipment',
  },
  {
    icon: Award,
    title: 'Recognition',
    description: 'Regular recognition programs and career advancement opportunities',
  },
];

const values = [
  {
    title: 'Innovation First',
    description: 'We push the boundaries of what\'s possible with AI, always seeking new and better solutions.',
  },
  {
    title: 'Ethical AI',
    description: 'We believe in responsible AI development that benefits society and respects human values.',
  },
  {
    title: 'Collaboration',
    description: 'We work together as a team, sharing knowledge and supporting each other\'s growth.',
  },
  {
    title: 'Excellence',
    description: 'We strive for excellence in everything we do, from code quality to client service.',
  },
  {
    title: 'Diversity & Inclusion',
    description: 'We celebrate diverse perspectives and create an inclusive environment for all.',
  },
  {
    title: 'Continuous Learning',
    description: 'We embrace lifelong learning and encourage experimentation and growth.',
  },
];

export default function CareersPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Shape the Future of AI
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Join our team of world-class AI experts and help businesses transform through 
              artificial intelligence. Build your career while making a meaningful impact.
            </p>
            <div className="mt-10">
              <a href="#open-positions" className="btn-primary text-lg px-8 py-4">
                View Open Positions
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Why Work With Us */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Why Applied Innovations?</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              We're building the future of AI, and we want you to be part of it
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-2xl mb-6">
                  <benefit.icon className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                  {benefit.title}
                </h3>
                <p className="text-secondary-600">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Our Values */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Our Values</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              The principles that guide everything we do
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {values.map((value, index) => (
              <div key={index} className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {value.title}
                </h3>
                <p className="text-secondary-600">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Open Positions */}
      <section id="open-positions" className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Open Positions</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Join our growing team and help shape the future of AI
            </p>
          </div>

          <div className="space-y-6">
            {openPositions.map((position) => (
              <div key={position.id} className="bg-white border border-secondary-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-xl font-semibold text-secondary-900">
                        {position.title}
                      </h3>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        {position.department}
                      </span>
                    </div>
                    
                    <div className="flex flex-wrap items-center gap-4 text-sm text-secondary-600 mb-4">
                      <div className="flex items-center">
                        <MapPin className="w-4 h-4 mr-1" />
                        {position.location}
                      </div>
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        {position.type}
                      </div>
                      <div className="flex items-center">
                        <DollarSign className="w-4 h-4 mr-1" />
                        {position.salary}
                      </div>
                    </div>

                    <p className="text-secondary-700 mb-4">
                      {position.description}
                    </p>

                    <div className="mb-4">
                      <h4 className="text-sm font-semibold text-secondary-900 mb-2">Key Requirements:</h4>
                      <ul className="space-y-1">
                        {position.requirements.slice(0, 2).map((req, index) => (
                          <li key={index} className="flex items-start text-sm text-secondary-700">
                            <div className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-2 mr-2 flex-shrink-0"></div>
                            {req}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <p className="text-xs text-secondary-500">
                      Posted: {new Date(position.posted).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </p>
                  </div>

                  <div className="mt-4 lg:mt-0 lg:ml-6 flex-shrink-0">
                    <button className="btn-primary w-full lg:w-auto">
                      Apply Now
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <p className="text-secondary-600 mb-4">
              Don't see a position that fits? We're always looking for exceptional talent.
            </p>
            <button className="btn-secondary">
              Send Us Your Resume
            </button>
          </div>
        </div>
      </section>

      {/* Team Stats */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Our Growing Team</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Join a diverse, talented team that's passionate about AI
            </p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">85+</div>
              <div className="text-secondary-600">Team Members</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">15+</div>
              <div className="text-secondary-600">Countries</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">45%</div>
              <div className="text-secondary-600">Women in Tech</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">4.9/5</div>
              <div className="text-secondary-600">Employee Satisfaction</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Join Our Mission?
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Help us build the future of AI while advancing your career with a team that values innovation, ethics, and excellence.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="#open-positions" className="btn-primary text-lg px-8 py-4">
              Browse Open Positions
            </a>
            <a href="/contact" className="btn-secondary text-lg px-8 py-4 bg-transparent border-white text-white hover:bg-white hover:text-secondary-900">
              Get in Touch
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
