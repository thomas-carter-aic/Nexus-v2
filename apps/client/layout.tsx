import { ClientProvider } from '@/contexts/ClientContext';
import ClientLayout from '@/components/client/Layout/ClientLayout';

export default function ClientLayoutPage({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClientProvider>
      <ClientLayout>
        {children}
      </ClientLayout>
    </ClientProvider>
  );
}
