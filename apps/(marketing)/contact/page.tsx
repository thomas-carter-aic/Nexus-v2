import type { Metadata } from 'next';
import { Mail, Phone, MapPin, Clock, MessageSquare, Calendar } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Contact Us - Applied Innovations Corporation',
  description: 'Get in touch with Applied Innovations Corporation for AI consulting, transformation services, and expert guidance on your AI journey.',
};

const contactMethods = [
  {
    name: 'Email',
    description: 'Send us an email and we\'ll respond within 24 hours',
    icon: Mail,
    contact: 'info@appliedinnovations.ai',
    href: 'mailto:info@appliedinnovations.ai',
  },
  {
    name: 'Phone',
    description: 'Call us during business hours for immediate assistance',
    icon: Phone,
    contact: '+1 (555) AI-TRANSFORM',
    href: 'tel:+1-555-248-7267',
  },
  {
    name: 'Office',
    description: 'Visit our headquarters in the heart of Tech Valley',
    icon: MapPin,
    contact: '123 Innovation Drive, Tech Valley, CA 94000',
    href: 'https://maps.google.com/?q=123+Innovation+Drive+Tech+Valley+CA',
  },
];

const offices = [
  {
    city: 'San Francisco',
    address: '123 Innovation Drive\nTech Valley, CA 94000',
    phone: '+1 (555) 248-7267',
    email: 'sf@appliedinnovations.ai',
  },
  {
    city: 'New York',
    address: '456 AI Boulevard\nManhattan, NY 10001',
    phone: '+1 (555) 692-4636',
    email: 'ny@appliedinnovations.ai',
  },
  {
    city: 'London',
    address: '789 Tech Square\nLondon, UK EC1A 1BB',
    phone: '+44 20 7946 0958',
    email: 'london@appliedinnovations.ai',
  },
];

export default function ContactPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="gradient-bg section-padding">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-6xl">
              Let's Transform Your Business Together
            </h1>
            <p className="mt-6 text-lg leading-8 text-secondary-600">
              Ready to start your AI transformation journey? Our experts are here to help. 
              Reach out to discuss your needs and discover how we can accelerate your success.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Methods */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {contactMethods.map((method) => (
              <a
                key={method.name}
                href={method.href}
                className="card-hover rounded-2xl border border-secondary-200 bg-white p-8 shadow-sm text-center group"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-2xl mb-6 group-hover:bg-primary-200 transition-colors">
                  <method.icon className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                  {method.name}
                </h3>
                <p className="text-secondary-600 mb-4">
                  {method.description}
                </p>
                <p className="text-primary-600 font-medium">
                  {method.contact}
                </p>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form */}
      <section className="section-padding gradient-bg">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
            <div>
              <h2 className="text-3xl font-bold text-secondary-900 mb-6">
                Send Us a Message
              </h2>
              <p className="text-lg text-secondary-600 mb-8">
                Fill out the form below and one of our AI experts will get back to you 
                within 24 hours to discuss your specific needs and how we can help.
              </p>
              
              <form className="space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-secondary-900 mb-2">
                      First Name *
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      required
                      className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      placeholder="John"
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-secondary-900 mb-2">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      required
                      className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      placeholder="Doe"
                    />
                  </div>
                </div>
                
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-secondary-900 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="john.doe@company.com"
                  />
                </div>
                
                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-secondary-900 mb-2">
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="Your Company"
                  />
                </div>
                
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-secondary-900 mb-2">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
                
                <div>
                  <label htmlFor="service" className="block text-sm font-medium text-secondary-900 mb-2">
                    Service Interest
                  </label>
                  <select
                    id="service"
                    name="service"
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                  >
                    <option value="">Select a service</option>
                    <option value="strategy">AI Strategy & Assessment</option>
                    <option value="implementation">AI Implementation</option>
                    <option value="governance">AI Governance & Compliance</option>
                    <option value="training">Team Training & Enablement</option>
                    <option value="innovation">AI Innovation Consulting</option>
                    <option value="optimization">Performance Optimization</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-secondary-900 mb-2">
                    Message *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={6}
                    required
                    className="w-full px-4 py-3 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="Tell us about your AI transformation goals and how we can help..."
                  />
                </div>
                
                <button
                  type="submit"
                  className="btn-primary w-full text-lg py-4"
                >
                  <MessageSquare className="w-5 h-5 mr-2" />
                  Send Message
                </button>
              </form>
            </div>
            
            <div>
              <div className="rounded-2xl border border-secondary-200 bg-white p-8 shadow-sm mb-8">
                <h3 className="text-xl font-semibold text-secondary-900 mb-6">
                  Prefer to Schedule a Call?
                </h3>
                <p className="text-secondary-600 mb-6">
                  Book a free 30-minute consultation with one of our AI experts to discuss 
                  your specific needs and explore how we can help transform your business.
                </p>
                <a
                  href="/consultation"
                  className="btn-primary w-full text-center"
                >
                  <Calendar className="w-5 h-5 mr-2" />
                  Schedule Free Consultation
                </a>
              </div>
              
              <div className="rounded-2xl border border-secondary-200 bg-white p-8 shadow-sm">
                <h3 className="text-xl font-semibold text-secondary-900 mb-6">
                  Business Hours
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center">
                    <Clock className="w-5 h-5 text-primary-600 mr-3" />
                    <div>
                      <div className="font-medium text-secondary-900">Monday - Friday</div>
                      <div className="text-secondary-600">9:00 AM - 6:00 PM PST</div>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <Clock className="w-5 h-5 text-primary-600 mr-3" />
                    <div>
                      <div className="font-medium text-secondary-900">Saturday</div>
                      <div className="text-secondary-600">10:00 AM - 2:00 PM PST</div>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <Clock className="w-5 h-5 text-secondary-600 mr-3" />
                    <div>
                      <div className="font-medium text-secondary-900">Sunday</div>
                      <div className="text-secondary-600">Closed</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Office Locations */}
      <section className="section-padding bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Our Offices</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              We have offices around the world to better serve our global client base.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {offices.map((office) => (
              <div key={office.city} className="text-center">
                <h3 className="text-xl font-semibold text-secondary-900 mb-4">
                  {office.city}
                </h3>
                <div className="space-y-3 text-secondary-600">
                  <div className="flex items-start justify-center">
                    <MapPin className="w-5 h-5 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                    <div className="whitespace-pre-line">{office.address}</div>
                  </div>
                  <div className="flex items-center justify-center">
                    <Phone className="w-5 h-5 text-primary-600 mr-2" />
                    <a href={`tel:${office.phone}`} className="hover:text-primary-600 transition-colors">
                      {office.phone}
                    </a>
                  </div>
                  <div className="flex items-center justify-center">
                    <Mail className="w-5 h-5 text-primary-600 mr-2" />
                    <a href={`mailto:${office.email}`} className="hover:text-primary-600 transition-colors">
                      {office.email}
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
