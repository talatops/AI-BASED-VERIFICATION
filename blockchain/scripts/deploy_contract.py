#!/usr/bin/env python3
"""
Script to compile and deploy the Identity Verification smart contract.
"""

import os
import json
import sys
from web3 import Web3
from solcx import compile_source, install_solc

# Install solc compiler if not already installed
def install_compiler():
    try:
        install_solc(version='0.8.0')
        print("Solidity compiler 0.8.0 installed.")
    except Exception as e:
        print(f"Error installing Solidity compiler: {e}")
        sys.exit(1)

# Compile the smart contract
def compile_contract(contract_source_path):
    with open(contract_source_path, 'r') as file:
        source = file.read()
    
    compiled_sol = compile_source(
        source,
        output_values=['abi', 'bin'],
        solc_version='0.8.0'
    )
    
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface

# Deploy the smart contract
def deploy_contract(w3, contract_interface, account_address):
    # Create contract
    IdentityVerification = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    # Build constructor transaction
    construct_txn = IdentityVerification.constructor().build_transaction({
        'from': account_address,
        'nonce': w3.eth.get_transaction_count(account_address),
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })
    
    # Sign the transaction
    private_key = os.getenv('PRIVATE_KEY', None)
    if private_key:
        signed_txn = w3.eth.account.sign_transaction(construct_txn, private_key=private_key)
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction hash: {tx_hash.hex()}")
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt['status'] == 1:
            print(f"Contract deployed at address: {tx_receipt['contractAddress']}")
            return tx_receipt['contractAddress']
        else:
            print("Transaction failed.")
            return None
    else:
        # For development with ganache, we'll use the unlocked account
        tx_hash = w3.eth.send_transaction(construct_txn)
        print(f"Transaction hash: {tx_hash.hex()}")
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt['status'] == 1:
            print(f"Contract deployed at address: {tx_receipt['contractAddress']}")
            return tx_receipt['contractAddress']
        else:
            print("Transaction failed.")
            return None

# Save contract information for later use
def save_contract_info(contract_address, contract_interface):
    contract_data = {
        'address': contract_address,
        'abi': contract_interface['abi']
    }
    
    os.makedirs(os.path.dirname('../data/'), exist_ok=True)
    with open('../data/identity_verification_contract.json', 'w') as file:
        json.dump(contract_data, file, indent=2)
    
    print("Contract information saved to data/identity_verification_contract.json")

def main():
    # Connect to blockchain
    blockchain_node_url = os.getenv('BLOCKCHAIN_NODE_URL', 'http://ganache:8545')
    w3 = Web3(Web3.HTTPProvider(blockchain_node_url))
    
    if not w3.is_connected():
        print(f"Failed to connect to Ethereum node at {blockchain_node_url}")
        sys.exit(1)
    
    print(f"Connected to Ethereum node at {blockchain_node_url}")
    
    # Get account to deploy from
    account_address = w3.eth.accounts[0]  # Use the first account for development
    print(f"Deploying from account: {account_address}")
    
    # Install Solidity compiler
    install_compiler()
    
    # Compile contract
    contract_path = os.path.join(os.path.dirname(__file__), '..', 'contracts', 'IdentityVerification.sol')
    contract_interface = compile_contract(contract_path)
    
    # Deploy contract
    contract_address = deploy_contract(w3, contract_interface, account_address)
    
    if contract_address:
        # Save contract information
        save_contract_info(contract_address, contract_interface)
    
    return contract_address

if __name__ == "__main__":
    main()