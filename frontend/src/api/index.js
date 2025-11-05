import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.message || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// Models API
export const modelsAPI = {
  getAll: () => api.get('/models'),
  getById: (id) => api.get(`/models/${id}`),
  create: (data) => api.post('/models', data),
  update: (id, data) => api.put(`/models/${id}`, data),
  delete: (id) => api.delete(`/models/${id}`),
  upload: (formData) => {
    return axios.post('/api/models', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000
    })
  }
}

// Datasets API
export const datasetsAPI = {
  getAll: () => api.get('/datasets'),
  getById: (id) => api.get(`/datasets/${id}`),
  create: (data) => api.post('/datasets', data),
  update: (id, data) => api.put(`/datasets/${id}`, data),
  delete: (id) => api.delete(`/datasets/${id}`),
  getStats: (id) => api.get(`/datasets/${id}/stats`),
  upload: (formData) => {
    return axios.post('/api/datasets', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000
    })
  }
}

// Training API
export const trainingAPI = {
  getTasks: () => api.get('/training/tasks'),
  getTask: (id) => api.get(`/training/tasks/${id}`),
  createTask: (data) => api.post('/training/tasks', data),
  stopTask: (id) => api.post(`/training/tasks/${id}/stop`),
  deleteTask: (id) => api.delete(`/training/tasks/${id}`),
  getMetrics: (id) => api.get(`/training/tasks/${id}/metrics`),
  addMetric: (id, data) => api.post(`/training/tasks/${id}/metrics`, data)
}

// AI Chat API
export const chatAPI = {
  sendMessage: (data) => api.post('/chat/message', data),
  getHistory: () => api.get('/chat/history'),
  clearHistory: () => api.delete('/chat/history')
}

export default api
