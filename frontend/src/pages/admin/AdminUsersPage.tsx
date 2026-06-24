import { useQuery } from '@tanstack/react-query';
import { Users } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { ProgressRing } from '@/components/ui/ProgressRing';
import { adminApi } from '@/services/api';

export function AdminUsersPage() {
  const { data: users, isLoading } = useQuery({
    queryKey: ['admin-users'],
    queryFn: () => adminApi.listUsers().then((r) => r.data),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Users className="h-6 w-6 text-secondary" />
          User Progress
        </h1>
        <p className="text-text-secondary">View registered users and their learning progress</p>
      </div>

      {isLoading ? (
        <div className="glass rounded-xl h-48 animate-pulse" />
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          {users?.map((user) => (
            <Card key={user.id}>
              <CardHeader>
                <CardTitle className="text-base truncate">{user.email}</CardTitle>
                <CardDescription>
                  {user.selected_expertise || 'No expertise selected'}
                </CardDescription>
              </CardHeader>
              <div className="flex items-center justify-between gap-4">
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="text-text-secondary">Skills completed:</span>
                    <Badge variant="success">{user.completed_skills}</Badge>
                  </div>
                  {user.selected_roadmap && (
                    <p className="text-text-secondary">Roadmap ID: {user.selected_roadmap}</p>
                  )}
                </div>
                <ProgressRing value={user.overall_completion} size={80} strokeWidth={6} />
              </div>
            </Card>
          ))}
          {!users?.length && (
            <p className="text-text-secondary col-span-2">No users registered yet.</p>
          )}
        </div>
      )}
    </div>
  );
}
