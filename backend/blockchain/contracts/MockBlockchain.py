"""
Mock Blockchain for local development and testing.
Simulates a basic blockchain with blocks, transactions, and events without requiring gas or real transactions.
"""

import time
import hashlib
import json
import uuid
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..storage import storage_manager

logger = logging.getLogger(__name__)


class Block:
    """Represents a block in the mock blockchain"""
    
    def __init__(self, block_number: int, previous_hash: str):
        self.block_number = block_number
        self.timestamp = int(time.time())
        self.transactions = []
        self.previous_hash = previous_hash
        self.hash = self._calculate_hash()
        
    def _calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_string = f"{self.block_number}{self.timestamp}{self.previous_hash}{len(self.transactions)}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_transaction(self, transaction: Dict[str, Any]) -> None:
        """Add a transaction to the block"""
        self.transactions.append(transaction)
        # Recalculate hash after adding a transaction
        self.hash = self._calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary for serialization"""
        return {
            "block_number": self.block_number,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions
        }


class Transaction:
    """Represents a transaction in the mock blockchain"""
    
    def __init__(self, 
                 from_address: str, 
                 to_address: str, 
                 data: Dict[str, Any], 
                 function_name: str):
        self.from_address = from_address
        self.to_address = to_address
        self.data = data
        self.function_name = function_name
        self.timestamp = int(time.time())
        self.hash = self._generate_hash()
        self.receipt = None
        
    def _generate_hash(self) -> str:
        """Generate a unique hash for this transaction"""
        tx_string = f"{self.from_address}{self.to_address}{str(self.data)}{self.timestamp}{uuid.uuid4()}"
        return "0x" + hashlib.sha256(tx_string.encode()).hexdigest()
    
    def execute(self) -> Dict[str, Any]:
        """Execute the transaction and get a receipt"""
        # In a real blockchain, execution would involve running code on the EVM
        # Here we just simulate success
        self.receipt = {
            "transaction_hash": self.hash,
            "from": self.from_address,
            "to": self.to_address,
            "block_number": None,  # Will be filled when added to a block
            "timestamp": self.timestamp,
            "status": 1,  # 1 = success
            "gas_used": 21000 + len(str(self.data)) * 100,  # Mock gas calculation
            "function_name": self.function_name
        }
        return self.receipt
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary for serialization"""
        return {
            "hash": self.hash,
            "from": self.from_address,
            "to": self.to_address,
            "data": self.data,
            "function_name": self.function_name,
            "timestamp": self.timestamp,
            "receipt": self.receipt
        }


class Event:
    """Represents an event emitted during transaction execution"""
    
    def __init__(self, 
                 name: str, 
                 args: Dict[str, Any], 
                 transaction_hash: str,
                 block_number: int,
                 address: str):
        self.name = name
        self.args = args
        self.transaction_hash = transaction_hash
        self.block_number = block_number
        self.log_index = 0  # Will be set when added to the logs
        self.address = address  # Contract address that emitted the event
        self.timestamp = int(time.time())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization"""
        return {
            "name": self.name,
            "args": self.args,
            "transaction_hash": self.transaction_hash,
            "block_number": self.block_number,
            "log_index": self.log_index,
            "address": self.address,
            "timestamp": self.timestamp
        }


class MockContract:
    """Simulates a smart contract on the blockchain"""
    
    def __init__(self, address: str, name: str, abi: List[Dict[str, Any]]):
        self.address = address
        self.name = name
        self.abi = abi
        self.storage = {}  # Contract state storage
        self.events = []  # Events emitted by this contract
        
    def call(self, function_name: str, args: Dict[str, Any]) -> Any:
        """
        Simulate a read-only call to the contract
        
        Args:
            function_name: Name of the function to call
            args: Arguments to pass to the function
            
        Returns:
            Simulated result of the function call
        """
        # In a real contract, this would execute EVM code
        # Here we just simulate basic functions
        
        # Generate a key based on function and args
        key = f"{function_name}:{json.dumps(args, sort_keys=True)}"
        
        # Return from storage if we've seen this call before
        if key in self.storage:
            return self.storage[key]
        
        # Default values for common functions
        if function_name == "balanceOf":
            return 100  # Default balance is 100 tokens
        elif function_name == "ownerOf":
            return args.get("tokenId", 0) % 10  # Simple mapping of token to owner
        elif function_name == "totalSupply":
            return 1000  # Default total supply
        elif function_name.startswith("get"):
            # For getter functions, return a simple value
            return "MockValue"
        
        # For unknown functions, return None
        return None
    
    def transact(self, function_name: str, args: Dict[str, Any], from_address: str) -> Transaction:
        """
        Simulate a transaction to the contract
        
        Args:
            function_name: Name of the function to call
            args: Arguments to pass to the function
            from_address: Address sending the transaction
            
        Returns:
            Transaction object
        """
        # Create a transaction
        tx = Transaction(
            from_address=from_address,
            to_address=self.address,
            data=args,
            function_name=function_name
        )
        
        # Execute transaction
        tx.execute()
        
        # Update contract storage
        key = f"{function_name}:{json.dumps(args, sort_keys=True)}"
        self.storage[key] = True  # Mark this call as executed
        
        return tx
    
    def emit_event(self, event_name: str, args: Dict[str, Any], transaction_hash: str, block_number: int) -> Event:
        """
        Emit an event from the contract
        
        Args:
            event_name: Name of the event
            args: Event arguments
            transaction_hash: Hash of the transaction that caused the event
            block_number: Block number where the event was emitted
            
        Returns:
            Event object
        """
        event = Event(
            name=event_name,
            args=args,
            transaction_hash=transaction_hash,
            block_number=block_number,
            address=self.address
        )
        
        # Set log index based on number of events
        event.log_index = len(self.events)
        
        # Add to events list
        self.events.append(event)
        
        return event
    
    def get_past_events(self, event_name: str, from_block: int = 0, to_block: Optional[int] = None, 
                        filters: Dict[str, Any] = None) -> List[Event]:
        """
        Get past events emitted by the contract
        
        Args:
            event_name: Name of the event to filter by
            from_block: Start block (inclusive)
            to_block: End block (inclusive), defaults to latest
            filters: Argument filters
            
        Returns:
            List of matching events
        """
        matching_events = []
        
        for event in self.events:
            # Skip if event name doesn't match
            if event.name != event_name:
                continue
                
            # Skip if block is before from_block
            if event.block_number < from_block:
                continue
                
            # Skip if block is after to_block
            if to_block is not None and event.block_number > to_block:
                continue
                
            # Check filters if provided
            if filters:
                match = True
                for key, value in filters.items():
                    if key not in event.args or event.args[key] != value:
                        match = False
                        break
                        
                if not match:
                    continue
                    
            # If we reach here, event matches all criteria
            matching_events.append(event)
            
        return matching_events


class MockBlockchain:
    """Mock implementation of a blockchain for testing and development"""
    
    def __init__(self):
        # Initialize chain with genesis block
        self.chain = [Block(0, "0" * 64)]
        self.pending_transactions = []
        self.contracts = {}  # address -> contract mapping
        self.accounts = {}  # address -> balance mapping
        self.nonces = {}  # address -> nonce mapping
        self.events = []  # All events across all contracts
        
        # Set default accounts
        for i in range(10):
            address = f"0x{i:040x}"
            self.accounts[address] = 100 * (10 ** 18)  # 100 ETH in wei
            self.nonces[address] = 0
            
        # Try to load state from storage
        self._load_state()
        
        # Set up auto-save if enabled
        if storage_manager.auto_save_enabled():
            self._setup_auto_save()
            
        logger.info("MockBlockchain initialized")
    
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
        
        logger.info(f"Auto-save enabled with interval of {interval} seconds")
    
    def _load_state(self):
        """Load blockchain state from storage"""
        state = storage_manager.load_blockchain_state()
        if state:
            try:
                # Load blocks
                self.chain = []
                for block_data in state.get("blocks", []):
                    block = Block(
                        block_number=block_data["block_number"],
                        previous_hash=block_data["previous_hash"]
                    )
                    block.timestamp = block_data["timestamp"]
                    block.hash = block_data["hash"]
                    block.transactions = block_data["transactions"]
                    self.chain.append(block)
                
                # Load accounts
                self.accounts = state.get("accounts", self.accounts)
                
                # Load nonces
                self.nonces = state.get("nonces", self.nonces)
                
                # Contracts will be re-populated by the contract objects
                
                logger.info(f"Loaded blockchain state with {len(self.chain)} blocks")
                return True
            except Exception as e:
                logger.error(f"Error loading blockchain state: {e}")
                return False
        return False
    
    def save_state(self):
        """Save blockchain state to storage"""
        try:
            # Convert blockchain state to dictionary
            state = self.to_dict()
            
            # Save to storage
            success = storage_manager.save_blockchain_state(state)
            
            if success:
                logger.info("Blockchain state saved successfully")
            else:
                logger.warning("Failed to save blockchain state")
                
            return success
        except Exception as e:
            logger.error(f"Error saving blockchain state: {e}")
            return False
    
    def deploy_contract(self, name: str, abi: List[Dict[str, Any]], from_address: str) -> MockContract:
        """
        Deploy a new contract to the blockchain
        
        Args:
            name: Name of the contract
            abi: Contract ABI
            from_address: Address deploying the contract
            
        Returns:
            Deployed contract instance
        """
        # Generate a deterministic contract address
        address_input = f"{name}{from_address}{len(self.contracts)}{uuid.uuid4()}"
        contract_address = "0x" + hashlib.sha256(address_input.encode()).hexdigest()[-40:]
        
        # Create the contract
        contract = MockContract(contract_address, name, abi)
        
        # Store the contract
        self.contracts[contract_address] = contract
        
        # Create deployment transaction
        tx = Transaction(
            from_address=from_address,
            to_address=None,  # Contract creation
            data={"contract_name": name},
            function_name="constructor"
        )
        
        # Execute transaction
        tx.execute()
        
        # Add to pending transactions
        self.pending_transactions.append(tx)
        
        # Mine block to include the transaction
        self.mine_block()
        
        return contract
    
    def get_contract(self, address: str) -> Optional[MockContract]:
        """Get a contract by address"""
        return self.contracts.get(address)
    
    def create_transaction(self, from_address: str, to_address: str, 
                         function_name: str, data: Dict[str, Any]) -> Transaction:
        """
        Create a new transaction
        
        Args:
            from_address: Sender address
            to_address: Recipient address
            function_name: Name of the function to call (if contract interaction)
            data: Transaction data or function arguments
            
        Returns:
            Created transaction
        """
        # Check sender has enough balance
        if self.accounts.get(from_address, 0) < 21000:  # Minimum gas
            raise ValueError(f"Insufficient balance for gas: {from_address}")
        
        # Create the transaction
        tx = Transaction(
            from_address=from_address,
            to_address=to_address,
            data=data,
            function_name=function_name
        )
        
        # Execute transaction
        tx.execute()
        
        # Update nonce
        self.nonces[from_address] = self.nonces.get(from_address, 0) + 1
        
        # Add to pending transactions
        self.pending_transactions.append(tx)
        
        return tx
    
    def mine_block(self) -> Block:
        """
        Mine a new block with pending transactions
        
        Returns:
            The newly mined block
        """
        # Get the last block
        last_block = self.chain[-1]
        
        # Create a new block
        new_block = Block(last_block.block_number + 1, last_block.hash)
        
        # Add pending transactions to the block
        for tx in self.pending_transactions:
            new_block.add_transaction(tx.to_dict())
            
            # Update transaction receipt with block number
            if tx.receipt:
                tx.receipt["block_number"] = new_block.block_number
            
            # If transaction is to a contract, allow it to emit events
            if tx.to_address in self.contracts:
                contract = self.contracts[tx.to_address]
                
                # Let the contract emit an event based on the function called
                event_name = f"{tx.function_name}Event"
                event = contract.emit_event(
                    event_name=event_name,
                    args=tx.data,
                    transaction_hash=tx.hash,
                    block_number=new_block.block_number
                )
                
                # Add to global events list
                self.events.append(event)
        
        # Add the block to the chain
        self.chain.append(new_block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        # Save state if enabled
        if storage_manager.auto_save_enabled():
            # Don't wait for save to complete
            threading.Thread(target=self.save_state, daemon=True).start()
        
        return new_block
    
    def get_balance(self, address: str) -> int:
        """Get balance of an address"""
        return self.accounts.get(address, 0)
    
    def get_transaction_count(self, address: str) -> int:
        """Get transaction count (nonce) for an address"""
        return self.nonces.get(address, 0)
    
    def get_block(self, block_identifier: Any) -> Optional[Dict[str, Any]]:
        """
        Get a block by number or hash
        
        Args:
            block_identifier: Block number or 'latest'
            
        Returns:
            Block data as dictionary
        """
        if block_identifier == 'latest':
            return self.chain[-1].to_dict()
        
        if isinstance(block_identifier, int):
            for block in self.chain:
                if block.block_number == block_identifier:
                    return block.to_dict()
        
        # If block_identifier is a hash
        for block in self.chain:
            if block.hash == block_identifier:
                return block.to_dict()
                
        return None
    
    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get transaction receipt by hash
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction receipt as dictionary
        """
        # Search for transaction in all blocks
        for block in self.chain:
            for tx_dict in block.transactions:
                if tx_dict.get("hash") == tx_hash:
                    return {
                        **tx_dict.get("receipt", {}),
                        "block_hash": block.hash
                    }
        
        return None
    
    def get_logs(self, from_block: int = 0, to_block: Optional[int] = None, 
                address: Optional[str] = None, topics: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get logs (events) from the blockchain
        
        Args:
            from_block: Start block (inclusive)
            to_block: End block (inclusive), defaults to latest
            address: Contract address to filter by
            topics: Event topics to filter by
            
        Returns:
            List of matching logs
        """
        if to_block is None:
            to_block = self.chain[-1].block_number
        
        matching_logs = []
        
        for event in self.events:
            # Skip if block is before from_block
            if event.block_number < from_block:
                continue
                
            # Skip if block is after to_block
            if event.block_number > to_block:
                continue
                
            # Skip if address doesn't match
            if address and event.address != address:
                continue
                
            # TODO: Topic filtering if needed
                
            # If we reach here, event matches all criteria
            matching_logs.append(event.to_dict())
            
        return matching_logs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert blockchain state to dictionary for serialization"""
        return {
            "blocks": [block.to_dict() for block in self.chain],
            "pending_transactions": [tx.to_dict() for tx in self.pending_transactions],
            "contracts": {addr: {"address": addr, "name": contract.name} 
                          for addr, contract in self.contracts.items()},
            "accounts": self.accounts,
            "nonces": self.nonces
        }


# Create a singleton instance
mock_blockchain = MockBlockchain() 