import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, Permission } from '@ultimate-paas/types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  clearAuth: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  hasPermission: (resource: string, action: string) => boolean;
  hasRole: (role: string) => boolean;
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      // State
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Actions
      setUser: (user: User) =>
        set({
          user,
          isAuthenticated: true,
          error: null,
        }),

      setToken: (token: string) =>
        set({
          token,
        }),

      clearAuth: () =>
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
        }),

      setLoading: (isLoading: boolean) =>
        set({
          isLoading,
        }),

      setError: (error: string | null) =>
        set({
          error,
          isLoading: false,
        }),

      hasPermission: (resource: string, action: string) => {
        const { user } = get();
        if (!user) return false;

        return user.permissions.some(
          (permission: Permission) =>
            permission.resource === resource &&
            permission.actions.includes(action)
        );
      },

      hasRole: (role: string) => {
        const { user } = get();
        if (!user) return false;
        return user.role === role;
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
