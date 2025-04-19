# Privacy-Preserving Identity Verification System

A blockchain-based identity verification system with AI fraud detection capabilities and enhanced privacy features.


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
