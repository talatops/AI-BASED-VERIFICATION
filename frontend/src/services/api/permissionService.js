import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Handle request errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

const permissionService = {
  /**
   * Grant access to a third party for specific data types
   * 
   * @param {string} userId - User ID
   * @param {string} thirdPartyId - Third party identifier
   * @param {Array<string>} dataTypes - Data types to share
   * @param {number} expiryDays - Number of days until expiry
   * @returns {Promise} - Promise with response data
   */
  grantAccess: async (userId, thirdPartyId, dataTypes, expiryDays = 30) => {
    try {
      return await apiClient.post('/api/verification/grant-access', {
        user_id: userId,
        third_party_id: thirdPartyId,
        data_types: dataTypes,
        expiry_days: expiryDays
      });
    } catch (error) {
      console.error('Grant access error:', error);
      throw error;
    }
  },

  /**
   * Revoke access from a third party
   * 
   * @param {string} userId - User ID
   * @param {string} thirdPartyId - Third party identifier
   * @returns {Promise} - Promise with response data
   */
  revokeAccess: async (userId, thirdPartyId) => {
    try {
      return await apiClient.delete(`/api/verification/revoke-access/${thirdPartyId}`, {
        data: { user_id: userId }
      });
    } catch (error) {
      console.error('Revoke access error:', error);
      throw error;
    }
  },

  /**
   * Get the list of permissions for a user
   * 
   * @param {string} userId - User ID
   * @returns {Promise} - Promise with response data
   */
  getPermissions: async (userId) => {
    try {
      return await apiClient.get('/api/verification/permissions', {
        params: { user_id: userId }
      });
    } catch (error) {
      console.error('Get permissions error:', error);
      throw error;
    }
  }
};

export default permissionService; 