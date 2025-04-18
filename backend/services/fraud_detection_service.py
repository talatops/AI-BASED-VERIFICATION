"""
AI-based fraud detection service for real-time identity verification.
"""

import logging
import numpy as np
import cv2
import os
import io
import json
import hashlib
import uuid
from datetime import datetime, timedelta
import tensorflow as tf
from typing import Dict, List, Optional, Any, Tuple
from PIL import Image

# Establish logger
logger = logging.getLogger(__name__)

class FraudDetectionService:
    """
    Service to detect fraudulent identity verification attempts using AI.
    
    This service implements multiple fraud detection strategies:
    1. Behavioral biometrics analysis
    2. Device fingerprinting
    3. Anomaly detection
    4. Image manipulation detection (deepfake, photoshop)
    5. Historical pattern analysis
    """
    
    def __init__(self):
        """Initialize the fraud detection service with required models"""
        # Models path
        self.models_dir = os.path.join(os.path.dirname(__file__), "../models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Load or initialize models
        self.image_manipulation_model = self._load_image_manipulation_model()
        self.anomaly_detection_model = self._load_anomaly_detection_model()
        
        # Store verification attempts for pattern recognition
        self.verification_attempts = {}
        
        # Known fraud patterns (would be updated regularly in real implementation)
        self.fraud_patterns = self._load_fraud_patterns()
        
        # Risk score thresholds
        self.risk_thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8
        }
        
        logger.info("Fraud Detection Service initialized")
    
    def _load_image_manipulation_model(self) -> Any:
        """
        Load the model for detecting manipulated images (deepfakes, photoshopped IDs)
        
        In a real implementation, this would load a trained CNN/transformer model
        """
        try:
            # For demo purposes, we're using a mock model
            # In production, this would load an actual model like:
            # return tf.keras.models.load_model(os.path.join(self.models_dir, 'manipulation_detector.h5'))
            
            class MockImageManipulationModel:
                def __init__(self):
                    self.name = "DeepfakeDetector-v1"
                
                def predict(self, image_array):
                    """
                    Mock prediction that examines image properties to detect likely manipulation.
                    
                    Returns a probability that the image has been manipulated.
                    """
                    # Analyze image noise patterns (simplified version of real detection)
                    if isinstance(image_array, np.ndarray) and image_array.size > 0:
                        # Convert to grayscale if it's color
                        if len(image_array.shape) > 2 and image_array.shape[2] == 3:
                            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
                        else:
                            gray = image_array
                            
                        # Simple noise pattern analysis (extremely simplified)
                        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                        variance = laplacian.var()
                        
                        # Analyze compression artifacts
                        # High compression often indicates manipulation to hide traces
                        _, encoded_img = cv2.imencode('.jpg', gray, [cv2.IMWRITE_JPEG_QUALITY, 90])
                        compression_ratio = len(encoded_img) / gray.size
                        
                        # For demo, generate synthetic score combining factors
                        manip_score = min(1.0, max(0.0, 
                                                  (1.0 - (variance / 500)) * 0.5 + 
                                                  (1.0 - compression_ratio * 5) * 0.5))
                        
                        # Add randomness to simulate real-world model behavior
                        manip_score = min(1.0, max(0.0, 
                                                  manip_score + np.random.normal(0, 0.1)))
                        
                        return manip_score
                    return 0.5  # Default 50% chance if image can't be processed
            
            return MockImageManipulationModel()
            
        except Exception as e:
            logger.error(f"Failed to load image manipulation detection model: {e}")
            return None
    
    def _load_anomaly_detection_model(self) -> Any:
        """
        Load the model for detecting anomalous verification behavior
        
        In a real implementation, this would load a trained anomaly detection model
        """
        try:
            # For demo purposes, we're using a mock model
            class MockAnomalyDetectionModel:
                def __init__(self):
                    self.name = "VerificationAnomalyDetector-v1"
                    # Historical baseline statistics (would be learned from data)
                    self.baseline_stats = {
                        "avg_verification_time": 60,  # seconds
                        "avg_attempts_per_day": 1.2,
                        "avg_device_count": 1.5,
                        "geo_velocity_threshold": 500  # km/hour
                    }
                
                def predict(self, user_data, current_attempt):
                    """
                    Detect anomalous verification attempts based on user history
                    """
                    anomaly_score = 0.0
                    factors = []
                    
                    # Check time of day unusual for this user
                    if user_data.get("verification_history"):
                        time_now = datetime.fromisoformat(current_attempt.get("timestamp"))
                        hour_now = time_now.hour
                        
                        # Calculate historical hour distribution
                        hour_counts = {}
                        for attempt in user_data.get("verification_history", []):
                            try:
                                time = datetime.fromisoformat(attempt.get("timestamp"))
                                hour = time.hour
                                hour_counts[hour] = hour_counts.get(hour, 0) + 1
                            except:
                                pass
                        
                        # If user rarely verifies at this hour
                        if hour_counts.get(hour_now, 0) < 2:
                            anomaly_score += 0.2
                            factors.append("unusual_time")
                    
                    # Check frequency of attempts
                    attempt_count_today = 0
                    today = datetime.now().date()
                    for attempt in user_data.get("verification_history", []):
                        try:
                            time = datetime.fromisoformat(attempt.get("timestamp"))
                            if time.date() == today:
                                attempt_count_today += 1
                        except:
                            pass
                    
                    if attempt_count_today > 3:  # Unusually high number of attempts
                        anomaly_score += min(0.4, (attempt_count_today - 3) * 0.1)
                        factors.append("high_frequency")
                    
                    # Check for multiple device/location anomalies
                    unique_devices = set()
                    unique_ips = set()
                    for attempt in user_data.get("verification_history", []):
                        unique_devices.add(attempt.get("device_fingerprint", ""))
                        unique_ips.add(attempt.get("ip_address", ""))
                    
                    # New device never seen before
                    if current_attempt.get("device_fingerprint") not in unique_devices:
                        anomaly_score += 0.3
                        factors.append("new_device")
                    
                    # IP address never seen before
                    if current_attempt.get("ip_address") not in unique_ips:
                        anomaly_score += 0.2
                        factors.append("new_ip")
                    
                    # Add randomness to simulate real model behavior
                    anomaly_score = min(1.0, max(0.0, 
                                               anomaly_score + np.random.normal(0, 0.05)))
                    
                    return {
                        "score": anomaly_score,
                        "factors": factors
                    }
            
            return MockAnomalyDetectionModel()
            
        except Exception as e:
            logger.error(f"Failed to load anomaly detection model: {e}")
            return None
    
    def _load_fraud_patterns(self) -> Dict:
        """Load known fraud patterns from configuration file"""
        try:
            # In a real implementation, this would load from a regularly updated database
            return {
                "device_fingerprints": [
                    # Known emulators and virtual environments
                    "emulator-android",
                    "BlueStacks",
                    "VirtualBox",
                ],
                "ip_ranges": [
                    # Example high-risk IP ranges (would be more comprehensive)
                    "185.156.73.0/24",
                    "45.227.253.0/24"
                ],
                "image_hashes": [
                    # Hashes of known fake or misused images
                    "e34a8899ef6b983a1882b1167a4b2500",
                    "d41d8cd98f00b204e9800998ecf8427e"
                ]
            }
        except Exception as e:
            logger.error(f"Failed to load fraud patterns: {e}")
            return {}
    
    def analyze_verification_attempt(self, user_id: str, verification_data: Dict, 
                                      image_data: Optional[bytes] = None) -> Dict:
        """
        Analyze an identity verification attempt for potential fraud
        
        Args:
            user_id: The ID of the user being verified
            verification_data: Data about the verification attempt 
                (device info, timestamps, etc.)
            image_data: Optional image data to analyze for manipulation
            
        Returns:
            Analysis results including risk score and identified threats
        """
        try:
            # Initialize result dictionary
            result = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "risk_score": 0.0,
                "risk_level": "low",
                "threats_detected": [],
                "verification_id": str(uuid.uuid4())
            }
            
            # 1. Image manipulation detection (if image provided)
            if image_data is not None and self.image_manipulation_model:
                manip_score = self._analyze_image_manipulation(image_data)
                result["image_manipulation_score"] = float(manip_score)
                
                if manip_score > 0.7:  # High confidence of manipulation
                    result["threats_detected"].append({
                        "type": "image_manipulation",
                        "confidence": float(manip_score),
                        "description": "Possible digital manipulation of verification image"
                    })
                    result["risk_score"] += manip_score * 0.4  # Image manipulation has high weight
            
            # 2. Load user history and device fingerprint analysis
            user_data = self._get_user_verification_history(user_id)
            
            # 3. Behavioral anomaly detection
            if self.anomaly_detection_model:
                anomaly_result = self._detect_behavioral_anomalies(user_data, verification_data)
                result["anomaly_score"] = float(anomaly_result["score"])
                
                if anomaly_result["score"] > 0.6:  # Significant anomaly
                    result["threats_detected"].append({
                        "type": "behavioral_anomaly",
                        "confidence": float(anomaly_result["score"]),
                        "description": f"Unusual verification behavior detected: {', '.join(anomaly_result['factors'])}"
                    })
                    result["risk_score"] += anomaly_result["score"] * 0.3
            
            # 4. Device and network analysis
            device_risk = self._analyze_device_and_network(verification_data)
            result["device_risk_score"] = float(device_risk["score"])
            
            if device_risk["score"] > 0.5:
                result["threats_detected"].append({
                    "type": "suspicious_device",
                    "confidence": float(device_risk["score"]),
                    "description": f"Suspicious device or network detected: {', '.join(device_risk['factors'])}"
                })
                result["risk_score"] += device_risk["score"] * 0.3
            
            # Update risk level based on final risk score
            result["risk_score"] = min(1.0, result["risk_score"])
            if result["risk_score"] >= self.risk_thresholds["high"]:
                result["risk_level"] = "high"
            elif result["risk_score"] >= self.risk_thresholds["medium"]:
                result["risk_level"] = "medium"
            else:
                result["risk_level"] = "low"
            
            # Store the verification attempt for future analysis
            self._store_verification_attempt(user_id, verification_data, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing verification attempt: {e}")
            return {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "risk_score": 0.5,  # Default to medium risk when analysis fails
                "risk_level": "medium",
                "threats_detected": [{
                    "type": "analysis_error",
                    "confidence": 1.0,
                    "description": f"Error during fraud analysis: {str(e)}"
                }],
                "verification_id": str(uuid.uuid4()),
                "error": str(e)
            }
    
    def _analyze_image_manipulation(self, image_data: bytes) -> float:
        """Analyze image for signs of manipulation"""
        try:
            # Convert image bytes to numpy array
            image = np.array(Image.open(io.BytesIO(image_data)))
            
            # Use the model to predict manipulation probability
            manip_score = self.image_manipulation_model.predict(image)
            
            return float(manip_score)
        except Exception as e:
            logger.error(f"Error analyzing image manipulation: {e}")
            return 0.5  # Default medium risk
    
    def _get_user_verification_history(self, user_id: str) -> Dict:
        """Retrieve user's verification history"""
        if user_id not in self.verification_attempts:
            self.verification_attempts[user_id] = {
                "verification_history": []
            }
        return self.verification_attempts[user_id]
    
    def _detect_behavioral_anomalies(self, user_data: Dict, current_attempt: Dict) -> Dict:
        """Detect anomalies in verification behavior"""
        if self.anomaly_detection_model:
            return self.anomaly_detection_model.predict(user_data, current_attempt)
        return {"score": 0.0, "factors": []}
    
    def _analyze_device_and_network(self, verification_data: Dict) -> Dict:
        """Analyze device fingerprint and network characteristics for risks"""
        try:
            score = 0.0
            factors = []
            
            # Check device fingerprint against known fraud patterns
            device_fp = verification_data.get("device_fingerprint", "")
            for suspicious_pattern in self.fraud_patterns.get("device_fingerprints", []):
                if suspicious_pattern in device_fp:
                    score += 0.7
                    factors.append(f"suspicious_device_pattern:{suspicious_pattern}")
                    break
            
            # Check for VPN/proxy use (real implementation would be more sophisticated)
            if verification_data.get("is_proxy", False) or verification_data.get("is_vpn", False):
                score += 0.4
                factors.append("proxy_vpn_detected")
            
            # Check browser/device consistency
            browser = verification_data.get("user_agent", "").lower()
            os_info = verification_data.get("os", "").lower()
            
            if "windows" in os_info and "android" in browser:
                score += 0.6
                factors.append("os_browser_mismatch")
            
            # Check for location/IP inconsistencies
            declared_country = verification_data.get("declared_country")
            ip_country = verification_data.get("ip_country")
            if declared_country and ip_country and declared_country != ip_country:
                score += 0.5
                factors.append("location_mismatch")
            
            # Add randomness to simulate real-world model behavior
            score = min(1.0, max(0.0, score + np.random.normal(0, 0.05)))
            
            return {
                "score": score,
                "factors": factors
            }
            
        except Exception as e:
            logger.error(f"Error analyzing device and network: {e}")
            return {"score": 0.2, "factors": ["analysis_error"]}
    
    def _store_verification_attempt(self, user_id: str, verification_data: Dict, analysis_result: Dict):
        """Store verification attempt for future analysis"""
        if user_id not in self.verification_attempts:
            self.verification_attempts[user_id] = {
                "verification_history": []
            }
        
        # Store relevant details but not the full analysis
        attempt_record = {
            "timestamp": verification_data.get("timestamp", datetime.now().isoformat()),
            "device_fingerprint": verification_data.get("device_fingerprint", ""),
            "ip_address": verification_data.get("ip_address", ""),
            "risk_score": analysis_result.get("risk_score", 0),
            "risk_level": analysis_result.get("risk_level", "low"),
            "verification_id": analysis_result.get("verification_id", "")
        }
        
        self.verification_attempts[user_id]["verification_history"].append(attempt_record)
        
        # Limit history size to prevent memory issues
        max_history = 20
        if len(self.verification_attempts[user_id]["verification_history"]) > max_history:
            self.verification_attempts[user_id]["verification_history"] = \
                self.verification_attempts[user_id]["verification_history"][-max_history:]
    
    def update_fraud_patterns(self):
        """
        Update fraud patterns based on new intelligence
        
        In a real implementation, this would download updates from a central system
        """
        try:
            # Simulate updating fraud patterns (would connect to API in real implementation)
            logger.info("Updating fraud detection patterns")
            
            # Add randomized new patterns to simulate updates
            new_fp = f"suspicious-device-{uuid.uuid4().hex[:8]}"
            self.fraud_patterns["device_fingerprints"].append(new_fp)
            
            # Remove oldest pattern to keep list manageable
            if len(self.fraud_patterns["device_fingerprints"]) > 100:
                self.fraud_patterns["device_fingerprints"].pop(0)
                
            return True
        except Exception as e:
            logger.error(f"Failed to update fraud patterns: {e}")
            return False
    
    def get_user_risk_profile(self, user_id: str) -> Dict:
        """Get the risk profile for a specific user based on verification history"""
        try:
            if user_id not in self.verification_attempts:
                return {
                    "user_id": user_id,
                    "risk_level": "unknown",
                    "confidence": 0.0,
                    "verification_count": 0
                }
            
            history = self.verification_attempts[user_id]["verification_history"]
            if not history:
                return {
                    "user_id": user_id,
                    "risk_level": "unknown",
                    "confidence": 0.0,
                    "verification_count": 0
                }
            
            # Calculate average risk score from last 5 verifications
            recent = history[-5:] if len(history) >= 5 else history
            avg_risk = sum(attempt.get("risk_score", 0) for attempt in recent) / len(recent)
            
            # Determine confidence based on number of verifications
            confidence = min(1.0, len(history) / 10)  # Max confidence at 10+ verifications
            
            # Determine risk level
            if avg_risk >= self.risk_thresholds["high"]:
                risk_level = "high"
            elif avg_risk >= self.risk_thresholds["medium"]:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "user_id": user_id,
                "risk_level": risk_level,
                "risk_score": float(avg_risk),
                "confidence": float(confidence),
                "verification_count": len(history),
                "last_verification": history[-1].get("timestamp") if history else None
            }
            
        except Exception as e:
            logger.error(f"Error getting user risk profile: {e}")
            return {
                "user_id": user_id,
                "risk_level": "unknown",
                "error": str(e)
            }


# Initialize singleton instance
fraud_detection_service = FraudDetectionService() 