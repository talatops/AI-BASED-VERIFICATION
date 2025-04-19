<!-- Project Logo -->
<p align="center">
  <img width="100" src="data:image/svg+xml;utf8,<?xml version='1.0' encoding='UTF-8'?><svg width='100px' height='100px' viewBox='0 0 24 24' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'><title>Lock Icon</title><g id='lock-icon' stroke='none' stroke-width='1' fill='none' fill-rule='evenodd'><path d='M18,8 L17,8 L17,6 C17,3.24 14.76,1 12,1 C9.24,1 7,3.24 7,6 L7,8 L6,8 C4.9,8 4,8.9 4,10 L4,20 C4,21.1 4.9,22 6,22 L18,22 C19.1,22 20,21.1 20,20 L20,10 C20,8.9 19.1,8 18,8 Z M12,17 C10.9,17 10,16.1 10,15 C10,13.9 10.9,13 12,13 C13.1,13 14,13.9 14,15 C14,16.1 13.1,17 12,17 Z M15.1,8 L8.9,8 L8.9,6 C8.9,4.29 10.29,2.9 12,2.9 C13.71,2.9 15.1,4.29 15.1,6 L15.1,8 Z' id='Shape' fill='%23000' fill-rule='nonzero'></path></g></svg>" alt="Lock Icon">
</p>

<h1 align="center">🔐 Privacy-Preserving Identity Verification System</h1>

<p align="center">
A blockchain-based identity verification system with AI fraud detection and privacy-preserving features, fully GDPR-compliant.
</p>


## Overview

This system provides a privacy-preserving identity verification solution with the following features:

- **Real-time identity verification** with facial and document recognition
- **AI-based fraud detection** to identify potential identity theft
- **Blockchain integration** for immutable and secure verification records
- **Zero-Knowledge Proofs** for privacy-preserving verification
- **User-controlled data sharing** with third parties
- **GDPR compliance** for privacy protection
- **Homomorphic encryption** for secure data processing
- **Document verification** with advanced validation techniques

## Architecture

The system consists of:

- **Frontend**: React application for user interactions
- **Backend**: FastAPI service for verification processing and AI analysis
- **Database**: PostgreSQL for structured data storage
- **Blockchain**: Ethereum-compatible blockchain with smart contracts

## Prerequisites

- Docker and Docker Compose
- Git
- Node.js and npm/yarn (for frontend development)
- Python 3.8+ (for backend development)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/talatops/AI-BASED-VERIFICATION.git
   cd AI-BASED-VERIFICATION
   ```

2. Create a `.env` file based on the `.env.example` provided

3. Start the services:
   ```
   docker-compose up -d --build
   ```

This will:
- Build and start the backend services (API, database, blockchain)
- Build and start the frontend service
- Create necessary networks and volumes

## Usage

After starting the services, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development

### Backend Development

Backend code is in the `backend/` directory:

- `main.py`: Application entry point
- `routers/`: API endpoints
  - `verification_router.py`: Identity verification endpoints
  - `privacy_router.py`: Privacy management endpoints
  - `encryption_router.py`: Encryption-related endpoints
- `services/`: Business logic
  - `biometric_service.py`: Facial recognition and biometric analysis
  - `blockchain_service.py`: Blockchain integration
  - `doc_verification_service.py`: Document verification
  - `encryption_service.py`: Data encryption/decryption
  - `fraud_detection_service.py`: AI-based fraud detection
  - `gdpr_compliance_service.py`: GDPR compliance features
  - `homomorphic_encryption_service.py`: Privacy-preserving computations
- `blockchain/`: Blockchain integration
- `utils/`: Utility functions

### Frontend Development

Frontend code is in the `frontend/` directory:

- `src/components/`: React components
- `src/pages/`: Application pages
  - `HomePage.js`: Main landing page
  - `VerificationPage.js`: Identity verification interface
  - `ProfilePage.js`: User profile management
  - `PrivacyDashboardPage.js`: Privacy controls and settings
  - `PermissionsPage.js`: Data sharing permission management
  - `GDPRRequestsPage.js`: GDPR-related requests handling
  - `HomomorphicEncryptionPage.js`: Encrypted data processing features
- `src/services/`: API integration
- `src/utils/`: Utility functions
- `src/contexts/`: React contexts for state management

### Blockchain Development

Blockchain code is in the `blockchain/` directory:

- `contracts/`: Smart contracts
  - `IdentityVerification.sol`: Identity verification smart contract

### Docker Configuration

- `docker-compose.yml`: Services configuration
- `backend/Dockerfile`: Backend container configuration
- `frontend/Dockerfile`: Frontend container configuration

## Key Features

### Privacy-Preserving Verification
- Zero-knowledge proofs for identity verification without exposing personal data
- Homomorphic encryption for processing encrypted data
- User-controlled data sharing permissions

### Security
- AI-based fraud detection
- Document tampering detection
- Secure biometric verification

### Compliance
- GDPR compliance tools
- Audit trails for verification requests
- Data minimization and purpose limitation

## License

MIT 
