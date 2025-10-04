'use client';

import Link from 'next/link';
import { Brain, Mail, Phone, MapPin, Linkedin, Twitter, Github } from 'lucide-react';

const navigation = {
  services: [
    { name: 'AI Strategy & Assessment', href: '/services/strategy' },
    { name: 'AI Implementation', href: '/services/implementation' },
    { name: 'AI Governance & Compliance', href: '/services/governance' },
    { name: 'Team Training & Enablement', href: '/services/training' },
    { name: 'AI Innovation Consulting', href: '/services/innovation' },
    { name: 'Performance Optimization', href: '/services/optimization' },
  ],
  solutions: [
    { name: 'Small & Medium Business', href: '/solutions/smb' },
    { name: 'Enterprise Organizations', href: '/solutions/enterprise' },
    { name: 'Healthcare', href: '/solutions/healthcare' },
    { name: 'Financial Services', href: '/solutions/financial' },
    { name: 'Manufacturing', href: '/solutions/manufacturing' },
    { name: 'Retail & E-commerce', href: '/solutions/retail' },
  ],
  company: [
    { name: 'About Us', href: '/about' },
    { name: 'Case Studies', href: '/case-studies' },
    { name: 'Careers', href: '/careers' },
    { name: 'News & Insights', href: '/blog' },
    { name: 'Partners', href: '/partners' },
    { name: 'Contact', href: '/contact' },
  ],
  resources: [
    { name: 'Documentation', href: '/docs' },
    { name: 'Nexus Platform', href: '/nexus' },
    { name: 'AI Readiness Assessment', href: '/assessment' },
    { name: 'Whitepapers', href: '/resources/whitepapers' },
    { name: 'Webinars', href: '/resources/webinars' },
    { name: 'Support', href: '/support' },
  ],
  legal: [
    { name: 'Privacy Policy', href: '/privacy' },
    { name: 'Terms of Service', href: '/terms' },
    { name: 'Cookie Policy', href: '/cookies' },
    { name: 'Security', href: '/security' },
  ],
};

const social = [
  {
    name: 'LinkedIn',
    href: 'https://linkedin.com/company/applied-innovations-corp',
    icon: Linkedin,
  },
  {
    name: 'Twitter',
    href: 'https://twitter.com/AppliedInnovCorp',
    icon: Twitter,
  },
  {
    name: 'GitHub',
    href: 'https://github.com/applied-innovations',
    icon: Github,
  },
];

export function Footer() {
  return (
    <footer className="bg-secondary-900" aria-labelledby="footer-heading">
      <h2 id="footer-heading" className="sr-only">
        Footer
      </h2>
      <div className="container py-16">
        <div className="xl:grid xl:grid-cols-3 xl:gap-8">
          <div className="space-y-8">
            <Link href="/" className="flex items-center space-x-2">
              <div className="flex items-center justify-center w-8 h-8 bg-primary-600 rounded-lg">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Applied Innovations</span>
            </Link>
            <p className="text-sm leading-6 text-secondary-300 max-w-md">
              Empowering businesses with strategic AI consulting, transformation services, 
              and cutting-edge technology solutions. Your trusted partner in AI excellence.
            </p>
            <div className="space-y-2">
              <div className="flex items-center text-sm text-secondary-300">
                <Mail className="w-4 h-4 mr-2 flex-shrink-0" />
                <a href="mailto:info@appliedinnovations.ai" className="hover:text-white transition-colors">
                  info@appliedinnovations.ai
                </a>
              </div>
              <div className="flex items-center text-sm text-secondary-300">
                <Phone className="w-4 h-4 mr-2 flex-shrink-0" />
                <a href="tel:+1-555-AI-TRANSFORM" className="hover:text-white transition-colors">
                  +1 (555) AI-TRANSFORM
                </a>
              </div>
              <div className="flex items-start text-sm text-secondary-300">
                <MapPin className="w-4 h-4 mr-2 flex-shrink-0 mt-0.5" />
                <span>
                  123 Innovation Drive<br />
                  Tech Valley, CA 94000
                </span>
              </div>
            </div>
            <div className="flex space-x-6">
              {social.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-secondary-400 hover:text-white transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span className="sr-only">{item.name}</span>
                  <item.icon className="h-6 w-6" aria-hidden="true" />
                </a>
              ))}
            </div>
          </div>
          <div className="mt-16 grid grid-cols-2 gap-8 xl:col-span-2 xl:mt-0">
            <div className="md:grid md:grid-cols-2 md:gap-8">
              <div>
                <h3 className="text-sm font-semibold leading-6 text-white">Services</h3>
                <ul role="list" className="mt-6 space-y-4">
                  {navigation.services.map((item) => (
                    <li key={item.name}>
                      <Link
                        href={item.href}
                        className="text-sm leading-6 text-secondary-300 hover:text-white transition-colors"
                      >
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="mt-10 md:mt-0">
                <h3 className="text-sm font-semibold leading-6 text-white">Solutions</h3>
                <ul role="list" className="mt-6 space-y-4">
                  {navigation.solutions.map((item) => (
                    <li key={item.name}>
                      <Link
                        href={item.href}
                        className="text-sm leading-6 text-secondary-300 hover:text-white transition-colors"
                      >
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="md:grid md:grid-cols-2 md:gap-8">
              <div>
                <h3 className="text-sm font-semibold leading-6 text-white">Company</h3>
                <ul role="list" className="mt-6 space-y-4">
                  {navigation.company.map((item) => (
                    <li key={item.name}>
                      <Link
                        href={item.href}
                        className="text-sm leading-6 text-secondary-300 hover:text-white transition-colors"
                      >
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="mt-10 md:mt-0">
                <h3 className="text-sm font-semibold leading-6 text-white">Resources</h3>
                <ul role="list" className="mt-6 space-y-4">
                  {navigation.resources.map((item) => (
                    <li key={item.name}>
                      <Link
                        href={item.href}
                        className="text-sm leading-6 text-secondary-300 hover:text-white transition-colors"
                      >
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div className="mt-16 border-t border-secondary-700 pt-8 sm:mt-20 lg:mt-24">
          <div className="md:flex md:items-center md:justify-between">
            <div className="flex space-x-6 md:order-2">
              {navigation.legal.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-sm leading-6 text-secondary-400 hover:text-secondary-300 transition-colors"
                >
                  {item.name}
                </Link>
              ))}
            </div>
            <p className="mt-8 text-xs leading-5 text-secondary-400 md:order-1 md:mt-0">
              &copy; 2024 Applied Innovations Corporation. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
