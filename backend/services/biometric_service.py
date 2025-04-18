"""
Biometric service for facial recognition and identity verification.
"""

import os
import io
import logging
import numpy as np
import cv2
import face_recognition
import tensorflow as tf
from PIL import Image
from datetime import datetime

logger = logging.getLogger(__name__)

class BiometricService:
    """Service for face recognition and biometric verification."""
    
    def __init__(self):
        """Initialize the biometric service."""
        self.face_model = None
        self.liveness_model = None
        self.load_models()
        
        # Cache of face encodings for registered users
        # In a real implementation, these would be stored in a database
        self.face_encodings = {}
        
        # For mock data demo
        self.mock_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mock')
        os.makedirs(self.mock_data_path, exist_ok=True)

    def load_models(self):
        """Load the face recognition and liveness detection models."""
        try:
            # Pretend to load a pre-trained TensorFlow model for liveness detection
            # In a real implementation, this would load an actual model
            logger.info("Pretending to load liveness detection model")
            self.liveness_model = MockLivenessModel()
            logger.info("Liveness detection model loaded")
        except Exception as e:
            logger.error(f"Error loading liveness detection model: {e}")
            self.liveness_model = None

    def verify_face(self, user_id, face_image_bytes, id_image_bytes=None):
        """Verify a face against a stored reference or ID photo.
        
        Args:
            user_id: The ID of the user to verify
            face_image_bytes: The face image to verify (selfie)
            id_image_bytes: Optional ID document image for first-time verification
            
        Returns:
            dict: Result of verification including success flag and confidence score
        """
        try:
            # Convert image bytes to numpy array for face_recognition library
            face_image = self._bytes_to_image(face_image_bytes)
            
            # Check if it's a real face (liveness detection)
            if self.liveness_model:
                liveness_score = self.liveness_model.predict(face_image)
                if liveness_score < 0.7:  # Threshold for liveness
                    return {
                        "success": False,
                        "message": "Liveness check failed. Please use a real face.",
                        "confidence": liveness_score
                    }
            
            # Find face locations and encodings
            face_locations = face_recognition.face_locations(face_image)
            if not face_locations:
                return {
                    "success": False,
                    "message": "No face detected in the image.",
                    "confidence": 0.0
                }
            
            # Generate face encodings
            face_encodings = face_recognition.face_encodings(face_image, face_locations)
            
            # If this is the first verification (registration) with ID
            if id_image_bytes and user_id not in self.face_encodings:
                # Process ID image to find face
                id_image = self._bytes_to_image(id_image_bytes)
                id_face_locations = face_recognition.face_locations(id_image)
                
                if not id_face_locations:
                    return {
                        "success": False,
                        "message": "No face detected in the ID document.",
                        "confidence": 0.0
                    }
                
                # Generate face encodings from ID
                id_face_encodings = face_recognition.face_encodings(id_image, id_face_locations)
                
                # Compare the selfie face with the ID face
                matches = face_recognition.compare_faces([id_face_encodings[0]], face_encodings[0])
                face_distance = face_recognition.face_distance([id_face_encodings[0]], face_encodings[0])[0]
                confidence = 1.0 - face_distance
                
                if matches[0]:
                    # Store the face encoding for future verifications
                    self.face_encodings[user_id] = face_encodings[0]
                    self._save_mock_data(user_id, face_image_bytes)
                    
                    return {
                        "success": True,
                        "message": "Face successfully verified against ID document.",
                        "confidence": float(confidence)
                    }
                else:
                    return {
                        "success": False,
                        "message": "Face does not match the ID document.",
                        "confidence": float(confidence)
                    }
            
            # If the user already has a registered face, compare with the stored encoding
            elif user_id in self.face_encodings:
                known_encoding = self.face_encodings[user_id]
                matches = face_recognition.compare_faces([known_encoding], face_encodings[0])
                face_distance = face_recognition.face_distance([known_encoding], face_encodings[0])[0]
                confidence = 1.0 - face_distance
                
                if matches[0]:
                    return {
                        "success": True,
                        "message": "Face successfully verified.",
                        "confidence": float(confidence)
                    }
                else:
                    return {
                        "success": False,
                        "message": "Face does not match the registered user.",
                        "confidence": float(confidence)
                    }
            
            # If the user doesn't have a registered face and no ID was provided
            else:
                return {
                    "success": False,
                    "message": "No reference face found for this user. Please provide an ID document for first-time verification.",
                    "confidence": 0.0
                }
                
        except Exception as e:
            logger.error(f"Error verifying face: {e}")
            return {
                "success": False,
                "message": f"Error during face verification: {str(e)}",
                "confidence": 0.0
            }

    def verify_id_document(self, id_image_bytes, id_type):
        """Verify the authenticity of an ID document.
        
        Args:
            id_image_bytes: The ID document image bytes
            id_type: The type of ID document (passport, driver_license, etc.)
            
        Returns:
            dict: Result of verification including success flag and extracted data
        """
        try:
            # Convert image bytes to numpy array for OpenCV
            id_image = self._bytes_to_image(id_image_bytes)
            
            # In a real implementation, this would use OCR and document verification
            # For this example, we'll just mock the verification
            
            # Pretend to extract text from the ID document using OCR
            extracted_data = self._mock_ocr_extraction(id_type)
            
            # Pretend to verify the document features (hologram, watermark, etc.)
            security_features_verified = True
            
            # Pretend to verify the document against an external database
            external_verification = True
            
            if security_features_verified and external_verification:
                return {
                    "success": True,
                    "message": "ID document verified successfully.",
                    "extracted_data": extracted_data,
                    "document_type": id_type
                }
            else:
                return {
                    "success": False,
                    "message": "ID document verification failed.",
                    "confidence": 0.0
                }
                
        except Exception as e:
            logger.error(f"Error verifying ID document: {e}")
            return {
                "success": False,
                "message": f"Error during ID document verification: {str(e)}",
                "confidence": 0.0
            }
    
    def _bytes_to_image(self, image_bytes):
        """Convert image bytes to a numpy array for processing."""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert PIL Image to numpy array
            return np.array(image)
        except Exception as e:
            logger.error(f"Error converting image bytes: {e}")
            raise
    
    def _save_mock_data(self, user_id, image_bytes):
        """Save mock face data for demo purposes."""
        try:
            file_path = os.path.join(self.mock_data_path, f"{user_id}_face.jpg")
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
            logger.info(f"Saved mock face data for user {user_id}")
        except Exception as e:
            logger.error(f"Error saving mock face data: {e}")
    
    def _mock_ocr_extraction(self, id_type):
        """Mock OCR extraction for demo purposes."""
        # In a real implementation, this would use OCR to extract data from the ID
        if id_type == "passport":
            return {
                "document_number": "P12345678",
                "full_name": "JOHN DOE",
                "nationality": "USA",
                "date_of_birth": "1985-06-15",
                "gender": "M",
                "issue_date": "2018-01-01",
                "expiry_date": "2028-01-01",
            }
        elif id_type == "driver_license":
            return {
                "document_number": "DL987654321",
                "full_name": "JOHN DOE",
                "address": "123 PRIVACY ST, SECURE CITY, NY 10001",
                "date_of_birth": "1985-06-15",
                "issue_date": "2020-03-15",
                "expiry_date": "2025-03-15",
                "class": "C",
            }
        else:
            return {
                "document_number": "ID12345678",
                "full_name": "JOHN DOE",
                "date_of_birth": "1985-06-15",
            }


class MockLivenessModel:
    """Mock liveness detection model for demo purposes."""
    
    def predict(self, image):
        """Predict whether an image contains a real face or a spoof.
        
        In a real implementation, this would use a trained model.
        For this example, we'll return a random value with a bias towards "real".
        """
        # Simulate a real liveness detection model
        # In reality, this would analyze the image for signs of spoofing
        
        # Always return a high value for demo purposes
        return 0.95  # 95% confidence that it's a real face

# Create a singleton instance
biometric_service = BiometricService() 