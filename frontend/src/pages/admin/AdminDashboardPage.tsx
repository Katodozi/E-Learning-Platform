import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { BarChart3, BookOpen, Layers, Users } from 'lucide-react';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { adminApi } from '@/services/api';

export function AdminDashboardPage() {
  const { data: analytics } = useQuery({
    queryKey: ['admin-analytics'],
    queryFn: () => adminApi.analytics().then((r) => r.data),
  });

  const stats = [
    { icon: Users, label: 'Total Users', value: analytics?.total_users || 0 },
    { icon: Layers, label: 'Expertise', value: analytics?.total_expertise || 0 },
    { icon: BookOpen, label: 'Skills', value: analytics?.total_skills || 0 },
    { icon: BarChart3, label: 'Avg Quiz Score', value: `${analytics?.average_quiz_score || 0}%` },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <p className="text-text-secondary">Platform overview and management</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map(({ icon: Icon, label, value }) => (
          <Card key={label}>
            <div className="flex items-center gap-3">
              <Icon className="h-8 w-8 text-secondary" />
              <div>
                <p className="text-sm text-text-secondary">{label}</p>
                <p className="text-2xl font-bold">{value}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid sm:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <div className="space-y-2">
            <Link to="/admin/expertise"><Button variant="outline" className="w-full justify-start">Manage Expertise</Button></Link>
            <Link to="/admin/roadmaps"><Button variant="outline" className="w-full justify-start">Manage Roadmaps</Button></Link>
            <Link to="/admin/prompts"><Button variant="outline" className="w-full justify-start">Manage Prompts</Button></Link>
            <Link to="/admin/users"><Button variant="outline" className="w-full justify-start">View Users</Button></Link>
          </div>
        </Card>

        <Card className="sm:col-span-2">
          <CardHeader>
            <CardTitle>Platform Stats</CardTitle>
            <CardDescription>Additional metrics</CardDescription>
          </CardHeader>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div><span className="text-text-secondary">Roadmaps:</span> {analytics?.total_roadmaps}</div>
            <div><span className="text-text-secondary">Quiz Attempts:</span> {analytics?.total_quiz_attempts}</div>
            <div><span className="text-text-secondary">Active (7d):</span> {analytics?.active_users_last_7_days}</div>
          </div>
        </Card>
      </div>
    </div>
  );
}
