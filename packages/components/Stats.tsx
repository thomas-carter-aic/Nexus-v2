'use client';

import { motion } from 'framer-motion';

const stats = [
  { id: 1, name: 'Enterprise Clients Served', value: '500+' },
  { id: 2, name: 'AI Projects Delivered', value: '1,200+' },
  { id: 3, name: 'Average ROI Increase', value: '340%' },
  { id: 4, name: 'Industries Transformed', value: '25+' },
];

export function Stats() {
  return (
    <section className="bg-white py-16">
      <div className="container">
        <div className="mx-auto max-w-7xl">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <dt className="text-base leading-7 text-secondary-600">{stat.name}</dt>
                <dd className="order-first text-3xl font-bold tracking-tight text-secondary-900 sm:text-5xl">
                  {stat.value}
                </dd>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
