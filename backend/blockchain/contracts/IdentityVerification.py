"""
Mock Identity Verification Contract for local development and testing.
This simulates a smart contract for identity verification without requiring a real blockchain.
"""

import json
import time
import logging
import threading
from typing import Dict, List, Any, Optional
from ..contracts.MockBlockchain import mock_blockchain, MockContract, Event
from ..storage import storage_manager

logger = logging.getLogger(__name__)

class IdentityVerificationContract:
    """
    Mock implementation of an Identity Verification smart contract.
    This class simulates the behavior of a blockchain-based identity verification contract
    without requiring real transactions or gas.
    """
    
    def __init__(self, contract_address: str = None):
        """
        Initialize the mock contract with default data
        
        Args:
            contract_address: Optional address to use for the contract
        """
        # Define the contract ABI for this mock contract
        self.abi = self._load_abi()
        
        # Initialize state storage for the contract
        self.identity_records = {}  # owner_address -> identity data
        self.verification_records = {}  # owner_address -> {verification_type -> status}
        self.access_grants = {}  # owner_address -> {third_party_address -> {data_types, expiry}}
        self.zkp_verifications = []  # List of ZKP verification records
        
        # Try to load state from storage
        self._load_state()
        
        # Load existing contract or deploy a new one
        if contract_address and contract_address in mock_blockchain.contracts:
            self.contract = mock_blockchain.get_contract(contract_address)
        else:
            # Deploy the contract to the mock blockchain
            self.contract = self._deploy_contract()
        
        # Event types
        self.event_types = {
            "VerificationUpdated": {
                "owner": "address",
                "verificationType": "uint8",
                "status": "uint8"
            },
            "AccessGranted": {
                "user": "address",
                "thirdParty": "address",
                "expiryTimestamp": "uint256"
            },
            "AccessRevoked": {
                "user": "address",
                "thirdParty": "address"
            },
            "ZKProofVerified": {
                "user": "address",
                "verifier": "address",
                "dataType": "bytes32"
            }
        }
        
        # Set up auto-save if enabled
        if storage_manager.auto_save_enabled():
            self._setup_auto_save()
            
        logger.info("IdentityVerificationContract initialized")
    
    def _setup_auto_save(self):
        """Set up periodic auto-save"""
        interval = storage_manager.get_auto_save_interval()
        
        def auto_save_worker():
            while True:
                time.sleep(interval)
                self.save_state()
        
        # Start auto-save thread
        auto_save_thread = threading.Thread(target=auto_save_worker, daemon=True)
        auto_save_thread.start()
        
        logger.info(f"Contract auto-save enabled with interval of {interval} seconds")
    
    def _load_state(self):
        """Load contract state from storage"""
        state = storage_manager.load_contract_state()
        if state:
            try:
                # Load identity records
                self.identity_records = state.get("identity_records", {})
                
                # Load verification records
                self.verification_records = state.get("verification_records", {})
                
                # Load access grants
                self.access_grants = state.get("access_grants", {})
                
                # Load ZKP verifications
                self.zkp_verifications = state.get("zkp_verifications", [])
                
                logger.info(f"Loaded contract state with {len(self.identity_records)} identities")
                return True
            except Exception as e:
                logger.error(f"Error loading contract state: {e}")
                return False
        return False
    
    def save_state(self):
        """Save contract state to storage"""
        try:
            # Create state dictionary
            state = {
                "identity_records": self.identity_records,
                "verification_records": self.verification_records,
                "access_grants": self.access_grants,
                "zkp_verifications": self.zkp_verifications
            }
            
            # Save to storage
            success = storage_manager.save_contract_state(state)
            
            if success:
                logger.info("Contract state saved successfully")
            else:
                logger.warning("Failed to save contract state")
                
            return success
        except Exception as e:
            logger.error(f"Error saving contract state: {e}")
            return False
    
    def _load_abi(self) -> List[Dict[str, Any]]:
        """
        Load the ABI for the contract
        
        Returns:
            List of ABI definitions
        """
        try:
            with open('backend/blockchain/abis/IdentityVerification.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If ABI file doesn't exist, return a minimal ABI
            return [
                {
                    "name": "VerificationUpdated",
                    "type": "event",
                    "inputs": [
                        {"name": "owner", "type": "address", "indexed": True},
                        {"name": "verificationType", "type": "uint8", "indexed": True},
                        {"name": "status", "type": "uint8", "indexed": False}
                    ]
                },
                {
                    "name": "AccessGranted",
                    "type": "event",
                    "inputs": [
                        {"name": "user", "type": "address", "indexed": True},
                        {"name": "thirdParty", "type": "address", "indexed": True},
                        {"name": "expiryTimestamp", "type": "uint256", "indexed": False}
                    ]
                },
                {
                    "name": "AccessRevoked",
                    "type": "event",
                    "inputs": [
                        {"name": "user", "type": "address", "indexed": True},
                        {"name": "thirdParty", "type": "address", "indexed": True}
                    ]
                },
                {
                    "name": "ZKProofVerified",
                    "type": "event",
                    "inputs": [
                        {"name": "user", "type": "address", "indexed": True},
                        {"name": "verifier", "type": "address", "indexed": True},
                        {"name": "dataType", "type": "bytes32", "indexed": False}
                    ]
                }
            ]
    
    def _deploy_contract(self) -> MockContract:
        """
        Deploy a new contract to the mock blockchain
        
        Returns:
            The deployed contract instance
        """
        # Use first account as deployer
        deployer_address = next(iter(mock_blockchain.accounts.keys()))
        
        # Deploy the contract
        contract = mock_blockchain.deploy_contract(
            name="IdentityVerification",
            abi=self.abi,
            from_address=deployer_address
        )
        
        return contract
    
    def create_identity(self, owner_address: str, from_address: str) -> Dict[str, Any]:
        """
        Create a new identity for an owner
        
        Args:
            owner_address: Address of the identity owner
            from_address: Address sending the transaction
            
        Returns:
            Transaction receipt
        """
        # Check if identity already exists
        if owner_address in self.identity_records:
            raise ValueError(f"Identity already exists for {owner_address}")
            
        # Create identity record
        self.identity_records[owner_address] = {
            "created_at": int(time.time()),
            "verification_types": {},
            "third_party_access": {}
        }
        
        # Create transaction
        tx = mock_blockchain.create_transaction(
            from_address=from_address,
            to_address=self.contract.address,
            function_name="createIdentity",
            data={"owner": owner_address}
        )
        
        # Update the block with this transaction
        mock_blockchain.mine_block()
        
        # Emit event
        self._emit_event(
            "IdentityCreated",
            {"owner": owner_address},
            tx.hash
        )
        
        # Save state on important operations
        if storage_manager.auto_save_enabled():
            threading.Thread(target=self.save_state, daemon=True).start()
        
        return mock_blockchain.get_transaction_receipt(tx.hash)
    
    def update_verification(self, owner_address: str, verification_type: int, 
                           status: int, from_address: str) -> Dict[str, Any]:
        """
        Update verification status for an identity
        
        Args:
            owner_address: Address of the identity owner
            verification_type: Type of verification (0=GovernmentID, 1=Biometric, 2=Address)
            status: Verification status (0=Pending, 1=Verified, 2=Rejected)
            from_address: Address sending the transaction
            
        Returns:
            Transaction receipt
        """
        # Create identity if it doesn't exist
        if owner_address not in self.identity_records:
            self.create_identity(owner_address, from_address)
            
        # Update verification status
        if owner_address not in self.verification_records:
            self.verification_records[owner_address] = {}
            
        self.verification_records[owner_address][verification_type] = status
        
        # Create transaction
        tx = mock_blockchain.create_transaction(
            from_address=from_address,
            to_address=self.contract.address,
            function_name="updateVerification",
            data={
                "owner": owner_address,
                "verificationType": verification_type,
                "status": status
            }
        )
        
        # Update the block with this transaction
        mock_blockchain.mine_block()
        
        # Emit event
        self._emit_event(
            "VerificationUpdated",
            {
                "owner": owner_address,
                "verificationType": verification_type,
                "status": status
            },
            tx.hash
        )
        
        # Save state on important operations
        if storage_manager.auto_save_enabled():
            threading.Thread(target=self.save_state, daemon=True).start()
        
        return mock_blockchain.get_transaction_receipt(tx.hash)
    
    def get_verification_status(self, owner_address: str, verification_type: int) -> int:
        """
        Get verification status for an identity
        
        Args:
            owner_address: Address of the identity owner
            verification_type: Type of verification to check
            
        Returns:
            Verification status (0=Pending, 1=Verified, 2=Rejected)
        """
        # If identity doesn't exist or verification not set, return Pending (0)
        if (owner_address not in self.verification_records or
            verification_type not in self.verification_records[owner_address]):
            return 0
            
        return self.verification_records[owner_address][verification_type]
    
    def grant_access(self, owner_address: str, third_party_address: str, 
                    expiry_timestamp: int, data_types: List[str], 
                    from_address: str) -> Dict[str, Any]:
        """
        Grant access to a third party
        
        Args:
            owner_address: Address of the identity owner
            third_party_address: Address of the third party
            expiry_timestamp: Timestamp when access expires
            data_types: List of data types to grant access to
            from_address: Address sending the transaction (must be owner)
            
        Returns:
            Transaction receipt
        """
        # Check that sender is the owner
        if from_address != owner_address:
            raise ValueError("Only the identity owner can grant access")
            
        # Create identity if it doesn't exist
        if owner_address not in self.identity_records:
            self.create_identity(owner_address, from_address)
            
        # Initialize access grants for this owner if not exists
        if owner_address not in self.access_grants:
            self.access_grants[owner_address] = {}
            
        # Update access grant
        self.access_grants[owner_address][third_party_address] = {
            "expiry_timestamp": expiry_timestamp,
            "data_types": data_types,
            "granted_at": int(time.time()),
            "revoked": False
        }
        
        # Create transaction
        tx = mock_blockchain.create_transaction(
            from_address=from_address,
            to_address=self.contract.address,
            function_name="grantAccess",
            data={
                "thirdParty": third_party_address,
                "expiryTimestamp": expiry_timestamp,
                "dataTypes": data_types
            }
        )
        
        # Update the block with this transaction
        mock_blockchain.mine_block()
        
        # Emit event
        self._emit_event(
            "AccessGranted",
            {
                "user": owner_address,
                "thirdParty": third_party_address,
                "expiryTimestamp": expiry_timestamp
            },
            tx.hash
        )
        
        # Save state on important operations
        if storage_manager.auto_save_enabled():
            threading.Thread(target=self.save_state, daemon=True).start()
        
        return mock_blockchain.get_transaction_receipt(tx.hash)
    
    def revoke_access(self, owner_address: str, third_party_address: str, 
                     from_address: str) -> Dict[str, Any]:
        """
        Revoke access from a third party
        
        Args:
            owner_address: Address of the identity owner
            third_party_address: Address of the third party
            from_address: Address sending the transaction (must be owner)
            
        Returns:
            Transaction receipt
        """
        # Check that sender is the owner
        if from_address != owner_address:
            raise ValueError("Only the identity owner can revoke access")
            
        # Check if access exists
        if (owner_address not in self.access_grants or 
            third_party_address not in self.access_grants[owner_address]):
            raise ValueError("No access found to revoke")
            
        # Mark access as revoked
        self.access_grants[owner_address][third_party_address]["revoked"] = True
        self.access_grants[owner_address][third_party_address]["revoked_at"] = int(time.time())
        
        # Create transaction
        tx = mock_blockchain.create_transaction(
            from_address=from_address,
            to_address=self.contract.address,
            function_name="revokeAccess",
            data={"thirdParty": third_party_address}
        )
        
        # Update the block with this transaction
        mock_blockchain.mine_block()
        
        # Emit event
        self._emit_event(
            "AccessRevoked",
            {
                "user": owner_address,
                "thirdParty": third_party_address
            },
            tx.hash
        )
        
        # Save state on important operations
        if storage_manager.auto_save_enabled():
            threading.Thread(target=self.save_state, daemon=True).start()
        
        return mock_blockchain.get_transaction_receipt(tx.hash)
    
    def check_access(self, third_party_address: str, owner_address: str) -> bool:
        """
        Check if a third party has access to an identity
        
        Args:
            third_party_address: Address of the third party
            owner_address: Address of the identity owner
            
        Returns:
            True if access is granted and not expired
        """
        # Check if access exists
        if (owner_address not in self.access_grants or 
            third_party_address not in self.access_grants[owner_address]):
            return False
            
        access = self.access_grants[owner_address][third_party_address]
        
        # Check if access has been revoked
        if access["revoked"]:
            return False
            
        # Check if access has expired
        if access["expiry_timestamp"] < int(time.time()):
            return False
            
        return True
    
    def record_zkp_verification(self, owner_address: str, proof_hash: str, 
                               data_type: str, from_address: str) -> Dict[str, Any]:
        """
        Record a zero-knowledge proof verification
        
        Args:
            owner_address: Address of the identity owner
            proof_hash: Hash of the zero-knowledge proof
            data_type: Type of data that was verified
            from_address: Address sending the transaction (verifier)
            
        Returns:
            Transaction receipt
        """
        # Check if verifier has access
        if not self.check_access(from_address, owner_address):
            raise ValueError("Verifier does not have access to the identity")
            
        # Create ZKP verification record
        verification = {
            "user": owner_address,
            "verifier": from_address,
            "proof_hash": proof_hash,
            "data_type": data_type,
            "timestamp": int(time.time())
        }
        
        self.zkp_verifications.append(verification)
        
        # Create transaction
        tx = mock_blockchain.create_transaction(
            from_address=from_address,
            to_address=self.contract.address,
            function_name="recordZKProofVerification",
            data={
                "user": owner_address,
                "proofHash": proof_hash,
                "dataType": data_type
            }
        )
        
        # Update the block with this transaction
        mock_blockchain.mine_block()
        
        # Emit event
        self._emit_event(
            "ZKProofVerified",
            {
                "user": owner_address,
                "verifier": from_address,
                "dataType": data_type
            },
            tx.hash
        )
        
        # Save state on important operations
        if storage_manager.auto_save_enabled():
            threading.Thread(target=self.save_state, daemon=True).start()
        
        return mock_blockchain.get_transaction_receipt(tx.hash)
    
    def _emit_event(self, event_name: str, args: Dict[str, Any], transaction_hash: str) -> None:
        """
        Emit an event to the mock blockchain
        
        Args:
            event_name: Name of the event
            args: Event arguments
            transaction_hash: Hash of the transaction that triggered the event
        """
        # Find latest block
        block_number = mock_blockchain.chain[-1].block_number
        
        # Create the event in the contract
        self.contract.emit_event(
            event_name=event_name,
            args=args,
            transaction_hash=transaction_hash,
            block_number=block_number
        )
    
    def get_past_events(self, event_name: str, 
                       from_block: int = 0, 
                       to_block: Optional[int] = None,
                       filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Get past events from the contract
        
        Args:
            event_name: Name of the event to filter by
            from_block: Start block (inclusive)
            to_block: End block (inclusive), defaults to latest
            filters: Argument filters
            
        Returns:
            List of matching events
        """
        events = self.contract.get_past_events(
            event_name=event_name,
            from_block=from_block,
            to_block=to_block,
            filters=filters
        )
        
        return [e.to_dict() for e in events]


# Create a singleton instance of the contract
identity_contract = IdentityVerificationContract() 