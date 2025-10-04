import { InvestorProvider } from '@/contexts/InvestorContext';
import InvestorLayout from '@/components/investor/Layout/InvestorLayout';

export default function InvestorLayoutPage({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <InvestorProvider>
      <InvestorLayout>
        {children}
      </InvestorLayout>
    </InvestorProvider>
  );
}
