import React, { createContext, useState, useEffect, useContext } from 'react';
import { blockchainService } from '../services/api';
import { useAuth } from './AuthContext';

// Create the context
const BlockchainContext = createContext();

// Custom hook to use the blockchain context
export const useBlockchain = () => useContext(BlockchainContext);

// Provider component
export const BlockchainProvider = ({ children }) => {
  const { isAuthenticated, user } = useAuth();
  const [blockchainAddress, setBlockchainAddress] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get user's blockchain address when authenticated
  useEffect(() => {
    const fetchBlockchainAddress = async () => {
      if (!isAuthenticated) {
        setBlockchainAddress(null);
        return;
      }

      try {
        setLoading(true);
        // In a real app, we would call the API
        // const response = await blockchainService.getUserBlockchainAddress();
        // const { address } = response.data;
        
        // Mock blockchain address for now
        const mockAddress = '0x' + Math.random().toString(16).substr(2, 40);
        
        setBlockchainAddress(mockAddress);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch blockchain address:', err);
        setError(err.message || 'Failed to fetch blockchain address');
      } finally {
        setLoading(false);
      }
    };

    fetchBlockchainAddress();
  }, [isAuthenticated, user]);

  // Generate a zero-knowledge proof
  const generateZkp = async (dataType, claim) => {
    try {
      setLoading(true);
      // In a real app, we would call the API
      // const response = await blockchainService.generateZkp(dataType, claim);
      // return response.data;
      
      // Mock ZKP response for now
      return {
        proof: '0x' + Math.random().toString(16).substr(2, 64),
        verified: true,
        dataType,
        claim,
      };
    } catch (err) {
      setError(err.message || 'Failed to generate ZKP');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Get transaction history
  const getTransactionHistory = async () => {
    try {
      setLoading(true);
      // In a real app, we would call the API
      // const response = await blockchainService.getTransactionHistory();
      // setTransactions(response.data);
      
      // Mock transaction history
      const mockTransactions = [
        {
          id: 'tx1',
          type: 'ID Verification',
          timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
          status: 'confirmed',
          txHash: '0x' + Math.random().toString(16).substr(2, 64),
        },
        {
          id: 'tx2',
          type: 'Biometric Verification',
          timestamp: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          status: 'confirmed',
          txHash: '0x' + Math.random().toString(16).substr(2, 64),
        },
        {
          id: 'tx3',
          type: 'Permission Grant',
          timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
          status: 'confirmed',
          txHash: '0x' + Math.random().toString(16).substr(2, 64),
        },
      ];
      
      setTransactions(mockTransactions);
      return mockTransactions;
    } catch (err) {
      setError(err.message || 'Failed to fetch transaction history');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Value object with blockchain state and functions
  const value = {
    blockchainAddress,
    transactions,
    loading,
    error,
    generateZkp,
    getTransactionHistory,
  };

  return <BlockchainContext.Provider value={value}>{children}</BlockchainContext.Provider>;
};

export default BlockchainContext; 