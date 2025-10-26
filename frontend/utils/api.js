import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export const registerUser = async (email, password) => {
  return api.post("/auth/register", { email, password });
};

export const loginUser = async (email, password) => {
  return api.post("/auth/login", { email, password });
};

export const getLessons = async (token) => {
  return api.get("/lessons/", {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export default api;
