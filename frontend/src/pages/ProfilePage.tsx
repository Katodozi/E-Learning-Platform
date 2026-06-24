import { useAuthStore } from '@/store/authStore';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

export function ProfilePage() {
  const { user } = useAuthStore();

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold">Profile</h1>
        <p className="text-text-secondary">Your account information</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Account Details</CardTitle>
          <CardDescription>Manage your SkillForge AI profile</CardDescription>
        </CardHeader>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-text-secondary">Email</label>
            <p className="font-medium">{user?.email}</p>
          </div>
          <div>
            <label className="text-sm text-text-secondary">Selected Expertise</label>
            <p className="font-medium">{user?.selected_expertise || 'Not selected'}</p>
          </div>
          <div>
            <label className="text-sm text-text-secondary">Active Roadmap</label>
            {user?.selected_roadmap ? (
              <Badge>Roadmap #{user.selected_roadmap}</Badge>
            ) : (
              <p className="font-medium">Not selected</p>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
}
