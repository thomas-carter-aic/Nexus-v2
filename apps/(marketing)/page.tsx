import { Hero } from '@/components/Hero';
import { Services } from '@/components/Services';
import { Solutions } from '@/components/Solutions';
import { CTA } from '@/components/CTA';
import { Stats } from '@/components/Stats';

export default function HomePage() {
  return (
    <>
      <Hero />
      <Stats />
      <Services />
      <Solutions />
      <CTA />
    </>
  );
}
