"""
Blockchain module for identity verification.
This module provides mock blockchain implementations for development and testing.
"""

# Import main components
from .contracts.MockBlockchain import mock_blockchain
from .contracts.IdentityVerification import identity_contract

# Export the core instances
__all__ = ['mock_blockchain', 'identity_contract'] 