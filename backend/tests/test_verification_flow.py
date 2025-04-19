#!/usr/bin/env python3
"""
Test script to demonstrate the identity verification flow.
This script runs a sequence of API calls that simulate a complete identity verification process,
including facial recognition, document verification, fraud detection, and blockchain recording.
"""

import requests
import json
import os
import time
import argparse
from typing import Dict, Any, List, Optional
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

class IdentityVerificationClient:
    """Client for testing the identity verification API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client with the API base URL."""
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of the API and its services."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def verify_face(self, user_id: str, face_image_path: str) -> Dict[str, Any]:
        """Test facial verification."""
        with open(face_image_path, "rb") as f:
            files = {"face_image": f}
            response = self.session.post(
                f"{self.base_url}/verification/face",
                params={"user_id": user_id},
                files=files
            )
        
        response.raise_for_status()
        return response.json()
    
    def verify_document(self, user_id: str, document_image_path: str, document_type: str) -> Dict[str, Any]:
        """Test document verification."""
        with open(document_image_path, "rb") as f:
            files = {"id_document": f}
            response = self.session.post(
                f"{self.base_url}/verification/document",
                params={"user_id": user_id, "document_type": document_type},
                files=files
            )
        
        response.raise_for_status()
        return response.json()
    
    def check_verification_status(self, user_id: str, verification_type: str) -> Dict[str, Any]:
        """Check verification status."""
        response = self.session.get(
            f"{self.base_url}/verification/status/{verification_type}",
            params={"user_id": user_id}
        )
        
        response.raise_for_status()
        return response.json()
    
    def grant_access(self, user_id: str, third_party_id: str, data_types: List[str], expiry_days: int = 30) -> Dict[str, Any]:
        """Grant access to a third party."""
        payload = {
            "third_party_id": third_party_id,
            "data_types": data_types,
            "expiry_days": expiry_days
        }
        
        response = self.session.post(
            f"{self.base_url}/verification/grant-access",
            params={"user_id": user_id},
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    def revoke_access(self, user_id: str, third_party_id: str) -> Dict[str, Any]:
        """Revoke access from a third party."""
        response = self.session.post(
            f"{self.base_url}/verification/revoke-access/{third_party_id}",
            params={"user_id": user_id}
        )
        
        response.raise_for_status()
        return response.json()
    
    def record_zkp_verification(self, user_id: str, third_party_id: str, proof_hash: str, data_type: str) -> Dict[str, Any]:
        """Record a Zero-Knowledge Proof verification."""
        payload = {
            "third_party_id": third_party_id,
            "proof_hash": proof_hash,
            "data_type": data_type
        }
        
        response = self.session.post(
            f"{self.base_url}/verification/zkp-verify",
            params={"user_id": user_id},
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_verification_history(self, user_id: str) -> Dict[str, Any]:
        """Get verification history for a user."""
        response = self.session.get(
            f"{self.base_url}/verification/history",
            params={"user_id": user_id}
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_risk_analysis(self, user_id: str) -> Dict[str, Any]:
        """Get risk analysis for a user."""
        response = self.session.get(
            f"{self.base_url}/verification/risk-analysis",
            params={"user_id": user_id}
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_verification_audit(self, user_id: str) -> Dict[str, Any]:
        """Get verification audit for a user."""
        response = self.session.get(
            f"{self.base_url}/verification/audit",
            params={"user_id": user_id}
        )
        
        response.raise_for_status()
        return response.json()

def run_verification_demo(api_url: str = "http://localhost:8000", image_dir: str = "data/sample_images"):
    """Run a demo of the verification flow."""
    client = IdentityVerificationClient(api_url)
    
    # Check API health
    logger.info("Checking API health...")
    health = client.health_check()
    logger.info(f"API Status: {json.dumps(health, indent=2)}")
    
    # Demo user IDs
    user_id = "user123"  # This will generate a successful verification
    user_id_fail = "user125"  # This will generate a failed verification
    
    # Sample image paths (replace with actual paths if available)
    face_image = f"{image_dir}/face.jpg"
    id_document = f"{image_dir}/passport.jpg"
    
    # Create sample images if they don't exist
    ensure_sample_images(image_dir)
    
    # 1. Facial Verification
    logger.info(f"\n--- Testing Facial Verification for user {user_id} ---")
    try:
        face_result = client.verify_face(user_id, face_image)
        logger.info(f"Facial verification result: {json.dumps(face_result, indent=2)}")
    except Exception as e:
        logger.error(f"Facial verification failed: {e}")
    
    # 2. Document Verification
    logger.info(f"\n--- Testing Document Verification for user {user_id} ---")
    try:
        doc_result = client.verify_document(user_id, id_document, "passport")
        logger.info(f"Document verification result: {json.dumps(doc_result, indent=2)}")
    except Exception as e:
        logger.error(f"Document verification failed: {e}")
    
    # 3. Check Verification Status
    logger.info(f"\n--- Checking Verification Status for user {user_id} ---")
    try:
        facial_status = client.check_verification_status(user_id, "facial")
        logger.info(f"Facial verification status: {json.dumps(facial_status, indent=2)}")
        
        document_status = client.check_verification_status(user_id, "document")
        logger.info(f"Document verification status: {json.dumps(document_status, indent=2)}")
    except Exception as e:
        logger.error(f"Status check failed: {e}")
    
    # 4. Grant Access to Third Party
    logger.info(f"\n--- Granting Access to a Third Party for user {user_id} ---")
    try:
        grant_result = client.grant_access(
            user_id, 
            "financial_app_1", 
            ["facial", "document"], 
            expiry_days=30
        )
        logger.info(f"Access grant result: {json.dumps(grant_result, indent=2)}")
    except Exception as e:
        logger.error(f"Access grant failed: {e}")
    
    # 5. Record a ZKP Verification
    logger.info(f"\n--- Recording ZKP Verification for user {user_id} ---")
    try:
        zkp_result = client.record_zkp_verification(
            user_id,
            "financial_app_1",
            "0x7a9ec4a7db1abee76f5d699b3b804042c0c41a33ec303a6c8411a4d781cd6fc9",
            "facial"
        )
        logger.info(f"ZKP verification result: {json.dumps(zkp_result, indent=2)}")
    except Exception as e:
        logger.error(f"ZKP verification failed: {e}")
    
    # 6. Get Verification History
    logger.info(f"\n--- Getting Verification History for user {user_id} ---")
    try:
        history_result = client.get_verification_history(user_id)
        logger.info(f"Verification history result: {json.dumps(history_result, indent=2)}")
    except Exception as e:
        logger.error(f"Getting history failed: {e}")
    
    # 7. Get Risk Analysis
    logger.info(f"\n--- Getting Risk Analysis for user {user_id} ---")
    try:
        risk_result = client.get_risk_analysis(user_id)
        logger.info(f"Risk analysis result: {json.dumps(risk_result, indent=2)}")
    except Exception as e:
        logger.error(f"Risk analysis failed: {e}")
    
    # 8. Get Verification Audit
    logger.info(f"\n--- Getting Verification Audit for user {user_id} ---")
    try:
        audit_result = client.get_verification_audit(user_id)
        logger.info(f"Verification audit result: {json.dumps(audit_result, indent=2)}")
    except Exception as e:
        logger.error(f"Getting audit failed: {e}")
    
    # 9. Revoke Access
    logger.info(f"\n--- Revoking Access from a Third Party for user {user_id} ---")
    try:
        revoke_result = client.revoke_access(user_id, "financial_app_1")
        logger.info(f"Access revocation result: {json.dumps(revoke_result, indent=2)}")
    except Exception as e:
        logger.error(f"Access revocation failed: {e}")
    
    logger.info("\n--- Verification Flow Demo Complete ---")

def ensure_sample_images(image_dir: str):
    """Ensure sample images exist for testing."""
    import os
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    
    # Create directory if it doesn't exist
    os.makedirs(image_dir, exist_ok=True)
    
    # Check if images already exist
    face_path = os.path.join(image_dir, "face.jpg")
    passport_path = os.path.join(image_dir, "passport.jpg")
    
    # Create a simple face image if it doesn't exist
    if not os.path.exists(face_path):
        # Create a blank image
        img = Image.new('RGB', (400, 500), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        
        # Draw a face-like shape
        d.ellipse((100, 100, 300, 300), fill=(255, 200, 200))
        d.ellipse((150, 150, 180, 180), fill=(0, 0, 0))  # Left eye
        d.ellipse((220, 150, 250, 180), fill=(0, 0, 0))  # Right eye
        d.arc((150, 200, 250, 250), 0, 180, fill=(0, 0, 0), width=5)  # Mouth
        
        # Add text
        d.text((150, 350), "Sample Face", fill=(255, 255, 255))
        
        # Save the image
        img.save(face_path)
        logger.info(f"Created sample face image at {face_path}")
    
    # Create a simple passport-like image if it doesn't exist
    if not os.path.exists(passport_path):
        # Create a blank image (passport-like dimensions)
        img = Image.new('RGB', (600, 400), color=(200, 200, 200))
        d = ImageDraw.Draw(img)
        
        # Draw a passport-like layout
        d.rectangle((20, 20, 580, 380), outline=(0, 0, 0), width=2)
        d.rectangle((40, 40, 200, 200), outline=(0, 0, 0), width=2)  # Photo area
        
        # Add text
        d.text((250, 50), "PASSPORT", fill=(0, 0, 0))
        d.text((250, 100), "Name: Sample User", fill=(0, 0, 0))
        d.text((250, 150), "DOB: 01-01-1990", fill=(0, 0, 0))
        d.text((250, 200), "Nationality: Sample", fill=(0, 0, 0))
        d.text((250, 250), "Passport No: ABC123456", fill=(0, 0, 0))
        
        # Add a simple face in the photo area
        d.ellipse((80, 70, 160, 150), fill=(255, 200, 200))
        d.ellipse((100, 90, 110, 100), fill=(0, 0, 0))  # Left eye
        d.ellipse((130, 90, 140, 100), fill=(0, 0, 0))  # Right eye
        d.arc((100, 110, 140, 130), 0, 180, fill=(0, 0, 0), width=2)  # Mouth
        
        # Save the image
        img.save(passport_path)
        logger.info(f"Created sample passport image at {passport_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the identity verification API")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--image-dir", default="data/sample_images", help="Directory for sample images")
    
    args = parser.parse_args()
    
    run_verification_demo(args.api_url, args.image_dir) 