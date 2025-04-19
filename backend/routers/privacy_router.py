"""
Router for privacy-related endpoints including homomorphic encryption and GDPR compliance.
"""

from fastapi import APIRouter, HTTPException, Request, Body, Query, Path, Depends, status, BackgroundTasks
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
import logging
from datetime import datetime, timedelta
import json
from enum import Enum
import hashlib
import uuid
import re
import binascii
import os

from services.encryption_service import encryption_service, EncryptionService
from services.blockchain_service import blockchain_service
from services.homomorphic_encryption_service import HomomorphicEncryptionService
from services.gdpr_compliance_service import GDPRComplianceService, RequestType, RequestStatus

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/privacy",
    tags=["privacy"],
    responses={404: {"description": "Not found"}}
)

# Define models
class EncryptRequest(BaseModel):
    user_id: Optional[str] = None
    value: Optional[float] = None
    data: Optional[Dict[str, Any]] = None
    purpose: Optional[str] = None
    
class EncryptValueRequest(BaseModel):
    value: float
    
class DecryptValueRequest(BaseModel):
    encrypted_value: str
    
class ComputeRequest(BaseModel):
    encrypted_value1: str
    encrypted_value2: str
    operation: str
    
class BulkEncryptRequest(BaseModel):
    user_id: str
    values: List[float]

class UserDataRequest(BaseModel):
    user_id: str
    data: Dict[str, Any]
    fields_to_encrypt: List[str] = Field(..., description="List of fields to encrypt")
    
class PrivacyComputationRequest(BaseModel):
    user_id: str
    operation: str = Field(..., description="Type of computation: 'sum', 'average', 'comparison'") 
    encrypted_value_ids: List[str] = Field(..., description="IDs of encrypted values to use in computation")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional parameters for the computation")

class DataMaskRequest(BaseModel):
    user_id: str
    data: Dict[str, Any]
    fields_to_share: List[str]
    mask_type: str = Field("hash", description="Type of masking (hash, tokenize, partial)")
    
class GDPRRequest(BaseModel):
    user_id: str
    request_type: str = Field(..., description="Type of GDPR request: 'access', 'delete', 'export'")

class ConsentRequest(BaseModel):
    purpose: str = Field(..., description="Purpose of data processing")
    data_categories: List[str] = Field(..., description="Categories of data being processed")
    third_parties: Optional[List[str]] = Field(None, description="Third parties data may be shared with")

class ConsentResponse(BaseModel):
    consent_id: str
    user_id: str
    purpose: str
    data_categories: List[str]
    third_parties: List[str]
    granted_at: str
    expires_at: str
    status: str

class RequestTypeEnum(str, Enum):
    ACCESS = "access"
    RECTIFICATION = "rectification"
    ERASURE = "erasure"
    RESTRICTION = "restriction"
    PORTABILITY = "portability"
    OBJECT = "object"
    AUTOMATED = "automated"

class DSRRequest(BaseModel):
    request_type: RequestTypeEnum
    details: Optional[Dict[str, Any]] = None

class DSRResponse(BaseModel):
    request_id: str
    user_id: str
    type: str
    details: Dict[str, Any]
    status: str
    submitted_at: str
    updated_at: str
    due_by: str
    notes: List[Dict[str, Any]]

class DSRStatusUpdate(BaseModel):
    status: str
    note: Optional[str] = None

class RetentionPolicyUpdate(BaseModel):
    data_category: str
    retention_days: int

class AccessLogEntry(BaseModel):
    log_id: str
    user_id: str
    data_category: str
    purpose: str
    accessed_by: str
    access_type: str
    timestamp: str
    ip_address: str

class PrivacyReport(BaseModel):
    user_id: str
    generated_at: str
    active_consents: List[Dict[str, Any]]
    withdrawn_consents: List[Dict[str, Any]]
    open_requests: List[Dict[str, Any]]
    completed_requests: List[Dict[str, Any]]
    recent_data_access: List[Dict[str, Any]]
    data_categories_accessed: List[str]
    third_parties_with_access: List[str]

class AnonymizeRequest(BaseModel):
    data: Dict[str, Any]
    sensitive_fields: List[str]

class RetentionPolicyRequest(BaseModel):
    data_category: str
    retention_days: int

# Cache for encrypted values with unique IDs
encrypted_values_cache = {}

# Cache for the homomorphic encryption demo
demo_encrypted_cache = {}

# Initialize services
encryption_service = HomomorphicEncryptionService()
gdpr_service = GDPRComplianceService()

# Homomorphic Encryption Demo Endpoints
@router.post("/encrypt", response_model=Dict[str, Any])
async def encrypt_value_demo(request: EncryptValueRequest):
    """
    Encrypt a single value for the homomorphic encryption demo.
    """
    try:
        # Mock an encrypted value with some formatting to make it look encrypted
        # In a real implementation, this would use actual homomorphic encryption
        value = float(request.value)
        mock_encrypted = f"HE_ENC(v={value})__{hash(str(value) + str(datetime.now()))}"
        
        # Store in the demo cache
        demo_encrypted_cache[mock_encrypted] = value
        
        return {
            "status": "success",
            "message": "Value encrypted successfully",
            "encrypted_value": mock_encrypted
        }
    except Exception as e:
        logger.error(f"Error in encrypt_value_demo: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to encrypt value: {str(e)}")

@router.post("/compute", response_model=Dict[str, Any])
async def compute_demo(request: ComputeRequest):
    """
    Perform a computation on encrypted values for the homomorphic encryption demo.
    """
    try:
        # Get values from cache or extract from strings if demo values
        value1 = demo_encrypted_cache.get(request.encrypted_value1)
        value2 = demo_encrypted_cache.get(request.encrypted_value2)
        
        if value1 is None or value2 is None:
            raise HTTPException(status_code=404, detail="One or more encrypted values not found")
        
        # Perform the operation
        result = None
        if request.operation == "add":
            result = value1 + value2
        elif request.operation == "subtract":
            result = value1 - value2
        elif request.operation == "multiply":
            result = value1 * value2
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported operation: {request.operation}")
        
        # Encrypt the result
        mock_encrypted_result = f"HE_ENC(result={result})__{hash(str(result) + str(datetime.now()))}"
        demo_encrypted_cache[mock_encrypted_result] = result
        
        return {
            "status": "success",
            "message": f"Computation '{request.operation}' performed successfully",
            "encrypted_result": mock_encrypted_result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in compute_demo: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to perform computation: {str(e)}")

@router.post("/decrypt", response_model=Dict[str, Any])
async def decrypt_value_demo(request: DecryptValueRequest):
    """
    Decrypt a value for the homomorphic encryption demo.
    """
    try:
        # Get the value from cache
        value = demo_encrypted_cache.get(request.encrypted_value)
        
        if value is None:
            raise HTTPException(status_code=404, detail="Encrypted value not found")
        
        return {
            "status": "success",
            "message": "Value decrypted successfully",
            "decrypted_value": value
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in decrypt_value_demo: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to decrypt value: {str(e)}")

# Original Data Encryption Endpoints
@router.post("/encrypt-value", response_model=Dict[str, Any])
async def encrypt_value(request: EncryptRequest):
    """
    Encrypt a single value using homomorphic encryption.
    Returns a unique ID for the encrypted value.
    """
    try:
        # Encrypt the value
        encrypted_value = encryption_service.encrypt_value(request.value)
        
        # Generate a unique ID
        value_id = f"{request.user_id}_{len(encrypted_values_cache) + 1}"
        
        # Store encrypted value in cache
        encrypted_values_cache[value_id] = encrypted_value
        
        # Return the ID
        return {
            "status": "success",
            "message": "Value encrypted successfully",
            "encrypted_value_id": value_id
        }
    except Exception as e:
        logger.error(f"Error in encrypt_value: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to encrypt value: {str(e)}")
    
@router.post("/encrypt-bulk", response_model=Dict[str, Any])
async def encrypt_bulk(request: BulkEncryptRequest):
    """
    Encrypt multiple values using homomorphic encryption.
    Returns unique IDs for the encrypted values.
    """
    try:
        value_ids = []
        
        # Encrypt each value
        for i, value in enumerate(request.values):
            encrypted_value = encryption_service.encrypt_value(value)
            
            # Generate a unique ID
            value_id = f"{request.user_id}_bulk_{i+1}"
            
            # Store encrypted value in cache
            encrypted_values_cache[value_id] = encrypted_value
            value_ids.append(value_id)
        
        # Return the IDs
        return {
            "status": "success",
            "message": f"Encrypted {len(request.values)} values successfully",
            "encrypted_value_ids": value_ids
        }
    except Exception as e:
        logger.error(f"Error in encrypt_bulk: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to encrypt values: {str(e)}")

@router.post("/privacy-computation", response_model=Dict[str, Any])
async def privacy_preserving_computation(request: PrivacyComputationRequest):
    """
    Perform privacy-preserving computation on encrypted values.
    """
    try:
        # Get encrypted values from cache
        encrypted_values = []
        for value_id in request.encrypted_value_ids:
            if value_id not in encrypted_values_cache:
                raise HTTPException(status_code=404, detail=f"Encrypted value with ID {value_id} not found")
            encrypted_values.append(encrypted_values_cache[value_id])
        
        # Perform computation
        result = encryption_service.privacy_preserving_computation(
            operation=request.operation,
            encrypted_values=encrypted_values,
            additional_params=request.parameters
        )
        
        return {
            "status": "success",
            "result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in privacy_preserving_computation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to perform computation: {str(e)}")

@router.post("/decrypt-value/{value_id}", response_model=Dict[str, Any])
async def decrypt_value(value_id: str, user_id: str = Query(...)):
    """
    Decrypt a value that was encrypted using homomorphic encryption.
    """
    try:
        # Check if value exists in cache
        if value_id not in encrypted_values_cache:
            raise HTTPException(status_code=404, detail=f"Encrypted value with ID {value_id} not found")
        
        # Get value from cache
        encrypted_value = encrypted_values_cache[value_id]
        
        # Check if user has permission (in a real app, this would be more robust)
        if not value_id.startswith(f"{user_id}_"):
            raise HTTPException(status_code=403, detail="User does not have permission to decrypt this value")
        
        # Decrypt value
        decrypted_value = encryption_service.decrypt_value(encrypted_value)
        
        return {
            "status": "success",
            "message": "Value decrypted successfully",
            "decrypted_value": decrypted_value
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in decrypt_value: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to decrypt value: {str(e)}")

@router.post("/encrypt-user-data", response_model=Dict[str, Any])
async def encrypt_user_data(request: UserDataRequest):
    """
    Encrypt user data using symmetric encryption for secure storage.
    """
    try:
        # Encrypt user data
        result = encryption_service.encrypt_user_data(
            user_id=request.user_id,
            data=request.data
        )
        
        return {
            "status": "success",
            "message": "User data encrypted successfully",
            "encrypted_data": result
        }
    except Exception as e:
        logger.error(f"Error in encrypt_user_data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to encrypt user data: {str(e)}")

@router.post("/data-mask", response_model=Dict[str, Any])
async def create_data_mask(request: DataMaskRequest):
    """
    Create a data mask for sharing only specific fields of user data with third parties.
    """
    try:
        # Filter the data to only include the fields to share
        masked_data = {k: request.data[k] for k in request.fields_to_share if k in request.data}
        
        # Record the access for audit purposes
        gdpr_service.record_data_access(
            user_id=request.user_id,
            data_category="masked_data",
            purpose="third_party_sharing",
            accessed_by="system",
            access_type="mask_creation"
        )
        
        return {
            "status": "success",
            "message": "Data mask created successfully",
            "masked_data": masked_data,
            "shared_fields": list(masked_data.keys())
        }
    except Exception as e:
        logger.error(f"Error in create_data_mask: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create data mask: {str(e)}")

@router.get("/gdpr-compliance", response_model=Dict[str, Any])
async def get_gdpr_compliance_info():
    """
    Get GDPR compliance information about the privacy services.
    """
    try:
        compliance_info = encryption_service.get_gdpr_compliance_info()
        
        return {
            "status": "success",
            "compliance_info": compliance_info
        }
    except Exception as e:
        logger.error(f"Error in get_gdpr_compliance_info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get GDPR compliance info: {str(e)}")

@router.post("/gdpr-request", response_model=Dict[str, Any])
async def handle_gdpr_request(request: GDPRRequest, background_tasks: BackgroundTasks):
    """
    Handle a GDPR-related request such as data access, deletion, or export.
    """
    try:
        if request.request_type == "access":
            # Get all data for the user
            user_data = {}  # In a real app, this would get data from multiple services
            
            return {
                "status": "success",
                "request_type": "access",
                "data": user_data
            }
            
        elif request.request_type == "delete":
            # Delete user data
            # In a real app, this would delete from multiple services and databases
            
            return {
                "status": "success",
                "request_type": "delete",
                "message": "User data deletion process initiated"
            }
            
        elif request.request_type == "export":
            # Export user data in a portable format
            user_data = {}  # In a real app, this would get data from multiple services
            
            return {
                "status": "success",
                "request_type": "export",
                "data": user_data,
                "format": "json"
            }
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported GDPR request type: {request.request_type}")
            
    except Exception as e:
        logger.error(f"Error in handle_gdpr_request: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process GDPR request: {str(e)}")

@router.post("/encrypt-data", response_model=Dict[str, Any])
async def encrypt_data(request: EncryptRequest):
    """
    Encrypt sensitive data using homomorphic encryption to allow processing without decryption
    """
    try:
        logger.info(f"Encrypting data for user {request.user_id} for purpose: {request.purpose}")
        encrypted_data, key_id = encryption_service.encrypt(
            request.user_id, 
            request.data, 
            request.purpose
        )
        return {
            "encrypted_data": encrypted_data,
            "key_id": key_id
        }
    except Exception as e:
        logger.error(f"Error encrypting data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to encrypt data: {str(e)}"
        )

@router.post("/decrypt-data", response_model=Dict[str, Any])
async def decrypt_data(request: EncryptRequest):
    """
    Decrypt previously encrypted data, requiring proper authorization
    """
    try:
        logger.info(f"Decrypting data for user {request.user_id}")
        # Check if purpose is authorized for this data
        if not gdpr_service.verify_purpose_authorization(request.user_id, request.purpose):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized purpose for data access"
            )
            
        decrypted_data = encryption_service.decrypt(
            request.user_id,
            request.data,
            request.purpose
        )
        return {
            "decrypted_data": decrypted_data
        }
    except Exception as e:
        logger.error(f"Error decrypting data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to decrypt data: {str(e)}"
        )

@router.post("/compute-encrypted", response_model=Dict[str, Any])
async def compute_on_encrypted_data(request: Dict[str, Any]):
    """
    Perform computation on encrypted data without decryption using homomorphic encryption
    """
    try:
        operation = request.get("operation")
        encrypted_values = request.get("encrypted_values", [])
        result = encryption_service.compute(operation, encrypted_values)
        return {"result": result}
    except Exception as e:
        logger.error(f"Error computing on encrypted data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform computation: {str(e)}"
        )

@router.post("/consent", response_model=ConsentResponse, tags=["privacy"])
async def record_consent(user_id: str, consent_data: ConsentRequest):
    """Record user consent for data processing"""
    try:
        result = gdpr_service.record_consent(
            user_id=user_id,
            purpose=consent_data.purpose,
            data_categories=consent_data.data_categories,
            third_parties=consent_data.third_parties
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/consent/{consent_id}", response_model=ConsentResponse, tags=["privacy"])
async def withdraw_consent(user_id: str, consent_id: str = Path(...)):
    """Withdraw a previously given consent"""
    try:
        result = gdpr_service.withdraw_consent(
            user_id=user_id,
            consent_id=consent_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consent", response_model=List[ConsentResponse], tags=["privacy"])
async def get_user_consents(user_id: str):
    """Get all consents for a user"""
    try:
        result = gdpr_service.get_user_consents(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consent/check", response_model=bool, tags=["privacy"])
async def check_user_consent(user_id: str, purpose: str, data_category: str):
    """Check if user has given consent for a specific purpose and data category"""
    try:
        result = gdpr_service.check_consent(
            user_id=user_id,
            purpose=purpose,
            data_category=data_category
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dsr", response_model=DSRResponse, tags=["privacy"])
async def submit_data_subject_request(user_id: str, request_data: DSRRequest):
    """Submit a new data subject request"""
    try:
        # Convert string enum to actual enum
        request_type = RequestType[request_data.request_type.upper()]
        
        result = gdpr_service.submit_data_subject_request(
            user_id=user_id,
            request_type=request_type,
            details=request_data.details
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dsr", response_model=List[DSRResponse], tags=["privacy"])
async def get_user_requests(user_id: str):
    """Get all data subject requests for a user"""
    try:
        result = gdpr_service.get_user_requests(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/dsr/{request_id}", response_model=DSRResponse, tags=["privacy"])
async def update_request_status(request_id: str, update_data: DSRStatusUpdate):
    """Update the status of a data subject request (admin only)"""
    try:
        # Convert string status to enum
        status = RequestStatus[update_data.status.upper()]
        
        result = gdpr_service.update_request_status(
            request_id=request_id,
            status=status,
            note=update_data.note
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs", response_model=List[AccessLogEntry], tags=["privacy"])
async def get_data_access_logs(user_id: str, limit: int = Query(50, ge=1, le=1000)):
    """Get data access logs for a user"""
    try:
        logs = gdpr_service.get_data_access_logs(user_id=user_id)
        # Apply limit from the end (most recent first)
        return logs[-limit:] if len(logs) > limit else logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report", response_model=PrivacyReport, tags=["privacy"])
async def generate_privacy_report(user_id: str):
    """Generate a comprehensive privacy report for a user"""
    try:
        result = gdpr_service.generate_privacy_report(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/retention-policies", response_model=Dict[str, int], tags=["privacy"])
async def get_retention_policies():
    """Get all data retention policies"""
    try:
        result = gdpr_service.get_retention_policies()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retention-policy", response_model=Dict[str, Any], tags=["privacy"])
async def set_retention_policy(policy: RetentionPolicyUpdate):
    """Set retention policy for a category of data (admin only)"""
    try:
        result = gdpr_service.set_retention_policy(
            data_category=policy.data_category,
            retention_days=policy.retention_days
        )
        return {
            "status": "success",
            "message": "Retention policy updated",
            "policy": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/anonymize", response_model=Dict[str, Any], tags=["privacy"])
async def anonymize_data(user_id: str, anonymize_request: AnonymizeRequest):
    """Anonymize sensitive fields in data before processing or sharing"""
    try:
        result = encryption_service.anonymize_data(
            anonymize_request.data, 
            anonymize_request.sensitive_fields
        )
        return {
            "status": "success",
            "anonymized_data": result
        }
    except Exception as e:
        logger.error(f"Error anonymizing data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/record-access", response_model=AccessLogEntry, tags=["privacy"])
async def record_data_access(
    user_id: str, 
    data_category: str, 
    purpose: str, 
    accessed_by: str, 
    access_type: str
):
    """Record data access for audit and compliance purposes"""
    try:
        result = gdpr_service.record_data_access(
            user_id=user_id,
            data_category=data_category,
            purpose=purpose,
            accessed_by=accessed_by,
            access_type=access_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retention-policy", response_model=Dict[str, Any])
async def set_retention_policy(request: RetentionPolicyRequest):
    """
    Set a data retention policy for a category of data.
    
    Args:
        request: RetentionPolicyRequest with data category and retention days
        
    Returns:
        Updated retention policy
    """
    try:
        # Set the retention policy
        updated_policy = gdpr_service.set_retention_policy(
            data_category=request.data_category,
            retention_days=request.retention_days
        )
        
        # Log policy change
        gdpr_service.record_data_access(
            user_id="system",
            data_category="retention_policy",
            purpose="compliance",
            accessed_by="admin",
            access_type="update"
        )
        
        return {
            "status": "success",
            "policy": updated_policy,
            "message": f"Retention policy for {request.data_category} updated to {request.retention_days} days"
        }
        
    except Exception as e:
        logger.error(f"Error setting retention policy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/retention-policies", response_model=Dict[str, Any])
async def get_retention_policies():
    """
    Get all data retention policies.
    
    Returns:
        Dictionary with all retention policies
    """
    try:
        policies = gdpr_service.get_retention_policies()
        
        return {
            "policies": policies,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting retention policies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enforce-retention", response_model=Dict[str, Any])
async def enforce_data_retention(background_tasks: BackgroundTasks):
    """
    Enforce data retention policies by purging expired data.
    This endpoint should be called periodically, typically by a scheduled job.
    
    Returns:
        Status and statistics about purged data
    """
    try:
        # Create stats container to capture results
        stats = {"purged_records": 0, "categories": {}}
        
        # Define callback to update stats
        async def retention_callback(category, count):
            stats["purged_records"] += count
            stats["categories"][category] = count
        
        # Run in background to avoid blocking
        background_tasks.add_task(
            gdpr_service.enforce_retention_policies,
            callback=retention_callback
        )
        
        return {
            "status": "success",
            "message": "Data retention enforcement started in background",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error enforcing data retention: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enforce data retention: {str(e)}"
        )

@router.get("/gdpr-requests", response_model=List[DSRResponse], tags=["privacy"])
async def get_gdpr_requests(user_id: str = Query(..., description="ID of the user to get requests for")):
    """
    Get all GDPR-related data subject requests for a user.
    
    This endpoint returns all GDPR requests the user has submitted, including
    data access, deletion, rectification, and portability requests.
    """
    logger.info(f"Fetching GDPR requests for user {user_id}")
    
    try:
        # Get all data subject requests for the user
        requests = gdpr_service.get_user_requests(user_id)
        
        if not requests:
            # Return empty list for users with no requests
            return []
            
        return requests
        
    except Exception as e:
        logger.error(f"Error fetching GDPR requests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load GDPR requests: {str(e)}"
        )

# Export the router
privacy_router = router 