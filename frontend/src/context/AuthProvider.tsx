import { useState, useEffect } from "react";
import type { ReactNode } from "react";
import AuthContext from "./AuthContext";
import axiosInstance from "@/utils/axiosInstance";

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    if (storedToken) setToken(storedToken);
  }, []);

  const login = (newToken: string) => {
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setToken(null);
  };

  const refreshAccessToken = async (): Promise<boolean> => {
    const refresh_token = localStorage.getItem("refresh_token");
    if (!refresh_token) {
      logout();
      return false;
    }

    try {
      const response = await axiosInstance.post<{
        access_token: string;
        token_type: string;
      }>("/api/v1/auth/refresh-token", {
        refresh_token,
      });

      const newToken = response.data.access_token;
      login(newToken);
      return true;
    } catch (error) {
      console.error("Refresh token failed:", error);
      logout();
      return false;
    }
  };

  return (
    <AuthContext.Provider
      value={{ token, isAuthenticated: !!token, login, logout, refreshAccessToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};
