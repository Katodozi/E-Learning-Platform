import { useQuery } from '@tanstack/react-query';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, BookOpen } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { PublicLayout } from '@/layouts/PublicLayout';
import { roadmapApi } from '@/services/api';
import { useAuthStore } from '@/store/authStore';

export function RoadmapDetailsPage() {
  const { roadmapId } = useParams<{ roadmapId: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();

  const { data: roadmap, isLoading } = useQuery({
    queryKey: ['roadmap', roadmapId],
    queryFn: () => roadmapApi.getRoadmap(Number(roadmapId)).then((r) => r.data),
    enabled: !!roadmapId,
  });

  return (
    <PublicLayout>
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Button variant="ghost" size="sm" className="mb-6" onClick={() => navigate(-1)}>
          <ArrowLeft className="h-4 w-4 mr-2" /> Back
        </Button>

        {isLoading ? (
          <div className="glass rounded-xl h-96 animate-pulse" />
        ) : roadmap ? (
          <>
            <div className="mb-8">
              <Badge className="mb-3">{roadmap.level}</Badge>
              <h1 className="text-3xl font-bold mb-2">{roadmap.title}</h1>
              <p className="text-text-secondary">{roadmap.expertise_name} · {roadmap.estimated_duration}</p>
              <p className="mt-4 text-text-secondary">{roadmap.description}</p>
            </div>

            <h2 className="text-xl font-semibold mb-4">Skills in this Roadmap</h2>
            <div className="space-y-4">
              {roadmap.skills.map((skill) => (
                <Card key={skill.id} hover>
                  <CardHeader>
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          <BookOpen className="h-5 w-5 text-primary" />
                          {skill.name}
                        </CardTitle>
                        <CardDescription>{skill.description}</CardDescription>
                      </div>
                      <Badge variant="accent">{skill.topic_count} topics</Badge>
                    </div>
                  </CardHeader>
                  {isAuthenticated && (
                    <Link to={`/skill/${skill.id}`}>
                      <Button size="sm">Start Skill</Button>
                    </Link>
                  )}
                </Card>
              ))}
            </div>

            {isAuthenticated && (
              <div className="mt-8 flex gap-3">
                <Link to="/dashboard">
                  <Button>Go to Dashboard</Button>
                </Link>
              </div>
            )}
          </>
        ) : (
          <p className="text-text-secondary">Roadmap not found.</p>
        )}
      </div>
    </PublicLayout>
  );
}
