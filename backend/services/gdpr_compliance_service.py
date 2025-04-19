import logging
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set
from enum import Enum
import hashlib
import re

# Setup logging
logger = logging.getLogger(__name__)

class RequestStatus(Enum):
    """Status values for data subject requests"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class RequestType(Enum):
    """Types of data subject requests under GDPR"""
    ACCESS = "access"          # Right to access
    RECTIFICATION = "rectification"  # Right to rectification
    ERASURE = "erasure"        # Right to be forgotten
    RESTRICTION = "restriction"     # Right to restrict processing
    PORTABILITY = "portability"    # Right to data portability
    OBJECT = "object"         # Right to object
    AUTOMATED = "automated"      # Rights related to automated decision making

class GDPRComplianceService:
    """
    Service for managing GDPR compliance, including data subject requests,
    consent management, and data retention policies.
    """
    
    def __init__(self):
        """Initialize the GDPR compliance service"""
        # Store consent records
        self.consent_records = {}
        
        # Store data subject requests
        self.subject_requests = {}
        
        # Data access logs
        self.access_logs = []
        
        # Default retention policy (in days)
        self.retention_policies = {
            "identity_verification": 365,  # 1 year
            "biometric_data": 180,         # 6 months
            "transaction_data": 730,       # 2 years
            "consent_records": 730,        # 2 years
            "access_logs": 90,             # 3 months
        }
        
        # Authorized purposes by default
        self.authorized_purposes = {
            "identity_verification": True,
            "fraud_detection": True,
            "compliance": True,
            "user_access": True,
            "analytics": False,  # Requires explicit consent
            "marketing": False,  # Requires explicit consent
        }
        
        logger.info("Initialized GDPR Compliance Service")
    
    def verify_purpose_authorization(self, user_id: str, purpose: str) -> bool:
        """
        Verify if a purpose is authorized for data processing
        
        Args:
            user_id: User identifier
            purpose: Purpose for data processing
            
        Returns:
            Boolean indicating if the purpose is authorized
        """
        try:
            # Check if purpose is generally authorized
            if purpose in self.authorized_purposes and self.authorized_purposes[purpose]:
                return True
                
            # Check if user has given consent for this purpose
            return self.check_consent(user_id, purpose, "any")
            
        except Exception as e:
            logger.error(f"Error verifying purpose authorization for user {user_id}: {str(e)}")
            # Default to False for security
            return False
    
    def record_consent(self, user_id: str, purpose: str, data_categories: List[str], 
                      third_parties: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Record user consent for specific data processing
        
        Args:
            user_id: User identifier
            purpose: Purpose of data processing
            data_categories: Categories of data being processed
            third_parties: Optional list of third parties data may be shared with
            
        Returns:
            Dictionary with consent record details
        """
        try:
            consent_id = str(uuid.uuid4())
            
            # Create consent record
            consent_record = {
                "consent_id": consent_id,
                "user_id": user_id,
                "purpose": purpose,
                "data_categories": data_categories,
                "third_parties": third_parties or [],
                "granted_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=365)).isoformat(),  # 1 year by default
                "status": "active"
            }
            
            # Store by user_id for easy lookup
            if user_id not in self.consent_records:
                self.consent_records[user_id] = {}
                
            self.consent_records[user_id][consent_id] = consent_record
            
            # Record this consent action
            self.record_data_access(
                user_id=user_id,
                data_category="consent",
                purpose="consent_management",
                accessed_by="system",
                access_type="create"
            )
            
            logger.info(f"Recorded consent for user {user_id} for purpose {purpose}")
            return consent_record
            
        except Exception as e:
            logger.error(f"Error recording consent for user {user_id}: {str(e)}")
            raise RuntimeError(f"Failed to record consent: {str(e)}")
    
    def withdraw_consent(self, user_id: str, consent_id: str) -> Dict[str, Any]:
        """
        Withdraw previously given consent
        
        Args:
            user_id: User identifier
            consent_id: ID of the consent record to withdraw
            
        Returns:
            Updated consent record
        """
        try:
            # Check if user and consent exist
            if user_id not in self.consent_records or consent_id not in self.consent_records[user_id]:
                raise ValueError(f"Consent record {consent_id} not found for user {user_id}")
            
            # Update consent record
            consent_record = self.consent_records[user_id][consent_id]
            consent_record["status"] = "withdrawn"
            consent_record["withdrawn_at"] = datetime.now().isoformat()
            
            # Record this consent withdrawal
            self.record_data_access(
                user_id=user_id,
                data_category="consent",
                purpose="consent_management",
                accessed_by="user",
                access_type="withdraw"
            )
            
            logger.info(f"Withdrawn consent {consent_id} for user {user_id}")
            return consent_record
            
        except Exception as e:
            logger.error(f"Error withdrawing consent for user {user_id}: {str(e)}")
            raise RuntimeError(f"Failed to withdraw consent: {str(e)}")
    
    def check_consent(self, user_id: str, purpose: str, data_category: str) -> bool:
        """
        Check if user has given consent for a specific purpose and data category
        
        Args:
            user_id: User identifier
            purpose: Purpose of data processing
            data_category: Category of data to check
            
        Returns:
            Boolean indicating if consent exists and is active
        """
        try:
            # No consent records for user
            if user_id not in self.consent_records:
                return False
            
            # Check all active consent records for this user
            for consent_id, record in self.consent_records[user_id].items():
                if (record["status"] == "active" and
                    record["purpose"] == purpose and
                    (data_category in record["data_categories"] or data_category == "any")):
                    
                    # Check if consent has expired
                    expiry = datetime.fromisoformat(record["expires_at"])
                    if expiry > datetime.now():
                        return True
            
            # No valid consent found
            return False
            
        except Exception as e:
            logger.error(f"Error checking consent for user {user_id}: {str(e)}")
            return False
    
    def get_user_consents(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all consent records for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of consent records
        """
        try:
            if user_id not in self.consent_records:
                return []
                
            return list(self.consent_records[user_id].values())
            
        except Exception as e:
            logger.error(f"Error retrieving consents for user {user_id}: {str(e)}")
            return []
    
    def submit_data_subject_request(self, user_id: str, request_type: RequestType, 
                                   details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Submit a data subject request (GDPR)
        
        Args:
            user_id: User identifier
            request_type: Type of request (e.g., access, erasure)
            details: Optional additional details about the request
            
        Returns:
            Dictionary with request details
        """
        try:
            request_id = str(uuid.uuid4())
            
            # Create request record
            request = {
                "request_id": request_id,
                "user_id": user_id,
                "type": request_type.value,
                "details": details or {},
                "status": RequestStatus.PENDING.value,
                "submitted_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "due_by": (datetime.now() + timedelta(days=30)).isoformat(),  # 30 days to fulfill
                "notes": []
            }
            
            # Store for processing
            self.subject_requests[request_id] = request
            
            # Record this DSR submission
            self.record_data_access(
                user_id=user_id,
                data_category="dsr",
                purpose="gdpr_compliance",
                accessed_by="user",
                access_type="submit"
            )
            
            logger.info(f"Submitted {request_type.value} request for user {user_id}")
            return request
            
        except Exception as e:
            logger.error(f"Error submitting request for user {user_id}: {str(e)}")
            raise RuntimeError(f"Failed to submit request: {str(e)}")
    
    def update_request_status(self, request_id: str, status: RequestStatus, 
                             note: Optional[str] = None) -> Dict[str, Any]:
        """
        Update the status of a data subject request
        
        Args:
            request_id: ID of the request to update
            status: New status for the request
            note: Optional note about the status update
            
        Returns:
            Updated request record
        """
        try:
            # Check if request exists
            if request_id not in self.subject_requests:
                raise ValueError(f"Request {request_id} not found")
            
            # Update request
            request = self.subject_requests[request_id]
            request["status"] = status.value
            request["updated_at"] = datetime.now().isoformat()
            
            # Add note if provided
            if note:
                request["notes"].append({
                    "note": note,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Record the DSR status update
            self.record_data_access(
                user_id=request["user_id"],
                data_category="dsr",
                purpose="gdpr_compliance",
                accessed_by="system",
                access_type="update"
            )
            
            logger.info(f"Updated request {request_id} status to {status.value}")
            return request
            
        except Exception as e:
            logger.error(f"Error updating request {request_id}: {str(e)}")
            raise RuntimeError(f"Failed to update request: {str(e)}")
    
    def get_user_requests(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all data subject requests for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of request records
        """
        try:
            # Filter requests by user_id
            return [r for r in self.subject_requests.values() if r["user_id"] == user_id]
            
        except Exception as e:
            logger.error(f"Error retrieving requests for user {user_id}: {str(e)}")
            return []
    
    def record_data_access(self, user_id: str, data_category: str, purpose: str, 
                       accessed_by: str, access_type: str) -> Dict[str, Any]:
        """
        Log access to user data for audit purposes
        
        Args:
            user_id: User identifier
            data_category: Category of data accessed
            purpose: Purpose of the access
            accessed_by: ID of the entity accessing the data (user, system, third-party)
            access_type: Type of access (read, write, delete)
            
        Returns:
            Log entry
        """
        try:
            log_entry = {
                "log_id": str(uuid.uuid4()),
                "user_id": user_id,
                "data_category": data_category,
                "purpose": purpose,
                "accessed_by": accessed_by,
                "access_type": access_type,
                "timestamp": datetime.now().isoformat(),
                "ip_address": "127.0.0.1"  # In a real system, this would be the actual IP
            }
            
            self.access_logs.append(log_entry)
            
            # Trim logs if they get too long (keep last 10000)
            if len(self.access_logs) > 10000:
                self.access_logs = self.access_logs[-10000:]
            
            return log_entry
            
        except Exception as e:
            logger.error(f"Error logging data access for user {user_id}: {str(e)}")
            # Don't raise exception - logging should not block operations
            return {
                "error": str(e),
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
    
    # Alias for record_data_access for backward compatibility
    log_data_access = record_data_access
    
    def get_data_access_logs(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all data access logs for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of access log entries
        """
        try:
            return [log for log in self.access_logs if log["user_id"] == user_id]
            
        except Exception as e:
            logger.error(f"Error retrieving access logs for user {user_id}: {str(e)}")
            return []
    
    def enforce_data_retention(self) -> Dict[str, Any]:
        """
        Enforce data retention policies by purging expired data
        This should be called periodically via a scheduled job
        
        Returns:
            Statistics about purged data
        """
        try:
            now = datetime.now()
            stats = {
                "logs_purged": 0,
                "consents_expired": 0,
                "requests_archived": 0
            }
            
            # Purge old access logs based on retention policy
            retention_days = self.retention_policies.get("access_logs", 90)
            cutoff_date = now - timedelta(days=retention_days)
            
            # Filter access logs to keep only those within retention period
            new_logs = []
            for log in self.access_logs:
                log_date = datetime.fromisoformat(log["timestamp"])
                if log_date >= cutoff_date:
                    new_logs.append(log)
                else:
                    stats["logs_purged"] += 1
            
            self.access_logs = new_logs
            
            # Check for expired consents
            for user_id, user_consents in self.consent_records.items():
                for consent_id, consent in list(user_consents.items()):
                    if consent["status"] == "active":
                        expiry = datetime.fromisoformat(consent["expires_at"])
                        if expiry < now:
                            # Mark as expired
                            consent["status"] = "expired"
                            consent["expired_at"] = now.isoformat()
                            stats["consents_expired"] += 1
            
            # Archive old completed DSRs
            retention_days = self.retention_policies.get("consent_records", 730)
            cutoff_date = now - timedelta(days=retention_days)
            
            for request_id, request in list(self.subject_requests.items()):
                if request["status"] in [RequestStatus.COMPLETED.value, RequestStatus.REJECTED.value]:
                    updated_date = datetime.fromisoformat(request["updated_at"])
                    if updated_date < cutoff_date:
                        # Archive the request (in a real system, this would move to cold storage)
                        self.subject_requests.pop(request_id)
                        stats["requests_archived"] += 1
            
            logger.info(f"Enforced data retention policies: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error enforcing data retention: {str(e)}")
            raise RuntimeError(f"Failed to enforce data retention: {str(e)}")
    
    def set_retention_policy(self, data_category: str, retention_days: int) -> Dict[str, Any]:
        """
        Set retention policy for a category of data
        
        Args:
            data_category: Category of data
            retention_days: Number of days to retain data
            
        Returns:
            Updated retention policy
        """
        try:
            # Validate retention days (minimum 30 days for most data)
            if data_category != "access_logs" and retention_days < 30:
                raise ValueError("Retention period must be at least 30 days for most data categories")
            
            self.retention_policies[data_category] = retention_days
            
            logger.info(f"Set retention policy for {data_category} to {retention_days} days")
            return {
                "data_category": data_category,
                "retention_days": retention_days,
                "updated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error setting retention policy: {str(e)}")
            raise RuntimeError(f"Failed to set retention policy: {str(e)}")
    
    def get_retention_policies(self) -> Dict[str, int]:
        """
        Get all data retention policies
        
        Returns:
            Dictionary of data categories and retention periods
        """
        return self.retention_policies
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Export all user data in a portable, machine-readable format (JSON)
        Required for GDPR Article 20 compliance
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with all user data
        """
        try:
            # Gather all user data from various sources
            consents = self.get_user_consents(user_id)
            requests = self.get_user_requests(user_id)
            access_logs = self.get_data_access_logs(user_id)
            
            # Compile into a structured format
            export_data = {
                "user_id": user_id,
                "export_date": datetime.now().isoformat(),
                "format_version": "1.0",
                "data": {
                    "consents": consents,
                    "data_subject_requests": requests,
                    "access_logs": access_logs
                }
            }
            
            # Record this data export
            self.record_data_access(
                user_id=user_id,
                data_category="user_data",
                purpose="data_portability",
                accessed_by="user",
                access_type="export"
            )
            
            logger.info(f"Exported all data for user {user_id}")
            return export_data
            
        except Exception as e:
            logger.error(f"Error exporting data for user {user_id}: {str(e)}")
            raise RuntimeError(f"Failed to export user data: {str(e)}")
    
    def generate_privacy_report(self, user_id: str) -> Dict[str, Any]:
        """
        Generate a privacy report for a user, showing consent,
        data subject requests, and access logs
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with privacy report details
        """
        try:
            # Get all consent records
            consents = self.get_user_consents(user_id)
            
            # Get all data subject requests
            requests = self.get_user_requests(user_id)
            
            # Get recent access logs (last 50)
            access_logs = self.get_data_access_logs(user_id)
            recent_access = access_logs[-50:] if len(access_logs) > 50 else access_logs
            
            # Get blockchain permissions
            from services.blockchain_service import blockchain_service
            blockchain_permissions = blockchain_service._get_user_access_grants(user_id)
            
            # Convert blockchain permissions to consent format
            blockchain_consents = []
            for perm in blockchain_permissions:
                consent = {
                    "consent_id": f"blockchain_{perm['third_party_id']}",
                    "user_id": user_id,
                    "purpose": "identity_verification",
                    "data_categories": perm["data_types"],
                    "third_parties": [perm["third_party_id"]],
                    "granted_at": perm["granted_at"],
                    "expires_at": perm["expires_at"],
                    "status": "active",
                    "source": "blockchain"
                }
                blockchain_consents.append(consent)
            
            # Compile report
            report = {
                "user_id": user_id,
                "generated_at": datetime.now().isoformat(),
                "active_consents": [c for c in consents if c["status"] == "active"] + blockchain_consents,
                "withdrawn_consents": [c for c in consents if c["status"] == "withdrawn"],
                "open_requests": [r for r in requests if r["status"] in 
                                 [RequestStatus.PENDING.value, RequestStatus.IN_PROGRESS.value]],
                "completed_requests": [r for r in requests if r["status"] in 
                                     [RequestStatus.COMPLETED.value, RequestStatus.REJECTED.value]],
                "recent_data_access": recent_access,
                "data_categories_accessed": list(set(log["data_category"] for log in access_logs)),
                "third_parties_with_access": self._get_third_parties_with_access(user_id, consents + blockchain_consents)
            }
            
            # Record this report generation
            self.record_data_access(
                user_id=user_id,
                data_category="privacy_report",
                purpose="transparency",
                accessed_by="user",
                access_type="read"
            )
            
            logger.info(f"Generated privacy report for user {user_id}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating privacy report for user {user_id}: {str(e)}")
            raise RuntimeError(f"Failed to generate privacy report: {str(e)}")
    
    def anonymize_data(self, user_id: str, data: Dict[str, Any], 
                      sensitive_fields: List[str]) -> Dict[str, Any]:
        """
        Anonymize user data for analytics
        
        Args:
            user_id: User identifier
            data: Data to anonymize
            sensitive_fields: Fields to anonymize
            
        Returns:
            Anonymized data
        """
        try:
            # Create a copy of the data
            anonymized = data.copy()
            
            # Remove user_id - replace with pseudonymous identifier
            if "user_id" in anonymized:
                # Create a deterministic but unrelated pseudonym
                salt = "anon_salt_8x7q2"
                hashed = hashlib.sha256((user_id + salt).encode()).hexdigest()
                anonymized["user_id"] = f"anon_{hashed[:8]}"
            
            # Anonymize sensitive fields based on field type
            for field in sensitive_fields:
                if field in anonymized:
                    value = anonymized[field]
                    
                    if isinstance(value, str):
                        # Different anonymization strategies based on data type
                        if '@' in value and re.match(r'^[^@]+@[^@]+\.[^@]+$', value):  
                            # Email anonymization
                            username, domain = value.split('@')
                            anonymized[field] = f"{self._hash_value(username)}@{domain}"
                        
                        elif re.match(r'^\d{10,15}$', value):  
                            # Phone number 
                            anonymized[field] = f"xxx-xxx-{value[-4:]}" if len(value) >= 4 else "xxx-xxx-xxxx"
                        
                        elif re.match(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$', value):
                            # Date - keep only year 
                            anonymized[field] = f"{value[:4]}-xx-xx"
                        
                        elif len(value) > 4:  
                            # Other string - keep first and last character with hash in middle
                            anonymized[field] = f"{value[0]}****{value[-1]}"
                        
                        else:
                            anonymized[field] = "****"
                    
                    elif isinstance(value, (int, float)):
                        if field.lower() in ['age', 'birth_year', 'year']:
                            # Age/year bucketing (into 5-year ranges)
                            bucket_size = 5
                            lower_bound = (value // bucket_size) * bucket_size
                            anonymized[field] = f"{lower_bound}-{lower_bound + bucket_size - 1}"
                        else:
                            # Random numeric perturbation for other numbers
                            anonymized[field] = 0
                    
                    elif isinstance(value, bool):
                        anonymized[field] = False
                    
                    elif isinstance(value, list) and len(value) > 0:
                        # Keep list structure but anonymize contents
                        if all(isinstance(item, str) for item in value):
                            anonymized[field] = [f"item_{i}" for i in range(len(value))]
                        else:
                            anonymized[field] = []
                    
                    elif isinstance(value, dict):
                        # Recursively anonymize nested dictionaries
                        nested_fields = list(value.keys())
                        anonymized[field] = self.anonymize_data(
                            user_id, 
                            value, 
                            nested_fields
                        )
                    
                    else:
                        anonymized[field] = "REDACTED"
            
            # Record this anonymization
            self.record_data_access(
                user_id=user_id,
                data_category="anonymized_data",
                purpose="analytics",
                accessed_by="system",
                access_type="anonymize"
            )
            
            logger.info(f"Anonymized data for user {user_id}")
            return anonymized
            
        except Exception as e:
            logger.error(f"Error anonymizing data for user {user_id}: {str(e)}")
            raise RuntimeError(f"Failed to anonymize data: {str(e)}")
    
    def _hash_value(self, value: str) -> str:
        """Hash a value for anonymization purposes"""
        salt = "privacy_salt_8675309"
        return hashlib.sha256((value + salt).encode()).hexdigest()[:6]
    
    def _get_third_parties_with_access(self, user_id: str, consents: List[Dict[str, Any]]) -> List[str]:
        """
        Get list of third parties with access to user data
        
        Args:
            user_id: User identifier
            consents: List of consent records
            
        Returns:
            List of third party identifiers
        """
        third_parties = set()
        
        # Get all third parties from active consents
        for consent in consents:
            if consent["status"] == "active":
                # Check if consent has expired
                if "expires_at" in consent:
                    expiry = datetime.fromisoformat(consent["expires_at"])
                    if expiry > datetime.now():
                        # Add all third parties
                        if "third_parties" in consent and isinstance(consent["third_parties"], list):
                            third_parties.update(consent["third_parties"])
                        # Also check for blockchain permissions that might have third_party_id directly
                        elif "third_party_id" in consent:
                            third_parties.add(consent["third_party_id"])
        
        return list(third_parties) 