import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { AuthModal } from '@/components/features/AuthModal';
import { RoadmapCard } from '@/components/features/RoadmapCard';
import { Button } from '@/components/ui/Button';
import { PublicLayout } from '@/layouts/PublicLayout';
import { roadmapApi } from '@/services/api';
import { useAuthStore } from '@/store/authStore';

export function RoadmapSelectionPage() {
  const { expertiseId } = useParams<{ expertiseId: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, login, register, isLoading: authLoading, setPendingSelection } = useAuthStore();
  const [authOpen, setAuthOpen] = useState(false);
  const [selectedRoadmap, setSelectedRoadmap] = useState<number | null>(null);

  const { data: expertise } = useQuery({
    queryKey: ['expertise'],
    queryFn: () => roadmapApi.listExpertise().then((r) => r.data),
  });

  const currentExpertise = expertise?.find((e) => e.id === Number(expertiseId));

  const { data: roadmaps, isLoading } = useQuery({
    queryKey: ['roadmaps', expertiseId],
    queryFn: () => roadmapApi.getRoadmaps(Number(expertiseId)).then((r) => r.data),
    enabled: !!expertiseId,
  });

  const handleStart = (roadmapId: number) => {
    if (isAuthenticated) {
      navigate(`/roadmap/${roadmapId}`);
      return;
    }
    setSelectedRoadmap(roadmapId);
    setPendingSelection(currentExpertise?.name || null, roadmapId);
    setAuthOpen(true);
  };

  const handleAuthSuccess = async (email: string, password: string, isLogin: boolean) => {
    if (isLogin) await login(email, password);
    else await register(email, password);
    if (selectedRoadmap) navigate(`/roadmap/${selectedRoadmap}`);
  };

  return (
    <PublicLayout>
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Button variant="ghost" size="sm" className="mb-6" onClick={() => navigate('/')}>
          <ArrowLeft className="h-4 w-4 mr-2" /> Back to Expertise
        </Button>

        <div className="mb-10">
          <h1 className="text-3xl font-bold mb-2">{currentExpertise?.name || 'Expertise'}</h1>
          <p className="text-text-secondary">{currentExpertise?.description}</p>
        </div>

        <h2 className="text-xl font-semibold mb-6">Choose Your Roadmap Level</h2>

        {isLoading ? (
          <div className="grid md:grid-cols-3 gap-6">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="glass rounded-xl h-64 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid md:grid-cols-3 gap-6">
            {roadmaps?.map((roadmap, i) => (
              <RoadmapCard
                key={roadmap.id}
                roadmap={roadmap}
                index={i}
                highlighted={roadmap.level === 'intermediate'}
                onPreview={() => navigate(`/roadmap/${roadmap.id}`)}
                onStart={() => handleStart(roadmap.id)}
              />
            ))}
          </div>
        )}
      </div>

      <AuthModal
        isOpen={authOpen}
        onClose={() => setAuthOpen(false)}
        isLoading={authLoading}
        onLogin={(email, password) => handleAuthSuccess(email, password, true)}
        onRegister={(email, password) => handleAuthSuccess(email, password, false)}
      />
    </PublicLayout>
  );
}
