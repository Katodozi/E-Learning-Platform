import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types';
import { adminAuthApi, authApi, initAuthFromStorage, setAuthToken } from '@/services/api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  pendingExpertise: string | null;
  pendingRoadmap: number | null;
  setPendingSelection: (expertise: string | null, roadmap: number | null) => void;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
  init: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      pendingExpertise: null,
      pendingRoadmap: null,

      setPendingSelection: (expertise, roadmap) =>
        set({ pendingExpertise: expertise, pendingRoadmap: roadmap }),

      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const { data } = await authApi.login({ email, password });
          setAuthToken(data.access_token);
          await get().fetchUser();
        } finally {
          set({ isLoading: false });
        }
      },

      register: async (email, password) => {
        set({ isLoading: true });
        try {
          const { pendingExpertise, pendingRoadmap } = get();
          const { data } = await authApi.register({
            email,
            password,
            selected_expertise: pendingExpertise || undefined,
            selected_roadmap: pendingRoadmap || undefined,
          });
          setAuthToken(data.access_token);
          set({ pendingExpertise: null, pendingRoadmap: null });
          await get().fetchUser();
        } finally {
          set({ isLoading: false });
        }
      },

      logout: () => {
        setAuthToken(null);
        set({ user: null, isAuthenticated: false });
      },

      fetchUser: async () => {
        try {
          const { data } = await authApi.me();
          set({ user: data, isAuthenticated: true });
        } catch {
          setAuthToken(null);
          set({ user: null, isAuthenticated: false });
        }
      },

      init: async () => {
        initAuthFromStorage();
        if (localStorage.getItem('token')) {
          await get().fetchUser();
        }
      },
    }),
    {
      name: 'skillforge-auth',
      partialize: (state) => ({
        pendingExpertise: state.pendingExpertise,
        pendingRoadmap: state.pendingRoadmap,
      }),
    },
  ),
);

interface AdminAuthState {
  admin: { id: number; email: string } | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  init: () => Promise<void>;
}

export const useAdminAuthStore = create<AdminAuthState>((set) => ({
  admin: null,
  isAuthenticated: false,

  login: async (email, password) => {
    const { data } = await adminAuthApi.login({ email, password });
    setAuthToken(data.access_token, true);
    const me = await adminAuthApi.me();
    set({ admin: me.data, isAuthenticated: true });
  },

  logout: () => {
    setAuthToken(null, true);
    set({ admin: null, isAuthenticated: false });
  },

  init: async () => {
    initAuthFromStorage();
    if (localStorage.getItem('admin_token')) {
      try {
        const { data } = await adminAuthApi.me();
        set({ admin: data, isAuthenticated: true });
      } catch {
        setAuthToken(null, true);
      }
    }
  },
}));
