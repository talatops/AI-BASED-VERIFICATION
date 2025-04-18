from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BlockchainAddress(BaseModel):
    address: str
    network: str
    created_at: str
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "address": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
                "network": "ganache",
                "created_at": "2023-10-26T12:00:00"
            }
        }

class Transaction(BaseModel):
    id: str
    type: str
    timestamp: str
    status: str
    tx_hash: str
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "tx1",
                "type": "Identity Verification",
                "timestamp": "2023-10-26T12:00:00",
                "status": "confirmed",
                "tx_hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            }
        }

class ZKProof(BaseModel):
    proof: str
    data_type: str
    claim: str
    verified: bool
    timestamp: str
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "proof": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                "data_type": "age",
                "claim": "over_18",
                "verified": True,
                "timestamp": "2023-10-26T12:00:00"
            }
        } 