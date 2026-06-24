import { Link, Outlet } from 'react-router-dom';
import { Shield, Zap } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useAdminAuthStore } from '@/store/authStore';

export function AdminLayout() {
  const { admin, logout } = useAdminAuthStore();

  return (
    <div className="min-h-screen">
      <header className="glass border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/admin" className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-secondary" />
            <span className="font-bold">SkillForge Admin</span>
          </Link>
          <nav className="hidden md:flex items-center gap-4 text-sm">
            <Link to="/admin" className="text-text-secondary hover:text-text-primary">Dashboard</Link>
            <Link to="/admin/expertise" className="text-text-secondary hover:text-text-primary">Expertise</Link>
            <Link to="/admin/roadmaps" className="text-text-secondary hover:text-text-primary">Roadmaps</Link>
            <Link to="/admin/prompts" className="text-text-secondary hover:text-text-primary">Prompts</Link>
            <Link to="/admin/users" className="text-text-secondary hover:text-text-primary">Users</Link>
          </nav>
          <div className="flex items-center gap-3">
            <span className="text-sm text-text-secondary hidden sm:block">{admin?.email}</span>
            <Button variant="outline" size="sm" onClick={logout}>Logout</Button>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto p-4 md:p-6">
        <Outlet />
      </main>
      <footer className="text-center py-4 text-xs text-text-secondary">
        <Link to="/" className="inline-flex items-center gap-1 hover:text-primary">
          <Zap className="h-3 w-3" /> Back to SkillForge AI
        </Link>
      </footer>
    </div>
  );
}
