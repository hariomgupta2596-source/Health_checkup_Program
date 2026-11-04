import axios from 'axios';

const rawBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const baseURL = rawBaseUrl.replace(/\/+$/, '');

const api = axios.create({
  baseURL,
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const userId = localStorage.getItem('user_id');
    if (userId) {
      config.headers['x-user-id'] = userId;
    }
  }
  return config;
});

export default api;
