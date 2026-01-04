import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const apiService = {
  getLogs: async () => {
    const response = await api.get('/logs');
    return response.data;
  },

  getAlerts: async () => {
    const response = await api.get('/alerts');
    return response.data;
  },

  getAlertCount: async () => {
    const response = await api.get('/alerts/count');
    return response.data;
  },

  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;
