import type { Metadata } from 'next';
import { Users, CheckCircle, BookOpen, Award, Target, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Team Training & Enablement - Applied Innovations Corporation',
  description: 'Comprehensive training programs to upskill your workforce for AI-driven business transformation and success.',
};

export default function TeamTrainingPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-orange-600 rounded-2xl mb-6">
              <Users className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Team Training & Enablement
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Comprehensive training programs to upskill your workforce for AI-driven business 
              transformation, ensuring your team can effectively leverage AI technologies.
            </p>
            <div className="mt-10">
              <a href="/consultation" className="btn-primary text-lg px-8 py-4">
                Start Training Program
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Service Overview */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-secondary-900 mb-6">
                Empower Your Team
              </h2>
              <p className="text-lg text-secondary-600 mb-6">
                Success with AI requires more than just technology—it requires people who 
                understand how to use it effectively. Our training programs ensure your 
                team has the skills and knowledge to drive AI success.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  'Executive workshops and leadership training',
                  'Technical training for IT and data teams',
                  'Change management and adoption support',
                  'Ongoing support and skill development',
                ].map((item, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-orange-500 mr-3 flex-shrink-0" />
                    <span className="text-secondary-700">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-2xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600 mb-2">95%</div>
                  <div className="text-sm text-secondary-600">Completion Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600 mb-2">5,000+</div>
                  <div className="text-sm text-secondary-600">Professionals Trained</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600 mb-2">4.8/5</div>
                  <div className="text-sm text-secondary-600">Training Rating</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600 mb-2">85%</div>
                  <div className="text-sm text-secondary-600">Skill Improvement</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Training Programs */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Training Programs</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Tailored training for every role and skill level
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Executive Leadership',
                description: 'AI strategy and decision-making for executives',
                icon: Target,
                color: 'bg-purple-100 text-purple-600',
              },
              {
                title: 'Technical Training',
                description: 'Hands-on AI development and implementation',
                icon: BookOpen,
                color: 'bg-blue-100 text-blue-600',
              },
              {
                title: 'Business Users',
                description: 'AI tools and applications for daily work',
                icon: Users,
                color: 'bg-green-100 text-green-600',
              },
              {
                title: 'Certification',
                description: 'Industry-recognized AI certifications',
                icon: Award,
                color: 'bg-orange-100 text-orange-600',
              },
            ].map((program, index) => (
              <div key={index} className="bg-white rounded-lg p-6 text-center shadow-sm">
                <div className={`inline-flex items-center justify-center w-12 h-12 ${program.color} rounded-xl mb-4`}>
                  <program.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                  {program.title}
                </h3>
                <p className="text-secondary-600">
                  {program.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-secondary-900">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Invest in Your Team's Future
          </h2>
          <p className="text-lg text-secondary-300 mb-8 max-w-2xl mx-auto">
            Equip your workforce with the AI skills they need to drive innovation 
            and success in your organization.
          </p>
          <a href="/consultation" className="btn-primary text-lg px-8 py-4">
            Design Training Program
            <ArrowRight className="w-5 h-5 ml-2" />
          </a>
        </div>
      </section>
    </div>
  );
}
