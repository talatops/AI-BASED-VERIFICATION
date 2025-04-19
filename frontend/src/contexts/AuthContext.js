import React, { createContext, useContext, useState } from 'react';

// Create the auth context
const AuthContext = createContext();

// Custom hook to use the auth context
export const useAuth = () => {
  return useContext(AuthContext);
};

// Provider component that wraps the app and makes auth object available
export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState({ uid: 'test-user-id' });
  const [loading, setLoading] = useState(false);

  // Mock sign in function
  const login = async (email, password) => {
    setLoading(true);
    try {
      // In a real app, this would use Firebase/Auth0/etc.
      console.log('Mock login with:', email, password);
      setCurrentUser({ uid: 'test-user-id', email });
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Mock sign out function
  const logout = async () => {
    setLoading(true);
    try {
      // In a real app, this would use Firebase/Auth0/etc.
      setCurrentUser(null);
      return true;
    } catch (error) {
      console.error('Logout error:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Value object to be provided to consumers
  const value = {
    currentUser,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider; 