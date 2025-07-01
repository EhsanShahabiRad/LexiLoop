import axios from "axios";

interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || "",
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error?.response?.status;
    const hasRefresh = !!localStorage.getItem("refresh_token");

    if (
      status === 401 &&
      error.config &&
      !error.config._retry &&
      hasRefresh
    ) {
      // Type-safe override of config
      const originalRequest = error.config as typeof error.config & { _retry?: boolean };
      originalRequest._retry = true;

      try {
        const refreshRes = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/api/v1/auth/refresh-token`,
          {
            refresh_token: localStorage.getItem("refresh_token"),
          }
        );

        const newToken = (refreshRes.data as RefreshTokenResponse).access_token;
        localStorage.setItem("access_token", newToken);

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
        }

        return axiosInstance(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
