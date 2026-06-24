import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { ExpertiseCard } from '@/components/features/ExpertiseCard';
import { HeroSection, PublicLayout } from '@/layouts/PublicLayout';
import { roadmapApi } from '@/services/api';

export function LandingPage() {
  const navigate = useNavigate();
  const { data: expertise, isLoading } = useQuery({
    queryKey: ['expertise'],
    queryFn: () => roadmapApi.listExpertise().then((r) => r.data),
  });

  return (
    <PublicLayout>
      <HeroSection />
      <section id="expertise" className="max-w-7xl mx-auto px-4 pb-20">
        <div className="text-center mb-10">
          <h2 className="text-2xl md:text-3xl font-bold mb-3">Choose Your Expertise</h2>
          <p className="text-text-secondary">Select a domain to explore structured learning roadmaps</p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="glass rounded-xl h-32 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {expertise?.map((exp, i) => (
              <ExpertiseCard
                key={exp.id}
                expertise={exp}
                index={i}
                onClick={() => navigate(`/expertise/${exp.id}`)}
              />
            ))}
          </div>
        )}
      </section>
    </PublicLayout>
  );
}
