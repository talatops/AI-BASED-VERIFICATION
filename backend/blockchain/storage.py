"""
Persistent storage manager for the mock blockchain.
Handles saving and loading blockchain state to/from files,
which can be mounted as Docker volumes for persistence.
"""

import os
import json
import logging
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class BlockchainStorage:
    """
    Manages persistent storage for the mock blockchain.
    Uses files in a specified directory to save and load blockchain state.
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the storage manager
        
        Args:
            storage_dir: Directory to store blockchain data files
                         If None, uses 'data/blockchain' relative to current directory
        """
        self.storage_dir = storage_dir or os.environ.get(
            "BLOCKCHAIN_STORAGE_DIR", 
            os.path.join(os.path.dirname(__file__), "../../data/blockchain")
        )
        
        # Ensure storage directory exists
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Define file paths
        self.blockchain_file = os.path.join(self.storage_dir, "blockchain_state.json")
        self.contract_file = os.path.join(self.storage_dir, "identity_contract_state.json")
        
        logger.info(f"Blockchain storage initialized at: {self.storage_dir}")
    
    def save_blockchain_state(self, state: Dict[str, Any]) -> bool:
        """
        Save blockchain state to file
        
        Args:
            state: Dictionary containing blockchain state
            
        Returns:
            bool: True if save was successful
        """
        try:
            # Create a serializable version of the state
            serializable_state = {
                "metadata": {
                    "timestamp": time.time(),
                    "version": "1.0"
                },
                "blocks": [block for block in state.get("blocks", [])],
                "accounts": state.get("accounts", {}),
                "nonces": state.get("nonces", {}),
                "contracts": {
                    addr: {
                        "address": addr,
                        "name": contract_data.get("name", "unknown")
                    } for addr, contract_data in state.get("contracts", {}).items()
                }
            }
            
            # Ensure temporary file doesn't already exist
            temp_file = self.blockchain_file + ".tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Write to temporary file first
            with open(temp_file, 'w') as f:
                json.dump(serializable_state, f, indent=2)
            
            # Rename temp file to target file (atomic operation)
            os.replace(temp_file, self.blockchain_file)
            
            logger.info(f"Blockchain state saved to {self.blockchain_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save blockchain state: {e}")
            return False
    
    def load_blockchain_state(self) -> Optional[Dict[str, Any]]:
        """
        Load blockchain state from file
        
        Returns:
            Dict containing blockchain state or None if file doesn't exist or load fails
        """
        try:
            if not os.path.exists(self.blockchain_file):
                logger.info(f"No blockchain state file found at {self.blockchain_file}")
                return None
            
            with open(self.blockchain_file, 'r') as f:
                state = json.load(f)
            
            logger.info(f"Blockchain state loaded from {self.blockchain_file}")
            return state
            
        except Exception as e:
            logger.error(f"Failed to load blockchain state: {e}")
            return None
    
    def save_contract_state(self, state: Dict[str, Any]) -> bool:
        """
        Save contract state to file
        
        Args:
            state: Dictionary containing contract state
            
        Returns:
            bool: True if save was successful
        """
        try:
            # Create a serializable version of the state
            serializable_state = {
                "metadata": {
                    "timestamp": time.time(),
                    "version": "1.0"
                },
                "identity_records": state.get("identity_records", {}),
                "verification_records": state.get("verification_records", {}),
                "access_grants": state.get("access_grants", {}),
                "zkp_verifications": state.get("zkp_verifications", [])
            }
            
            # Ensure temporary file doesn't already exist
            temp_file = self.contract_file + ".tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Write to temporary file first
            with open(temp_file, 'w') as f:
                json.dump(serializable_state, f, indent=2)
            
            # Rename temp file to target file (atomic operation)
            os.replace(temp_file, self.contract_file)
            
            logger.info(f"Contract state saved to {self.contract_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save contract state: {e}")
            return False
    
    def load_contract_state(self) -> Optional[Dict[str, Any]]:
        """
        Load contract state from file
        
        Returns:
            Dict containing contract state or None if file doesn't exist or load fails
        """
        try:
            if not os.path.exists(self.contract_file):
                logger.info(f"No contract state file found at {self.contract_file}")
                return None
            
            with open(self.contract_file, 'r') as f:
                state = json.load(f)
            
            logger.info(f"Contract state loaded from {self.contract_file}")
            return state
            
        except Exception as e:
            logger.error(f"Failed to load contract state: {e}")
            return None
    
    def auto_save_enabled(self) -> bool:
        """Check if auto-save is enabled via environment variable"""
        return os.environ.get("BLOCKCHAIN_AUTO_SAVE", "true").lower() == "true"
    
    def get_auto_save_interval(self) -> int:
        """Get auto-save interval in seconds from environment variable"""
        try:
            return int(os.environ.get("BLOCKCHAIN_AUTO_SAVE_INTERVAL", "300"))
        except ValueError:
            return 300  # Default to 5 minutes

# Create a singleton instance
storage_manager = BlockchainStorage() 