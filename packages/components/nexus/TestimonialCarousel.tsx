'use client';

import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Star, Quote } from 'lucide-react';

interface Testimonial {
  id: string;
  name: string;
  title: string;
  company: string;
  content: string;
  rating: number;
  image: string;
  metrics: {
    label: string;
    value: string;
  }[];
}

const testimonials: Testimonial[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    title: 'CTO',
    company: 'TechFlow Solutions',
    content: 'Nexus transformed our AI development process. What used to take our team 8 months now takes just 6 weeks. The pre-built components and automated workflows are game-changers.',
    rating: 5,
    image: '/api/placeholder/80/80',
    metrics: [
      { label: 'Time Saved', value: '75%' },
      { label: 'Cost Reduction', value: '$2.3M' },
      { label: 'Deployment Speed', value: '10x faster' }
    ]
  },
  {
    id: '2',
    name: 'Michael Rodriguez',
    title: 'Head of Innovation',
    company: 'Global Finance Corp',
    content: 'The security and compliance features in Nexus gave us confidence to deploy AI in our regulated environment. The ROI has been exceptional - we\'ve seen 300% improvement in processing efficiency.',
    rating: 5,
    image: '/api/placeholder/80/80',
    metrics: [
      { label: 'Processing Efficiency', value: '300%' },
      { label: 'Compliance Score', value: '100%' },
      { label: 'Error Reduction', value: '95%' }
    ]
  },
  {
    id: '3',
    name: 'Emily Watson',
    title: 'VP of Product',
    company: 'HealthTech Innovations',
    content: 'Nexus enabled us to launch three AI-powered features in the time it would have taken to build one from scratch. The platform\'s flexibility and scalability are unmatched.',
    rating: 5,
    image: '/api/placeholder/80/80',
    metrics: [
      { label: 'Features Launched', value: '3x more' },
      { label: 'User Engagement', value: '+180%' },
      { label: 'Revenue Growth', value: '+250%' }
    ]
  },
  {
    id: '4',
    name: 'David Kim',
    title: 'Chief Data Officer',
    company: 'RetailMax',
    content: 'The analytics and monitoring capabilities in Nexus give us unprecedented visibility into our AI systems. We can optimize performance in real-time and ensure consistent quality.',
    rating: 5,
    image: '/api/placeholder/80/80',
    metrics: [
      { label: 'System Uptime', value: '99.9%' },
      { label: 'Performance Gain', value: '40%' },
      { label: 'Monitoring Coverage', value: '100%' }
    ]
  },
  {
    id: '5',
    name: 'Lisa Thompson',
    title: 'Director of Engineering',
    company: 'CloudScale Systems',
    content: 'The developer experience with Nexus is outstanding. Our team was productive from day one, and the learning curve was minimal. It\'s like having an AI expert on every project.',
    rating: 5,
    image: '/api/placeholder/80/80',
    metrics: [
      { label: 'Developer Productivity', value: '+400%' },
      { label: 'Learning Time', value: '2 days' },
      { label: 'Code Quality', value: '+60%' }
    ]
  }
];

export function TestimonialCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);

  useEffect(() => {
    if (!isAutoPlaying) return;

    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => 
        prevIndex === testimonials.length - 1 ? 0 : prevIndex + 1
      );
    }, 5000);

    return () => clearInterval(interval);
  }, [isAutoPlaying]);

  const goToPrevious = () => {
    setIsAutoPlaying(false);
    setCurrentIndex(currentIndex === 0 ? testimonials.length - 1 : currentIndex - 1);
  };

  const goToNext = () => {
    setIsAutoPlaying(false);
    setCurrentIndex(currentIndex === testimonials.length - 1 ? 0 : currentIndex + 1);
  };

  const goToSlide = (index: number) => {
    setIsAutoPlaying(false);
    setCurrentIndex(index);
  };

  const currentTestimonial = testimonials[currentIndex];

  return (
    <section className="py-24 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Trusted by Industry Leaders
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            See how companies are transforming their AI initiatives with Nexus
          </p>
        </div>

        <div className="relative">
          {/* Main Testimonial Card */}
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div className="grid lg:grid-cols-2">
              {/* Content Side */}
              <div className="p-8 lg:p-12">
                <div className="flex items-center gap-1 mb-6">
                  {[...Array(currentTestimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>

                <div className="relative mb-8">
                  <Quote className="absolute -top-2 -left-2 w-8 h-8 text-blue-200" />
                  <blockquote className="text-lg lg:text-xl text-gray-700 leading-relaxed pl-6">
                    "{currentTestimonial.content}"
                  </blockquote>
                </div>

                <div className="flex items-center gap-4 mb-8">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                    {currentTestimonial.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <div className="font-bold text-gray-900 text-lg">
                      {currentTestimonial.name}
                    </div>
                    <div className="text-gray-600">
                      {currentTestimonial.title}
                    </div>
                    <div className="text-blue-600 font-medium">
                      {currentTestimonial.company}
                    </div>
                  </div>
                </div>

                {/* Navigation Controls */}
                <div className="flex items-center justify-between">
                  <div className="flex gap-2">
                    {testimonials.map((_, index) => (
                      <button
                        key={index}
                        onClick={() => goToSlide(index)}
                        className={`w-3 h-3 rounded-full transition-all duration-300 ${
                          index === currentIndex
                            ? 'bg-blue-600 w-8'
                            : 'bg-gray-300 hover:bg-gray-400'
                        }`}
                      />
                    ))}
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={goToPrevious}
                      className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors duration-200"
                    >
                      <ChevronLeft className="w-5 h-5 text-gray-600" />
                    </button>
                    <button
                      onClick={goToNext}
                      className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors duration-200"
                    >
                      <ChevronRight className="w-5 h-5 text-gray-600" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Metrics Side */}
              <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-8 lg:p-12 text-white">
                <h3 className="text-2xl font-bold mb-8">Key Results</h3>
                
                <div className="space-y-6">
                  {currentTestimonial.metrics.map((metric, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="text-blue-100">{metric.label}</div>
                      <div className="text-2xl font-bold">{metric.value}</div>
                    </div>
                  ))}
                </div>

                <div className="mt-12 pt-8 border-t border-blue-400">
                  <div className="text-center">
                    <div className="text-3xl font-bold mb-2">
                      {testimonials.length}
                    </div>
                    <div className="text-blue-100">
                      Success Stories
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Thumbnail Navigation */}
          <div className="mt-8 flex justify-center gap-4 overflow-x-auto pb-4">
            {testimonials.map((testimonial, index) => (
              <button
                key={testimonial.id}
                onClick={() => goToSlide(index)}
                className={`flex-shrink-0 p-4 rounded-xl transition-all duration-300 ${
                  index === currentIndex
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-white text-gray-600 hover:bg-gray-50 shadow'
                }`}
              >
                <div className="text-center">
                  <div className="font-semibold text-sm mb-1">
                    {testimonial.name}
                  </div>
                  <div className="text-xs opacity-75">
                    {testimonial.company}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 text-center">
          <div className="bg-white rounded-2xl shadow-xl p-8 max-w-4xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Join These Success Stories
            </h3>
            <p className="text-gray-600 mb-6">
              Ready to transform your AI development process? Start your journey with Nexus today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200">
                Start Free Trial
              </button>
              <button className="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors duration-200">
                View Case Studies
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
