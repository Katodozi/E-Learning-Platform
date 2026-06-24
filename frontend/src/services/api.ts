import axios from 'axios';
import type {
  Analytics,
  DashboardData,
  Expertise,
  PromptTemplate,
  QuizQuestion,
  QuizResult,
  RoadmapDetail,
  RoadmapSummary,
  SkillContent,
  User,
  UserProgressSummary,
} from '@/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

export function setAuthToken(token: string | null, isAdmin = false) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
    localStorage.setItem(isAdmin ? 'admin_token' : 'token', token);
  } else {
    delete api.defaults.headers.common.Authorization;
    localStorage.removeItem(isAdmin ? 'admin_token' : 'token');
  }
}

export function initAuthFromStorage() {
  const token = localStorage.getItem('token');
  const adminToken = localStorage.getItem('admin_token');
  if (adminToken) setAuthToken(adminToken, true);
  else if (token) setAuthToken(token);
}

// Auth
export const authApi = {
  register: (data: { email: string; password: string; selected_expertise?: string; selected_roadmap?: number }) =>
    api.post<{ access_token: string }>('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post<{ access_token: string }>('/auth/login', data),
  me: () => api.get<User>('/auth/me'),
};

export const adminAuthApi = {
  login: (data: { email: string; password: string }) =>
    api.post<{ access_token: string }>('/admin/login', data),
  me: () => api.get<{ id: number; email: string }>('/admin/me'),
};

// Roadmaps
export const roadmapApi = {
  listExpertise: () => api.get<Expertise[]>('/expertise'),
  getRoadmaps: (expertiseId: number) => api.get<RoadmapSummary[]>(`/roadmaps/${expertiseId}`),
  getRoadmap: (roadmapId: number) => api.get<RoadmapDetail>(`/roadmap/${roadmapId}`),
};

// Skills & Topics
export const skillApi = {
  getSkill: (skillId: number) => api.get<SkillContent>(`/skills/${skillId}`),
  completeTopic: (topicId: number) => api.post('/topics/complete', { topic_id: topicId }),
};

// Quiz
export const quizApi = {
  generate: (skillId: number) => api.post<{ skill_id: number; questions: QuizQuestion[]; cached: boolean }>('/quiz/generate', { skill_id: skillId }),
  submit: (skillId: number, answers: number[]) =>
    api.post<QuizResult>('/quiz/submit', { skill_id: skillId, answers }),
};

// Dashboard
export const dashboardApi = {
  get: () => api.get<DashboardData>('/dashboard'),
};

// Admin
export const adminApi = {
  listExpertise: () => api.get<Expertise[]>('/admin/expertise'),
  createExpertise: (data: Partial<Expertise>) => api.post<Expertise>('/admin/expertise', data),
  updateExpertise: (id: number, data: Partial<Expertise>) => api.put<Expertise>(`/admin/expertise/${id}`, data),
  deleteExpertise: (id: number) => api.delete(`/admin/expertise/${id}`),
  listRoadmaps: (expertiseId?: number) => api.get<RoadmapSummary[]>('/admin/roadmaps', { params: { expertise_id: expertiseId } }),
  createRoadmap: (data: Record<string, unknown>) => api.post('/admin/roadmaps', data),
  updateRoadmap: (id: number, data: Record<string, unknown>) => api.put(`/admin/roadmaps/${id}`, data),
  deleteRoadmap: (id: number) => api.delete(`/admin/roadmaps/${id}`),
  listSkills: (roadmapId: number) => api.get(`/admin/roadmaps/${roadmapId}/skills`),
  createSkill: (data: Record<string, unknown>) => api.post('/admin/skills', data),
  updateSkill: (id: number, data: Record<string, unknown>) => api.put(`/admin/skills/${id}`, data),
  deleteSkill: (id: number) => api.delete(`/admin/skills/${id}`),
  listTopics: (skillId: number) => api.get(`/admin/skills/${skillId}/topics`),
  createTopic: (data: Record<string, unknown>) => api.post('/admin/topics', data),
  updateTopic: (id: number, data: Record<string, unknown>) => api.put(`/admin/topics/${id}`, data),
  deleteTopic: (id: number) => api.delete(`/admin/topics/${id}`),
  listPrompts: () => api.get<PromptTemplate[]>('/admin/prompts'),
  createPrompt: (data: Partial<PromptTemplate>) => api.post<PromptTemplate>('/admin/prompts', data),
  updatePrompt: (id: number, data: Partial<PromptTemplate>) => api.put<PromptTemplate>(`/admin/prompts/${id}`, data),
  deletePrompt: (id: number) => api.delete(`/admin/prompts/${id}`),
  clearCache: (skillId: number) => api.delete(`/admin/cache/skills/${skillId}`),
  listUsers: () => api.get<UserProgressSummary[]>('/admin/users'),
  analytics: () => api.get<Analytics>('/admin/analytics'),
};
