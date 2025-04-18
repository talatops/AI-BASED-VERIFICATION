# Privacy-Preserving Identity Verification System

A blockchain-based identity verification system with AI fraud detection capabilities.

## Overview

This system provides a privacy-preserving identity verification solution with the following features:

- **Real-time identity verification** with facial and document recognition
- **AI-based fraud detection** to identify potential identity theft
- **Blockchain integration** for immutable and secure verification records
- **Zero-Knowledge Proofs** for privacy-preserving verification
- **User-controlled data sharing** with third parties

## Architecture

The system consists of:

- **Frontend**: React application for user interactions
- **Backend**: FastAPI service for verification processing and AI analysis
- **Database**: PostgreSQL for structured data storage
- **Blockchain**: Ethereum-compatible blockchain (Ganache for development)

## Prerequisites

- Docker and Docker Compose
- Git

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/privacy-identity-verification.git
   cd privacy-identity-verification
   ```

2. Run the setup script:
   ```
   chmod +x run.sh
   ./run.sh
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
- `services/`: Business logic
- `models/`: Data models
- `blockchain/`: Blockchain integration

### Frontend Development

Frontend code is in the `frontend/` directory:

- `src/components/`: React components
- `src/pages/`: Application pages
- `src/services/`: API integration
- `src/utils/`: Utility functions

### Docker Configuration

- `docker-compose.yml`: Backend services configuration
- `docker-compose.frontend.yml`: Frontend service configuration
- `backend/Dockerfile`: Backend container configuration
- `frontend/Dockerfile`: Frontend container configuration

## License

MIT 