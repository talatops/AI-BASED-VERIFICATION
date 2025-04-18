"""
Service for blockchain-based verification and privacy management.
Uses a mock implementation that simulates blockchain behaviors.
"""

import json
import logging
import hashlib
import time
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Import Web3 for type hinting but we'll use mocks instead of real transactions
from web3 import Web3

logger = logging.getLogger(__name__)

class BlockchainService:
    """
    Service for managing verification status and data access permissions
    using blockchain technology for security and auditability.
    
    This is a mock implementation that simulates blockchain behavior without requiring
    actual gas or transactions, while maintaining the same interface as the real implementation.
    """
    
    def __init__(self):
        """Initialize the mock blockchain service."""
        self.logger = logging.getLogger(__name__)
        
        # Load configuration 
        self.config = self._load_config()
        
        # Initialize storage for our mock blockchain
        self.verification_cache = {}  # Mock storage for verification records
        self.access_grants_cache = {}  # Mock storage for access grants
        self.identities = {}  # Mock storage for identity records
        self.zkp_verifications = []  # Mock storage for ZKP verifications
        
        # Mock blockchain state
        self.current_block = 1000
        self.events = {
            "VerificationUpdated": [],
            "AccessGranted": [],
            "AccessRevoked": [],
            "ZKProofVerified": []
        }
        
        self.logger.info("Mock BlockchainService initialized")
    
    def _load_config(self) -> Dict:
        """Load blockchain configuration from environment or file"""
        config = {
            "provider_url": os.environ.get("BLOCKCHAIN_NODE_URL", "http://mock-blockchain:8545"),
            "chain_id": int(os.environ.get("CHAIN_ID", "1337")),
            "account_address": os.environ.get("BLOCKCHAIN_ACCOUNT_ADDRESS", "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"),
            "private_key": os.environ.get("BLOCKCHAIN_PRIVATE_KEY", "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"),
            "contracts": {
                "identity_verification": {
                    "address": os.environ.get("IDENTITY_CONTRACT_ADDRESS", "0xCfEB869F69431e42cdB54A4F4f105C19C080A601")
                }
            }
        }
        
        # Try to load from local config if available
        try:
            with open(os.path.join(os.path.dirname(__file__), "../config/blockchain.json"), "r") as f:
                file_config = json.load(f)
                config.update(file_config)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Could not load blockchain config from file: {e}")
        
        return config
    
    def update_verification_status(self, user_id: str, verification_type: str, status: bool) -> bool:
        """
        Update a user's verification status (mock blockchain implementation).
        
        Args:
            user_id: The unique identifier for the user
            verification_type: The type of verification (facial, document, etc.)
            status: The verification status (True for verified)
            
        Returns:
            bool: True if the update was successful
        """
        try:
            # Convert status to enum value (0=Pending, 1=Verified, 2=Rejected)
            status_enum = 1 if status else 2
            verification_type_enum = self._get_verification_type_enum(verification_type)
            
            # Generate a mock transaction hash
            tx_hash = self._generate_mock_transaction_hash(user_id, verification_type)
            
            # Update the mock blockchain state
            self.current_block += 1
            
            # Create user record if it doesn't exist
            if user_id not in self.verification_cache:
                self.verification_cache[user_id] = {}
            
            # Update the verification status
            self.verification_cache[user_id][verification_type] = {
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "transaction_hash": tx_hash,
                "block_number": self.current_block
            }
            
            # Record the event for later querying
            self.events["VerificationUpdated"].append({
                "args": {
                    "owner": self._user_id_to_address(user_id),
                    "verificationType": verification_type_enum,
                    "status": status_enum
                },
                "blockNumber": self.current_block,
                "transactionHash": bytes.fromhex(tx_hash.replace("0x", "")),
                "logIndex": len(self.events["VerificationUpdated"])
            })
            
            self.logger.info(f"Updated {verification_type} verification status to {status} for user {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update verification status: {e}")
            return False
    
    def get_verification_status(self, user_id: str, verification_type: str) -> bool:
        """
        Get a user's verification status from the mock blockchain.
        
        Args:
            user_id: The unique identifier for the user
            verification_type: The type of verification to check
            
        Returns:
            bool: The verification status (False if not found)
        """
        try:
            # Check if we have a cached status
            if user_id in self.verification_cache and verification_type in self.verification_cache[user_id]:
                return self.verification_cache[user_id][verification_type]["status"]
            
            # If not in cache, return not verified
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to get verification status: {e}")
            return False
    
    def grant_access(self, user_id: str, third_party_id: str, data_types: List[str], 
                     expiry_days: int = 30) -> bool:
        """
        Grant access to a third party for specific data types (mock implementation).
        
        Args:
            user_id: The user granting access
            third_party_id: The third party receiving access
            data_types: List of data types to grant access to
            expiry_days: Number of days until access expires
            
        Returns:
            bool: True if access was granted successfully
        """
        try:
            # Generate a mock transaction hash
            tx_hash = self._generate_mock_transaction_hash(user_id, third_party_id)
            
            # Update the mock blockchain state
            self.current_block += 1
            
            # Calculate expiry timestamp
            expiry_timestamp = int((datetime.now() + timedelta(days=expiry_days)).timestamp())
            
            # Create user entry if it doesn't exist
            if user_id not in self.access_grants_cache:
                self.access_grants_cache[user_id] = {}
            
            # Set the access grant with expiry
            self.access_grants_cache[user_id][third_party_id] = {
                "data_types": data_types,
                "granted_at": datetime.now().isoformat(),
                "expires_at": datetime.fromtimestamp(expiry_timestamp).isoformat(),
                "transaction_hash": tx_hash,
                "block_number": self.current_block
            }
            
            # Record the event for later querying
            self.events["AccessGranted"].append({
                "args": {
                    "user": self._user_id_to_address(user_id),
                    "thirdParty": self._user_id_to_address(third_party_id),
                    "expiryTimestamp": expiry_timestamp
                },
                "blockNumber": self.current_block,
                "transactionHash": bytes.fromhex(tx_hash.replace("0x", "")),
                "logIndex": len(self.events["AccessGranted"])
            })
            
            self.logger.info(f"Granted access to {third_party_id} for user {user_id} data types: {data_types}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to grant access: {e}")
            return False
    
    def revoke_access(self, user_id: str, third_party_id: str) -> bool:
        """
        Revoke access previously granted to a third party (mock implementation).
        
        Args:
            user_id: The user revoking access
            third_party_id: The third party losing access
            
        Returns:
            bool: True if access was revoked successfully
        """
        try:
            # Check if access exists
            if user_id not in self.access_grants_cache or third_party_id not in self.access_grants_cache[user_id]:
                self.logger.warning(f"No access found to revoke for user {user_id} and third party {third_party_id}")
                return False
            
            # Generate a mock transaction hash
            tx_hash = self._generate_mock_transaction_hash(user_id, f"revoke:{third_party_id}")
            
            # Update the mock blockchain state
            self.current_block += 1
            
            # Mark as revoked
            self.access_grants_cache[user_id][third_party_id]["revoked_at"] = datetime.now().isoformat()
            self.access_grants_cache[user_id][third_party_id]["revoke_transaction_hash"] = tx_hash
            self.access_grants_cache[user_id][third_party_id]["revoke_block_number"] = self.current_block
            
            # Record the event for later querying
            self.events["AccessRevoked"].append({
                "args": {
                    "user": self._user_id_to_address(user_id),
                    "thirdParty": self._user_id_to_address(third_party_id)
                },
                "blockNumber": self.current_block,
                "transactionHash": bytes.fromhex(tx_hash.replace("0x", "")),
                "logIndex": len(self.events["AccessRevoked"])
            })
            
            self.logger.info(f"Revoked access from {third_party_id} for user {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to revoke access: {e}")
            return False
    
    def check_access(self, user_id: str, third_party_id: str, data_type: str) -> bool:
        """
        Check if a third party has access to a specific data type (mock implementation).
        
        Args:
            user_id: The user who granted access
            third_party_id: The third party to check
            data_type: The data type to check access for
            
        Returns:
            bool: True if access is granted and not expired
        """
        try:
            if user_id not in self.access_grants_cache or third_party_id not in self.access_grants_cache[user_id]:
                return False
            
            access = self.access_grants_cache[user_id][third_party_id]
            
            # Check if access has been revoked
            if "revoked_at" in access:
                return False
            
            # Check if access has expired
            expiry = datetime.fromisoformat(access["expires_at"])
            if datetime.now() > expiry:
                return False
            
            # Check if the requested data type is in the granted types
            return data_type in access["data_types"]
            
        except Exception as e:
            self.logger.error(f"Failed to check access: {e}")
            return False
    
    def record_zkp_verification(self, user_id: str, third_party_id: str, 
                               proof_hash: str, data_type: str) -> bool:
        """
        Record a Zero-Knowledge Proof verification (mock implementation).
        
        Args:
            user_id: The user whose data was verified
            third_party_id: The third party that verified the data
            proof_hash: The hash of the zero-knowledge proof
            data_type: The type of data that was verified
            
        Returns:
            bool: True if the record was created successfully
        """
        try:
            # Check if the third party has access
            if not self.check_access(user_id, third_party_id, data_type):
                self.logger.warning(f"Third party {third_party_id} doesn't have access to {data_type} for user {user_id}")
                return False
            
            # Generate a mock transaction hash
            tx_hash = self._generate_mock_transaction_hash(user_id, proof_hash)
            
            # Update the mock blockchain state
            self.current_block += 1
            
            # Record the verification
            verification_record = {
                "user_id": user_id,
                "third_party_id": third_party_id,
                "data_type": data_type,
                "proof_hash": proof_hash,
                "timestamp": datetime.now().isoformat(),
                "transaction_hash": tx_hash,
                "block_number": self.current_block
            }
            
            self.zkp_verifications.append(verification_record)
            
            # Record the event for later querying
            data_type_bytes32 = proof_hash  # Simplified for mock
            self.events["ZKProofVerified"].append({
                "args": {
                    "user": self._user_id_to_address(user_id),
                    "verifier": self._user_id_to_address(third_party_id),
                    "dataType": data_type_bytes32
                },
                "blockNumber": self.current_block,
                "transactionHash": bytes.fromhex(tx_hash.replace("0x", "")),
                "logIndex": len(self.events["ZKProofVerified"])
            })
            
            self.logger.info(f"Recorded ZKP verification for user {user_id} by {third_party_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to record ZKP verification: {e}")
            return False
    
    def get_verification_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get the verification history for a user (mock implementation).
        
        Args:
            user_id: The user to get history for
            
        Returns:
            List of verification records
        """
        try:
            # Extract events for this user from our mock events storage
            user_address = self._user_id_to_address(user_id)
            verification_records = []
            
            # Get events related to this user
            for event in self.events["VerificationUpdated"]:
                if event["args"]["owner"].lower() == user_address.lower():
                    verification_records.append({
                        'user_id': user_id,
                        'verification_type': self._get_verification_type_name(event["args"]["verificationType"]),
                        'status': event["args"]["status"] == 1,  # 1 is Verified
                        'timestamp': datetime.now().replace(minute=event["blockNumber"] % 60).isoformat(),  # Mock timestamp
                        'transaction_hash': event["transactionHash"].hex(),
                        'block_number': event["blockNumber"]
                    })
            
            return verification_records
            
        except Exception as e:
            self.logger.error(f"Failed to get verification history: {e}")
            return []
    
    def get_user_verification_audit(self, user_id: str) -> Dict[str, Any]:
        """
        Get a complete audit of a user's verifications and access grants.
        
        Args:
            user_id: The user to get audit for
            
        Returns:
            dict: Complete audit information
        """
        try:
            # Get verification history
            verification_history = self.get_verification_history(user_id)
            
            # Get access grants
            access_grants = self._get_user_access_grants(user_id)
            
            # Get ZKP verifications
            zkp_verifications = self._get_user_zkp_verifications(user_id)
            
            return {
                'user_id': user_id,
                'verification_history': verification_history,
                'access_grants': access_grants,
                'zkp_verifications': zkp_verifications,
                'audit_generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get user verification audit: {e}")
            return {
                'user_id': user_id,
                'error': str(e),
                'audit_generated_at': datetime.now().isoformat()
            }
    
    def _get_user_access_grants(self, user_id: str) -> List[Dict[str, Any]]:
        """Get access grants for a user (mock implementation)"""
        try:
            # Extract from our mock storage
            if user_id not in self.access_grants_cache:
                return []
            
            result = []
            for third_party_id, grant_data in self.access_grants_cache[user_id].items():
                result.append({
                    'third_party_id': third_party_id,
                    'granted_at': grant_data.get('granted_at'),
                    'expires_at': grant_data.get('expires_at'),
                    'transaction_hash': grant_data.get('transaction_hash'),
                    'status': 'revoked' if 'revoked_at' in grant_data else 'active',
                    'revoked_at': grant_data.get('revoked_at'),
                    'revoke_transaction_hash': grant_data.get('revoke_transaction_hash')
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get user access grants: {e}")
            return []
    
    def _get_user_zkp_verifications(self, user_id: str) -> List[Dict[str, Any]]:
        """Get ZKP verifications for a user (mock implementation)"""
        try:
            # Filter verifications for this user
            return [v for v in self.zkp_verifications if v["user_id"] == user_id]
            
        except Exception as e:
            self.logger.error(f"Failed to get user ZKP verifications: {e}")
            return []
    
    def _generate_mock_transaction_hash(self, *args) -> str:
        """Generate a mock blockchain transaction hash."""
        # In a real implementation, this would be the hash returned by the blockchain
        combined = str(args) + str(time.time()) + str(uuid.uuid4())
        return "0x" + hashlib.sha256(combined.encode()).hexdigest()
    
    def _user_id_to_address(self, user_id: str) -> str:
        """Convert a user ID to an Ethereum address"""
        # If it's already an Ethereum address, return it
        if user_id.startswith("0x") and len(user_id) == 42:
            return user_id
        
        # Otherwise, derive an address from the user ID
        h = hashlib.sha256(user_id.encode()).digest()
        addr = '0x' + h[-20:].hex()
        return addr
    
    def _address_to_user_id(self, address: str) -> str:
        """Convert an Ethereum address to a user ID"""
        # In production, lookup the user ID from a database
        # For this mock implementation, we'll just use the address as the ID
        return address
    
    def _get_verification_type_enum(self, verification_type: str) -> int:
        """Map verification type string to enum value used in contract"""
        mapping = {
            'government_id': 0,
            'document': 0,  # Alias for government_id
            'biometric': 1,
            'facial': 1,    # Alias for biometric
            'address': 2
        }
        return mapping.get(verification_type.lower(), 0)
    
    def _get_verification_type_name(self, verification_type_enum: int) -> str:
        """Map verification type enum to string name"""
        mapping = {
            0: 'government_id',
            1: 'biometric',
            2: 'address'
        }
        return mapping.get(verification_type_enum, 'unknown')


# Initialize the singleton instance
blockchain_service = BlockchainService() 