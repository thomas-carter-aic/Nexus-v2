import type { Metadata } from 'next';
import { Brain, Users, Target, Award, Lightbulb, Shield } from 'lucide-react';

export const metadata: Metadata = {
  title: 'About Us - Applied Innovations Corporation',
  description: 'Learn about Applied Innovations Corporation, our mission to democratize AI, and our team of experts helping businesses transform with artificial intelligence.',
};

const values = [
  {
    name: 'Innovation First',
    description: 'We stay at the forefront of AI technology, continuously exploring new possibilities and solutions.',
    icon: Lightbulb,
  },
  {
    name: 'Client Success',
    description: 'Your success is our success. We measure our impact by the transformation we enable.',
    icon: Target,
  },
  {
    name: 'Ethical AI',
    description: 'We champion responsible AI development with transparency, fairness, and accountability.',
    icon: Shield,
  },
  {
    name: 'Excellence',
    description: 'We deliver exceptional quality in every project, consultation, and client interaction.',
    icon: Award,
  },
];

const team = [
  {
    name: 'Dr. Sarah Chen',
    role: 'Chief Executive Officer',
    bio: 'Former AI Research Director at Google, PhD in Machine Learning from Stanford. 15+ years leading AI initiatives.',
    image: '/team/sarah-chen.jpg',
  },
  {
    name: 'Michael Rodriguez',
    role: 'Chief Technology Officer',
    bio: 'Ex-Microsoft Principal Engineer, architect of the Nexus platform. Expert in scalable AI systems.',
    image: '/team/michael-rodriguez.jpg',
  },
  {
    name: 'Dr. Priya Patel',
    role: 'Head of AI Strategy',
    bio: 'Former McKinsey Partner specializing in AI transformation. PhD in Computer Science from MIT.',
    image: '/team/priya-patel.jpg',
  },
  {
    name: 'James Thompson',
    role: 'VP of Client Success',
    bio: '20+ years in enterprise consulting. Led digital transformations for Fortune 500 companies.',
    image: '/team/james-thompson.jpg',
  },
];

export default function AboutPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Pioneering AI Transformation
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Applied Innovations Corporation was founded with a simple yet ambitious mission: 
              to democratize artificial intelligence and make its transformative power accessible 
              to businesses of all sizes.
            </p>
          </div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-secondary-900 mb-6">Our Mission</h2>
              <p className="text-lg text-secondary-600 mb-6">
                We empower businesses to harness the full potential of artificial intelligence 
                through strategic consulting, safe implementation, and comprehensive enablement services.
              </p>
              <p className="text-secondary-600">
                Our approach combines deep technical expertise with business acumen, ensuring 
                that AI initiatives deliver measurable value while maintaining the highest 
                standards of security, compliance, and ethical responsibility.
              </p>
            </div>
            <div className="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-2xl p-8">
              <div className="flex items-center mb-6">
                <Brain className="w-8 h-8 text-primary-600 mr-3" />
                <h3 className="text-xl font-semibold text-secondary-900">Our Vision</h3>
              </div>
              <p className="text-secondary-700">
                To be the world's most trusted AI transformation partner, enabling every 
                organization to thrive in the age of artificial intelligence through 
                innovation, expertise, and unwavering commitment to client success.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Our Core Values</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              These principles guide every decision we make and every solution we deliver.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value) => (
              <div key={value.name} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-2xl mb-6">
                  <value.icon className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                  {value.name}
                </h3>
                <p className="text-secondary-600">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Leadership Team */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Leadership Team</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Meet the experts leading Applied Innovations Corporation's mission to transform 
              businesses through artificial intelligence.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member) => (
              <div key={member.name} className="text-center">
                <div className="w-32 h-32 bg-secondary-200 rounded-full mx-auto mb-6 flex items-center justify-center">
                  <Users className="w-16 h-16 text-secondary-400" />
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-1">
                  {member.name}
                </h3>
                <p className="text-primary-600 font-medium mb-3">
                  {member.role}
                </p>
                <p className="text-sm text-secondary-600">
                  {member.bio}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Company Stats */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Our Impact</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Numbers that reflect our commitment to client success and AI excellence.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">500+</div>
              <div className="text-secondary-600">Clients Served</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">1,200+</div>
              <div className="text-secondary-600">AI Projects Delivered</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">25+</div>
              <div className="text-secondary-600">Industries Transformed</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">340%</div>
              <div className="text-secondary-600">Average ROI Increase</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Join the hundreds of businesses that have successfully implemented AI with our guidance.
          </p>
          <a
            href="/consultation"
            className="btn-primary text-lg px-8 py-4"
          >
            Schedule Your Free Consultation
          </a>
        </div>
      </section>
    </div>
  );
}
