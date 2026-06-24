import { useEffect } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DashboardLayout } from '@/layouts/DashboardLayout';
import { AdminLayout } from '@/layouts/AdminLayout';
import { LandingPage } from '@/pages/LandingPage';
import { RoadmapSelectionPage } from '@/pages/RoadmapSelectionPage';
import { RoadmapDetailsPage } from '@/pages/RoadmapDetailsPage';
import { LoginPage, RegisterPage } from '@/pages/AuthPages';
import { DashboardPage } from '@/pages/DashboardPage';
import { SkillLearningPage } from '@/pages/SkillLearningPage';
import { QuizPage } from '@/pages/QuizPage';
import { ProfilePage } from '@/pages/ProfilePage';
import { AdminLoginPage } from '@/pages/admin/AdminLoginPage';
import { AdminDashboardPage } from '@/pages/admin/AdminDashboardPage';
import { AdminExpertisePage } from '@/pages/admin/AdminExpertisePage';
import { AdminRoadmapPage } from '@/pages/admin/AdminRoadmapPage';
import { AdminPromptPage } from '@/pages/admin/AdminPromptPage';
import { AdminUsersPage } from '@/pages/admin/AdminUsersPage';
import { ProtectedRoute, AdminProtectedRoute, GuestRoute } from '@/routes/ProtectedRoute';
import { useAdminAuthStore, useAuthStore } from '@/store/authStore';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 30000 } },
});

function AppInit() {
  const initAuth = useAuthStore((s) => s.init);
  const initAdmin = useAdminAuthStore((s) => s.init);

  useEffect(() => {
    initAuth();
    initAdmin();
  }, [initAuth, initAdmin]);

  return null;
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppInit />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/expertise/:expertiseId" element={<RoadmapSelectionPage />} />
          <Route path="/roadmap/:roadmapId" element={<RoadmapDetailsPage />} />

          <Route element={<GuestRoute />}>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Route>

          <Route element={<ProtectedRoute />}>
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>
            <Route path="/skill/:skillId" element={<SkillLearningPage />} />
            <Route path="/quiz/:skillId" element={<QuizPage />} />
          </Route>

          <Route path="/admin/login" element={<AdminLoginPage />} />
          <Route element={<AdminProtectedRoute />}>
            <Route element={<AdminLayout />}>
              <Route path="/admin" element={<AdminDashboardPage />} />
              <Route path="/admin/expertise" element={<AdminExpertisePage />} />
              <Route path="/admin/roadmaps" element={<AdminRoadmapPage />} />
              <Route path="/admin/prompts" element={<AdminPromptPage />} />
              <Route path="/admin/users" element={<AdminUsersPage />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
