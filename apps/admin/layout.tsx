import { AdminProvider } from '@/contexts/AdminContext';
import AdminLayout from '@/components/admin/Layout/AdminLayout';

export default function AdminLayoutPage({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AdminProvider>
      <AdminLayout>
        {children}
      </AdminLayout>
    </AdminProvider>
  );
}
