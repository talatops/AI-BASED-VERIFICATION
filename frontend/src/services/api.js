import axios from 'axios';

// This will be replaced with actual backend API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create an axios instance with common configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for auth tokens
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication services
export const authService = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
};

// Identity verification services
export const identityService = {
  verifyBiometric: (biometricData) => api.post('/identity/verify/biometric', biometricData),
  verifyGovernmentId: (idData) => api.post('/identity/verify/id', idData),
  getVerificationStatus: () => api.get('/identity/verification-status'),
};

// Blockchain-related services
export const blockchainService = {
  getUserBlockchainAddress: () => api.get('/blockchain/user-address'),
  getTransactionHistory: () => api.get('/blockchain/transactions'),
  generateZkp: (dataType, claim) => api.post('/blockchain/generate-zkp', { dataType, claim }),
};

// Permission management services
export const permissionService = {
  getAllPermissions: () => api.get('/permissions'),
  grantPermission: (serviceData) => api.post('/permissions', serviceData),
  revokePermission: (permissionId) => api.delete(`/permissions/${permissionId}`),
  updatePermission: (permissionId, updates) => api.put(`/permissions/${permissionId}`, updates),
};

// User profile services
export const userService = {
  getUserProfile: () => api.get('/user/profile'),
  updateUserProfile: (profileData) => api.put('/user/profile', profileData),
  getPrivacySettings: () => api.get('/user/privacy-settings'),
  updatePrivacySettings: (settings) => api.put('/user/privacy-settings', settings),
};

export default {
  authService,
  identityService,
  blockchainService,
  permissionService,
  userService,
}; 