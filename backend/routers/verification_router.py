"""
Router for handling biometric and identity verification requests.
"""

import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.services.blockchain_service import blockchain_service
from backend.services.biometric_service import BiometricService
from backend.services.fraud_detection_service import fraud_detection_service

# Setup logging
logger = logging.getLogger(__name__)

# Create services
biometric_service = BiometricService()

# Create router
router = APIRouter(
    prefix="/verification",
    tags=["verification"],
)

# Models for request/response validation
class VerificationResponse(BaseModel):
    success: bool
    message: str
    transaction_hash: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    verification_id: Optional[str] = None

class VerificationStatusResponse(BaseModel):
    user_id: str
    verification_type: str
    is_verified: bool
    timestamp: Optional[str] = None
    risk_level: Optional[str] = None

class AccessGrantRequest(BaseModel):
    third_party_id: str
    data_types: List[str]
    expiry_days: Optional[int] = 30

class ZKPVerificationRequest(BaseModel):
    third_party_id: str
    proof_hash: str
    data_type: str

class VerificationHistoryResponse(BaseModel):
    user_id: str
    history: List[Dict[str, Any]]

class ThreatInfo(BaseModel):
    type: str
    confidence: float
    description: str

class RiskAnalysisResponse(BaseModel):
    user_id: str
    risk_level: str
    risk_score: float
    threats_detected: List[ThreatInfo]
    verification_id: str
    timestamp: str

@router.post("/face", response_model=VerificationResponse)
async def verify_face(
    request: Request,
    user_id: str = Query(..., description="ID of the user to verify"),
    face_image: UploadFile = File(..., description="Facial image to verify")
):
    """
    Endpoint for verifying a user's face.
    
    This uses facial recognition and fraud detection to verify a user's identity.
    """
    logger.info(f"Processing facial verification for user {user_id}")
    
    try:
        # Read image data
        contents = await face_image.read()
        
        # Collect device and request metadata for fraud analysis
        verification_metadata = await _extract_verification_metadata(request, user_id)
        
        # Perform facial verification
        verification_result = biometric_service.verify_face(user_id, contents)
        
        # Run fraud detection analysis
        fraud_analysis = fraud_detection_service.analyze_verification_attempt(
            user_id=user_id,
            verification_data=verification_metadata,
            image_data=contents
        )
        
        # Combine verification result with fraud analysis
        verification_success = verification_result["success"] and fraud_analysis["risk_level"] != "high"
        
        # If high risk detected, override success status
        if fraud_analysis["risk_level"] == "high":
            verification_success = False
            message = "Verification failed due to security concerns. Please try again or contact support."
        else:
            message = verification_result.get("message", "Verification processed")
        
        # Record verification status on blockchain
        transaction_success = blockchain_service.update_verification_status(
            user_id, "facial", verification_success
        )
        
        if not transaction_success:
            raise HTTPException(status_code=500, detail="Failed to record verification status")
        
        # Get transaction hash from the blockchain service
        tx_hash = None
        if user_id in blockchain_service.verification_cache and "facial" in blockchain_service.verification_cache[user_id]:
            tx_hash = blockchain_service.verification_cache[user_id]["facial"].get("transaction_hash")
        
        return VerificationResponse(
            success=verification_success,
            message=message,
            transaction_hash=tx_hash,
            risk_level=fraud_analysis["risk_level"],
            risk_score=fraud_analysis["risk_score"],
            verification_id=fraud_analysis["verification_id"]
        )
        
    except Exception as e:
        logger.error(f"Error during facial verification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Verification processing error: {str(e)}")

@router.post("/document", response_model=VerificationResponse)
async def verify_document(
    request: Request,
    user_id: str = Query(..., description="ID of the user to verify"),
    id_document: UploadFile = File(..., description="ID document to verify"),
    document_type: str = Query(..., description="Type of document (passport, driver_license, id_card)")
):
    """
    Endpoint for verifying an ID document.
    
    This extracts information from an ID document and verifies its authenticity while performing fraud detection.
    """
    logger.info(f"Processing document verification for user {user_id}")
    
    try:
        # Read document image
        contents = await id_document.read()
        
        # Collect device and request metadata for fraud analysis
        verification_metadata = await _extract_verification_metadata(request, user_id)
        verification_metadata["document_type"] = document_type
        
        # Verify document
        document_verification = biometric_service.verify_id_document(contents, document_type)
        
        # Run fraud detection analysis
        fraud_analysis = fraud_detection_service.analyze_verification_attempt(
            user_id=user_id,
            verification_data=verification_metadata,
            image_data=contents
        )
        
        # Combine results - document must be verified and not high risk
        verification_success = document_verification["success"] and fraud_analysis["risk_level"] != "high"
        
        # Determine message based on results
        if fraud_analysis["risk_level"] == "high":
            message = "Document verification failed due to security concerns. Please try again or contact support."
            verification_success = False
        else:
            message = document_verification.get("message", "Document verification processed")
        
        # Record verification status on blockchain
        transaction_success = blockchain_service.update_verification_status(
            user_id, "document", verification_success
        )
        
        if not transaction_success:
            raise HTTPException(status_code=500, detail="Failed to record verification status")
        
        # Get transaction hash from the blockchain service
        tx_hash = None
        if user_id in blockchain_service.verification_cache and "document" in blockchain_service.verification_cache[user_id]:
            tx_hash = blockchain_service.verification_cache[user_id]["document"].get("transaction_hash")
        
        return VerificationResponse(
            success=verification_success,
            message=message,
            transaction_hash=tx_hash,
            risk_level=fraud_analysis["risk_level"],
            risk_score=fraud_analysis["risk_score"],
            verification_id=fraud_analysis["verification_id"]
        )
        
    except Exception as e:
        logger.error(f"Error during document verification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Verification processing error: {str(e)}")

@router.get("/status/{verification_type}", response_model=VerificationStatusResponse)
async def check_verification_status(
    user_id: str = Query(..., description="ID of the user to check"),
    verification_type: str = Query(..., description="Type of verification to check (facial, document)")
):
    """
    Check the verification status for a user.
    """
    logger.info(f"Checking {verification_type} verification status for user {user_id}")
    
    try:
        # Get status from blockchain
        is_verified = blockchain_service.get_verification_status(user_id, verification_type)
        
        # Get user's risk profile from fraud detection service
        risk_profile = fraud_detection_service.get_user_risk_profile(user_id)
        
        # Get timestamp from cache if available
        timestamp = None
        if user_id in blockchain_service.verification_cache:
            if verification_type in blockchain_service.verification_cache[user_id]:
                timestamp = blockchain_service.verification_cache[user_id][verification_type].get("timestamp")
        
        return VerificationStatusResponse(
            user_id=user_id,
            verification_type=verification_type,
            is_verified=is_verified,
            timestamp=timestamp,
            risk_level=risk_profile.get("risk_level")
        )
        
    except Exception as e:
        logger.error(f"Error checking verification status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking verification status: {str(e)}")

@router.post("/grant-access", response_model=VerificationResponse)
async def grant_access(
    user_id: str = Query(..., description="ID of the user granting access"),
    request: AccessGrantRequest = Body(...)
):
    """
    Grant access to a third party for specific data types.
    """
    logger.info(f"User {user_id} granting access to {request.third_party_id}")
    
    try:
        # Record access grant on blockchain
        success = blockchain_service.grant_access(
            user_id, 
            request.third_party_id,
            request.data_types,
            request.expiry_days
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to grant access")
        
        # Get transaction hash
        tx_hash = None
        if user_id in blockchain_service.access_grants_cache and request.third_party_id in blockchain_service.access_grants_cache[user_id]:
            tx_hash = blockchain_service.access_grants_cache[user_id][request.third_party_id].get("transaction_hash")
        
        return VerificationResponse(
            success=True,
            message=f"Access granted to {request.third_party_id} for data types: {', '.join(request.data_types)}",
            transaction_hash=tx_hash
        )
        
    except Exception as e:
        logger.error(f"Error granting access: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error granting access: {str(e)}")

@router.post("/revoke-access/{third_party_id}", response_model=VerificationResponse)
async def revoke_access(
    user_id: str = Query(..., description="ID of the user revoking access"),
    third_party_id: str = Query(..., description="ID of the third party losing access")
):
    """
    Revoke access from a third party.
    """
    logger.info(f"User {user_id} revoking access from {third_party_id}")
    
    try:
        # Record access revocation on blockchain
        success = blockchain_service.revoke_access(user_id, third_party_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to revoke access")
        
        # Get transaction hash
        tx_hash = None
        if user_id in blockchain_service.access_grants_cache and third_party_id in blockchain_service.access_grants_cache[user_id]:
            tx_hash = blockchain_service.access_grants_cache[user_id][third_party_id].get("revoke_transaction_hash")
        
        return VerificationResponse(
            success=True,
            message=f"Access revoked from {third_party_id}",
            transaction_hash=tx_hash
        )
        
    except Exception as e:
        logger.error(f"Error revoking access: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error revoking access: {str(e)}")

@router.post("/zkp-verify", response_model=VerificationResponse)
async def record_zkp_verification(
    user_id: str = Query(..., description="ID of the user whose data is verified"),
    request: ZKPVerificationRequest = Body(...)
):
    """
    Record a Zero-Knowledge Proof verification on the blockchain.
    
    This allows proving a user's attribute without revealing the actual data.
    """
    logger.info(f"Recording ZKP verification for user {user_id} by {request.third_party_id}")
    
    try:
        # Verify that the third party has access to this data type
        has_access = blockchain_service.check_access(user_id, request.third_party_id, request.data_type)
        
        if not has_access:
            raise HTTPException(
                status_code=403, 
                detail=f"Third party {request.third_party_id} does not have access to {request.data_type} for user {user_id}"
            )
        
        # Record the verification on blockchain
        success = blockchain_service.record_zkp_verification(
            user_id, 
            request.third_party_id,
            request.proof_hash,
            request.data_type
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to record ZKP verification")
        
        # No transaction hash returned in this mock, but in a real implementation we would get it
        return VerificationResponse(
            success=True,
            message=f"ZKP verification for {request.data_type} recorded successfully",
            transaction_hash=None  # In a real implementation, this would be the transaction hash
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recording ZKP verification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error recording ZKP verification: {str(e)}")

@router.get("/history", response_model=VerificationHistoryResponse)
async def get_verification_history(
    user_id: str = Query(..., description="ID of the user to get history for")
):
    """
    Get verification history for a user.
    """
    logger.info(f"Getting verification history for user {user_id}")
    
    try:
        # Get verification history from blockchain
        history = blockchain_service.get_verification_history(user_id)
        
        return VerificationHistoryResponse(
            user_id=user_id,
            history=history
        )
        
    except Exception as e:
        logger.error(f"Error getting verification history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting verification history: {str(e)}")

@router.get("/risk-analysis", response_model=RiskAnalysisResponse)
async def get_user_risk_analysis(
    user_id: str = Query(..., description="ID of the user to analyze"),
    verification_id: Optional[str] = Query(None, description="Specific verification ID to analyze")
):
    """
    Get detailed risk analysis for a user or specific verification.
    """
    logger.info(f"Getting risk analysis for user {user_id}")
    
    try:
        if verification_id:
            # In a real system, we would retrieve the specific verification from a database
            # For now, just return the user's overall risk profile
            logger.info(f"Specific verification ID not supported yet, returning overall profile")
        
        # Get user risk profile
        risk_profile = fraud_detection_service.get_user_risk_profile(user_id)
        
        # Convert to response format
        threats = []
        
        # This is simulated; in a real implementation, we would get threats from the risk profile
        if risk_profile.get("risk_level") == "high":
            threats.append(ThreatInfo(
                type="suspicious_activity_pattern",
                confidence=0.85,
                description="Multiple failed verification attempts from different locations"
            ))
        elif risk_profile.get("risk_level") == "medium":
            threats.append(ThreatInfo(
                type="unusual_device",
                confidence=0.65,
                description="Verification attempted from unfamiliar device"
            ))
        
        return RiskAnalysisResponse(
            user_id=user_id,
            risk_level=risk_profile.get("risk_level", "unknown"),
            risk_score=risk_profile.get("risk_score", 0.0),
            threats_detected=threats,
            verification_id=verification_id or "overall_profile",
            timestamp=risk_profile.get("last_verification") or "N/A"
        )
        
    except Exception as e:
        logger.error(f"Error getting risk analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting risk analysis: {str(e)}")

@router.get("/audit", response_model=Dict[str, Any])
async def get_verification_audit(
    user_id: str = Query(..., description="ID of the user to get audit for")
):
    """
    Get a complete audit of a user's verifications and access grants.
    """
    logger.info(f"Getting verification audit for user {user_id}")
    
    try:
        # Get the audit from blockchain service
        audit = blockchain_service.get_user_verification_audit(user_id)
        
        return audit
        
    except Exception as e:
        logger.error(f"Error getting verification audit: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting verification audit: {str(e)}")

async def _extract_verification_metadata(request: Request, user_id: str) -> Dict[str, Any]:
    """
    Extract metadata from the request for fraud detection analysis.
    """
    client_host = request.client.host if request.client else "unknown"
    
    # Get headers
    user_agent = request.headers.get("user-agent", "")
    
    # Try to parse body if it's form data (this is just for demo)
    try:
        form = await request.form()
        declared_country = form.get("country", "")
    except:
        declared_country = ""
    
    # Build metadata object
    metadata = {
        "user_id": user_id,
        "ip_address": client_host,
        "timestamp": datetime.now().isoformat(),
        "user_agent": user_agent,
        "device_fingerprint": f"{user_agent}:{client_host}",  # simplified fingerprint
        "declared_country": declared_country,
        "ip_country": "US",  # In a real implementation, this would be determined from IP
        "is_vpn": False,     # In a real implementation, this would be determined from IP
        "is_proxy": False,   # In a real implementation, this would be determined from IP
        "os": _extract_os_from_user_agent(user_agent)
    }
    
    return metadata

def _extract_os_from_user_agent(user_agent: str) -> str:
    """Extract OS information from user agent string."""
    user_agent = user_agent.lower()
    
    if "windows" in user_agent:
        return "windows"
    elif "mac" in user_agent:
        return "macos"
    elif "linux" in user_agent:
        return "linux"
    elif "android" in user_agent:
        return "android"
    elif "ios" in user_agent or "iphone" in user_agent or "ipad" in user_agent:
        return "ios"
    else:
        return "unknown" 