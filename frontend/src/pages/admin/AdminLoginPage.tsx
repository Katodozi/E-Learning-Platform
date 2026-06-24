import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { useAdminAuthStore } from '@/store/authStore';

export function AdminLoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAdminAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await login(email, password);
      navigate('/admin');
    } catch {
      setError('Invalid admin credentials');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-center gap-2 mb-2">
            <Shield className="h-5 w-5 text-secondary" />
            <CardTitle>Admin Login</CardTitle>
          </div>
          <CardDescription>SkillForge AI Administration Panel</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input type="email" placeholder="admin@skillforge.ai" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          {error && <p className="text-sm text-red-400">{error}</p>}
          <Button type="submit" variant="secondary" className="w-full">Sign In</Button>
        </form>
      </Card>
    </div>
  );
}
