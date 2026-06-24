import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Zap } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useAuthStore } from '@/store/authStore';

interface PublicLayoutProps {
  children: React.ReactNode;
}

export function PublicLayout({ children }: PublicLayoutProps) {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="min-h-screen">
      <header className="glass border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <Zap className="h-6 w-6 text-primary" />
            <span className="font-bold text-xl">SkillForge AI</span>
          </Link>
          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <Link to="/dashboard">
                <Button size="sm">Dashboard</Button>
              </Link>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost" size="sm">Login</Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">Get Started</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </header>
      {children}
    </div>
  );
}

export function HeroSection() {
  return (
    <section className="relative overflow-hidden py-16 md:py-24 px-4">
      <div className="absolute inset-0 bg-gradient-radial from-primary/10 via-transparent to-transparent" />
      <div className="max-w-4xl mx-auto text-center relative">
        <div className="inline-flex items-center gap-2 glass rounded-full px-4 py-1.5 text-sm text-accent mb-6">
          <Sparkles className="h-4 w-4" />
          AI-Powered Learning Roadmaps
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6">
          Forge Your Skills with{' '}
          <span className="gradient-text">Intelligent Roadmaps</span>
        </h1>
        <p className="text-lg md:text-xl text-text-secondary max-w-2xl mx-auto mb-8">
          Choose your expertise, follow structured learning paths, and let AI generate
          personalized content and quizzes to accelerate your growth.
        </p>
        <Link to="#expertise">
          <Button size="lg" className="gap-2">
            Explore Expertise <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </div>
    </section>
  );
}
