from fastapi import APIRouter, HTTPException, Depends, Response, status, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field, validator
import logging
import json
import time
from datetime import datetime
import uuid

from services.encryption_service import encryption_service

logger = logging.getLogger(__name__)

# Define router
encryption_router = APIRouter(
    prefix="/encryption",
    tags=["encryption"],
    responses={404: {"description": "Not found"}},
)

# Request and response models
class EncryptRequest(BaseModel):
    plaintext: str
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "plaintext": "sensitive data to encrypt",
                "metadata": {"purpose": "user profile", "data_type": "personal"}
            }
        }

class BulkEncryptRequest(BaseModel):
    items: List[str]
    format_preserving: Optional[bool] = False
    
    class Config:
        schema_extra = {
            "example": {
                "items": ["value1", "value2", "value3"],
                "format_preserving": False
            }
        }

class DecryptRequest(BaseModel):
    ciphertext: str
    
    class Config:
        schema_extra = {
            "example": {
                "ciphertext": "encrypted_data_string"
            }
        }

class HomomorphicEncryptRequest(BaseModel):
    value: str
    
    class Config:
        schema_extra = {
            "example": {
                "value": "42.5"
            }
        }

class HomomorphicComputeRequest(BaseModel):
    encrypted_values: List[str]
    operation: str = Field(..., description="Operation to perform (sum, average, min, max)")
    
    @validator('operation')
    def validate_operation(cls, v):
        valid_ops = ['sum', 'average', 'min', 'max']
        if v not in valid_ops:
            raise ValueError(f"Operation must be one of {valid_ops}")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "encrypted_values": ["HE_encrypted1", "HE_encrypted2"],
                "operation": "sum"
            }
        }

class KeyRotationRequest(BaseModel):
    force: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "force": True
            }
        }

class AnonymizeRequest(BaseModel):
    data: str
    data_type: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "data": "john.doe@example.com",
                "data_type": "email"
            }
        }

# Endpoints
@encryption_router.post("/encrypt", response_model=Dict[str, str])
async def encrypt_data(request: EncryptRequest):
    """
    Encrypt sensitive data using standard encryption with authentication.
    Returns a ciphertext that can be decrypted with the decrypt endpoint.
    """
    try:
        additional_data = None
        if request.metadata:
            additional_data = json.dumps(request.metadata).encode('utf-8')
            
        encrypted = encryption_service.encrypt(request.plaintext, additional_data)
        
        return {
            "ciphertext": encrypted,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to encrypt data: {str(e)}"
        )

@encryption_router.post("/bulk-encrypt", response_model=Dict[str, Any])
async def bulk_encrypt(request: BulkEncryptRequest):
    """
    Encrypt multiple items at once.
    Optionally use format-preserving encryption to maintain the data format.
    """
    try:
        start_time = time.time()
        results = []
        
        encrypt_method = encryption_service.format_preserving_encrypt if request.format_preserving else encryption_service.encrypt
        
        for item in request.items:
            encrypted = encrypt_method(item)
            results.append(encrypted)
        
        processing_time = time.time() - start_time
        
        return {
            "encrypted_items": results,
            "count": len(results),
            "format_preserving": request.format_preserving,
            "processing_time_ms": round(processing_time * 1000, 2),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Bulk encryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to encrypt items: {str(e)}"
        )

@encryption_router.post("/decrypt", response_model=Dict[str, str])
async def decrypt_data(request: DecryptRequest):
    """
    Decrypt data that was encrypted using the standard encryption endpoint.
    """
    try:
        decrypted = encryption_service.decrypt(request.ciphertext)
        
        return {
            "plaintext": decrypted,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to decrypt data: {str(e)}"
        )

@encryption_router.post("/homomorphic/encrypt", response_model=Dict[str, str])
async def homomorphic_encrypt(request: HomomorphicEncryptRequest):
    """
    Encrypt data using homomorphic encryption to enable computation on encrypted data.
    """
    try:
        encrypted = encryption_service.homomorphic_encrypt(request.value)
        
        return {
            "encrypted_value": encrypted,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Homomorphic encryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to homomorphically encrypt data: {str(e)}"
        )

@encryption_router.post("/homomorphic/compute", response_model=Dict[str, Any])
async def homomorphic_compute(request: HomomorphicComputeRequest):
    """
    Perform computation on homomorphically encrypted values.
    Supports sum, average, min, and max operations.
    """
    try:
        result = encryption_service.homomorphic_compute(
            request.encrypted_values, 
            request.operation
        )
        
        # Check if result is still encrypted (for sum operation)
        is_encrypted = isinstance(result, str) and result.startswith("HE_")
        
        return {
            "result": result,
            "is_encrypted": is_encrypted,
            "operation": request.operation,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Homomorphic computation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute on encrypted data: {str(e)}"
        )

@encryption_router.post("/homomorphic/decrypt", response_model=Dict[str, str])
async def homomorphic_decrypt(request: DecryptRequest):
    """
    Decrypt homomorphically encrypted data.
    """
    try:
        if not request.ciphertext.startswith("HE_"):
            raise ValueError("Not a homomorphically encrypted value")
            
        decrypted = encryption_service.homomorphic_decrypt(request.ciphertext)
        
        return {
            "plaintext": decrypted,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Homomorphic decryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to decrypt homomorphically encrypted data: {str(e)}"
        )

@encryption_router.post("/anonymize", response_model=Dict[str, str])
async def anonymize_data(request: AnonymizeRequest):
    """
    Anonymize sensitive data based on its type.
    Supports email, phone, name, address, and auto-detection.
    """
    try:
        anonymized = encryption_service.anonymize(request.data, request.data_type)
        
        return {
            "anonymized_data": anonymized,
            "data_type": request.data_type or "auto-detected",
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Anonymization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to anonymize data: {str(e)}"
        )

@encryption_router.post("/rotate-keys", response_model=Dict[str, Any])
async def rotate_encryption_keys(request: KeyRotationRequest, background_tasks: BackgroundTasks):
    """
    Rotate encryption keys for improved security.
    Can be forced or will follow the configured rotation schedule.
    """
    try:
        # If force is True, set last rotation to a date far in the past
        if request.force:
            encryption_service.last_rotation = datetime.min
            
        # Schedule key rotation in background
        background_tasks.add_task(encryption_service.rotate_keys)
        
        return {
            "message": "Key rotation scheduled" + (" (forced)" if request.force else ""),
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Key rotation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to schedule key rotation: {str(e)}"
        )

@encryption_router.get("/status", response_model=Dict[str, Any])
async def encryption_service_status():
    """
    Get current status of the encryption service, including key versions and last rotation.
    """
    try:
        return {
            "status": "active",
            "key_versions": encryption_service.key_versions,
            "last_key_rotation": encryption_service.last_rotation.isoformat(),
            "next_scheduled_rotation": (
                encryption_service.last_rotation + 
                encryption_service.key_rotation_interval
            ).isoformat(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve encryption service status: {str(e)}"
        ) 