import { Navigate, Outlet } from 'react-router-dom';
import { useAdminAuthStore, useAuthStore } from '@/store/authStore';

export function ProtectedRoute() {
  const { isAuthenticated } = useAuthStore();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <Outlet />;
}

export function AdminProtectedRoute() {
  const { isAuthenticated } = useAdminAuthStore();
  if (!isAuthenticated) return <Navigate to="/admin/login" replace />;
  return <Outlet />;
}

export function GuestRoute() {
  const { isAuthenticated } = useAuthStore();
  if (isAuthenticated) return <Navigate to="/dashboard" replace />;
  return <Outlet />;
}
