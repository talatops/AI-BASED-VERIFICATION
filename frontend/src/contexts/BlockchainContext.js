import React, { createContext, useContext, useState } from 'react';

// Create the blockchain context
const BlockchainContext = createContext();

// Custom hook to use the blockchain context
export const useBlockchain = () => {
  return useContext(BlockchainContext);
};

// Provider component that wraps the app and makes blockchain object available
export function BlockchainProvider({ children }) {
  const [connected, setConnected] = useState(false);
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Mock connect function
  const connect = async () => {
    setLoading(true);
    try {
      // In a real app, this would connect to MetaMask or another wallet
      console.log('Mock connecting to blockchain');
      setAccount('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1');
      setConnected(true);
      return true;
    } catch (error) {
      console.error('Blockchain connection error:', error);
      setError('Failed to connect to blockchain');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Mock disconnect function
  const disconnect = async () => {
    setLoading(true);
    try {
      // In a real app, this would disconnect from the wallet
      console.log('Mock disconnecting from blockchain');
      setAccount(null);
      setConnected(false);
      return true;
    } catch (error) {
      console.error('Blockchain disconnection error:', error);
      setError('Failed to disconnect from blockchain');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Value object to be provided to consumers
  const value = {
    connected,
    account,
    loading,
    error,
    connect,
    disconnect
  };

  return (
    <BlockchainContext.Provider value={value}>
      {children}
    </BlockchainContext.Provider>
  );
}

export default BlockchainProvider; 