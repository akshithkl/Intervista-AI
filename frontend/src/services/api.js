

import axios from "axios";

// Base URL (proxied by Vite to Django)
const api = axios.create({
  baseURL: "/api/", // Added trailing slash for consistency
  headers: {
    "Content-Type": "application/json",
  },
});

// 🔐 Attach token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ✅ Test API
export const testAPI = async () => {
  const res = await api.get("test/");
  return res.data;
};

// 📌 Job roles endpoints
export const jobAPI = {
  getJobRoles: () => api.get("job-roles/"),
};

// 📌 Session endpoints
export const sessionAPI = {
  getSessions: () => api.get("sessions/"),
  createSession: (data) => api.post("sessions/", data),
};

// 📌 AI endpoints
export const aiAPI = {
  generateQuestion: (data) => api.post("generate-question/", data),
  evaluateAnswer: (data) => api.post("evaluate-answer/", data),
};

export default api;


