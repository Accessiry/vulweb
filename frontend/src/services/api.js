import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Models API
export const modelsAPI = {
  getAll: () => api.get('/models'),
  getById: (id) => api.get(`/models/${id}`),
  create: (formData) => api.post('/models', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update: (id, data) => api.put(`/models/${id}`, data),
  delete: (id) => api.delete(`/models/${id}`),
};

// Datasets API
export const datasetsAPI = {
  getAll: () => api.get('/datasets'),
  getById: (id) => api.get(`/datasets/${id}`),
  create: (formData) => api.post('/datasets', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update: (id, data) => api.put(`/datasets/${id}`, data),
  delete: (id) => api.delete(`/datasets/${id}`),
  getStats: (id) => api.get(`/datasets/${id}/stats`),
};

// Training API
export const trainingAPI = {
  getTasks: () => api.get('/training/tasks'),
  getTaskById: (id) => api.get(`/training/tasks/${id}`),
  createTask: (data) => api.post('/training/tasks', data),
  stopTask: (id) => api.post(`/training/tasks/${id}/stop`),
  getMetrics: (id) => api.get(`/training/tasks/${id}/metrics`),
  deleteTask: (id) => api.delete(`/training/tasks/${id}`),
};

export default api;
