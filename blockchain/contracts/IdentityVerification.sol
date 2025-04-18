// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Identity Verification Contract
/// @notice This contract manages identity verification records on the blockchain
contract IdentityVerification {
    
    // Verification status
    enum VerificationStatus { Pending, Verified, Rejected }
    
    // Verification types
    enum VerificationType { GovernmentID, Biometric, Address }
    
    // Identity record
    struct Identity {
        address owner;
        bytes32 dataHash;  // Hash of the personal data (stored off-chain)
        mapping(uint8 => VerificationStatus) verificationStatus;  // Mapping verification type to status
        mapping(uint8 => uint256) verificationTimestamp;  // When verification occurred
        bool exists;
    }
    
    // Access control for third parties
    struct AccessControl {
        address thirdParty;
        address user;
        bool hasAccess;
        uint256 expiryTimestamp;
        bytes32[] allowedDataTypes;  // What data types can be accessed
    }
    
    // ZKP verification records
    struct ZKProofVerification {
        address verifier;
        address user;
        bytes32 proofHash;
        bytes32 dataType;
        uint256 timestamp;
        bool verified;
    }
    
    // Mapping from user address to identity
    mapping(address => Identity) private identities;
    
    // List of all access controls
    mapping(bytes32 => AccessControl) private accessControls;
    
    // List of ZKP verification records
    ZKProofVerification[] private zkpVerifications;
    
    // Events
    event IdentityCreated(address indexed owner, bytes32 dataHash);
    event VerificationUpdated(address indexed owner, uint8 verificationType, VerificationStatus status);
    event AccessGranted(address indexed user, address indexed thirdParty, uint256 expiryTimestamp);
    event AccessRevoked(address indexed user, address indexed thirdParty);
    event ZKProofVerified(address indexed user, address indexed verifier, bytes32 dataType);
    
    // Modifiers
    modifier onlyIdentityOwner(address owner) {
        require(msg.sender == owner, "Only identity owner can perform this action");
        _;
    }
    
    modifier identityExists(address owner) {
        require(identities[owner].exists, "Identity does not exist");
        _;
    }
    
    modifier hasAccessTo(address user) {
        bytes32 accessId = keccak256(abi.encodePacked(msg.sender, user));
        require(accessControls[accessId].hasAccess, "No access to this identity");
        require(accessControls[accessId].expiryTimestamp > block.timestamp, "Access has expired");
        _;
    }
    
    // Functions
    
    /// @notice Create a new identity record
    /// @param dataHash Hash of the personal data
    function createIdentity(bytes32 dataHash) external {
        require(!identities[msg.sender].exists, "Identity already exists");
        
        Identity storage identity = identities[msg.sender];
        identity.owner = msg.sender;
        identity.dataHash = dataHash;
        identity.exists = true;
        
        emit IdentityCreated(msg.sender, dataHash);
    }
    
    /// @notice Update verification status
    /// @param owner Identity owner address
    /// @param verificationType Type of verification
    /// @param status New verification status
    function updateVerification(
        address owner, 
        uint8 verificationType, 
        VerificationStatus status
    ) 
        external 
        identityExists(owner)
    {
        // In a real implementation, this would have more access control
        // Only verified verifiers should be able to update verification status
        
        Identity storage identity = identities[owner];
        identity.verificationStatus[verificationType] = status;
        identity.verificationTimestamp[verificationType] = block.timestamp;
        
        emit VerificationUpdated(owner, verificationType, status);
    }
    
    /// @notice Grant access to a third party
    /// @param thirdParty Address of the third party
    /// @param expiryTimestamp When the access expires
    /// @param allowedDataTypes Which data types can be accessed
    function grantAccess(
        address thirdParty, 
        uint256 expiryTimestamp, 
        bytes32[] calldata allowedDataTypes
    ) 
        external 
        identityExists(msg.sender)
    {
        bytes32 accessId = keccak256(abi.encodePacked(thirdParty, msg.sender));
        
        AccessControl storage access = accessControls[accessId];
        access.thirdParty = thirdParty;
        access.user = msg.sender;
        access.hasAccess = true;
        access.expiryTimestamp = expiryTimestamp;
        access.allowedDataTypes = allowedDataTypes;
        
        emit AccessGranted(msg.sender, thirdParty, expiryTimestamp);
    }
    
    /// @notice Revoke access from a third party
    /// @param thirdParty Address of the third party
    function revokeAccess(address thirdParty) 
        external 
        identityExists(msg.sender)
    {
        bytes32 accessId = keccak256(abi.encodePacked(thirdParty, msg.sender));
        
        require(accessControls[accessId].hasAccess, "No access to revoke");
        require(accessControls[accessId].user == msg.sender, "Not authorized to revoke access");
        
        accessControls[accessId].hasAccess = false;
        
        emit AccessRevoked(msg.sender, thirdParty);
    }
    
    /// @notice Record a ZKP verification
    /// @param user User address
    /// @param proofHash Hash of the ZKP
    /// @param dataType Type of data being verified
    function recordZKProofVerification(
        address user, 
        bytes32 proofHash, 
        bytes32 dataType
    ) 
        external 
        identityExists(user)
        hasAccessTo(user)
    {
        ZKProofVerification memory zkp = ZKProofVerification({
            verifier: msg.sender,
            user: user,
            proofHash: proofHash,
            dataType: dataType,
            timestamp: block.timestamp,
            verified: true
        });
        
        zkpVerifications.push(zkp);
        
        emit ZKProofVerified(user, msg.sender, dataType);
    }
    
    /// @notice Check if an identity has been verified for a specific type
    /// @param owner Identity owner address
    /// @param verificationType Type of verification
    /// @return status The verification status
    function getVerificationStatus(address owner, uint8 verificationType) 
        external 
        view 
        identityExists(owner)
        returns (VerificationStatus)
    {
        return identities[owner].verificationStatus[verificationType];
    }
    
    /// @notice Check if a third party has access to a user's identity
    /// @param thirdParty Address of the third party
    /// @param user User address
    /// @return Whether access is granted and not expired
    function checkAccess(address thirdParty, address user) 
        external 
        view 
        returns (bool)
    {
        bytes32 accessId = keccak256(abi.encodePacked(thirdParty, user));
        
        return (
            accessControls[accessId].hasAccess && 
            accessControls[accessId].expiryTimestamp > block.timestamp
        );
    }
} 