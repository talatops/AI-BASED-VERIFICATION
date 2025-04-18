import React, { createContext, useState, useEffect, useContext } from 'react';
import { authService } from '../services/api';

// Create the context
const AuthContext = createContext();

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);

// Provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is already logged in on component mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const token = localStorage.getItem('authToken');
        if (token) {
          // For now, we'll just mock the user data
          // In a real app, we would validate the token with the server
          setUser({
            id: 'mock-user-id',
            firstName: 'John',
            lastName: 'Doe',
            email: 'john.doe@example.com',
          });
        }
      } catch (err) {
        console.error('Auth check failed:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  // Login function
  const login = async (credentials) => {
    try {
      setLoading(true);
      // In a real app, we would call the API
      // const response = await authService.login(credentials);
      // const { token, user } = response.data;
      
      // Mock successful login for now
      const mockToken = 'mock-jwt-token';
      const mockUser = {
        id: 'mock-user-id',
        firstName: 'John',
        lastName: 'Doe',
        email: credentials.email,
      };
      
      localStorage.setItem('authToken', mockToken);
      setUser(mockUser);
      setError(null);
      return mockUser;
    } catch (err) {
      setError(err.message || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      setLoading(true);
      // In a real app, we would call the API
      // const response = await authService.register(userData);
      // const { token, user } = response.data;
      
      // Mock successful registration
      const mockToken = 'mock-jwt-token';
      const mockUser = {
        id: 'mock-user-id',
        firstName: userData.firstName,
        lastName: userData.lastName,
        email: userData.email,
      };
      
      localStorage.setItem('authToken', mockToken);
      setUser(mockUser);
      setError(null);
      return mockUser;
    } catch (err) {
      setError(err.message || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('authToken');
    setUser(null);
  };

  // Create value object with authentication state and functions
  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext; 