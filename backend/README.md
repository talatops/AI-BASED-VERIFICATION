# Privacy-Preserving Identity Verification System

This backend implements a privacy-preserving identity verification system using:
- Biometric verification (facial and document)
- AI-powered fraud detection
- Blockchain for immutable record-keeping
- MongoDB for data persistence

## System Architecture

The system consists of the following main components:

1. **API Layer**: FastAPI-based REST API for verification requests
2. **Biometric Service**: Handles facial recognition and document verification
3. **Fraud Detection Service**: AI-powered fraud detection and risk analysis
4. **Blockchain Service**: Stores verification results immutably with MongoDB persistence
5. **MongoDB**: Provides persistent storage for blockchain data

## Requirements

- Python 3.9+
- Docker and Docker Compose
- MongoDB (included in Docker Compose setup)
- Ganache for blockchain simulation (included in Docker Compose setup)

## Running the System

### With Docker Compose

The easiest way to run the system is using Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd privacy

# Start all services
docker-compose up
```

This will start the following services:
- Backend API at http://localhost:8000
- MongoDB at localhost:27017
- Ganache blockchain simulator at http://localhost:8545
- PostgreSQL database at localhost:5432

### Without Docker

If you prefer to run the backend directly:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
export USE_MONGODB=true
export MONGODB_URL=mongodb://localhost:27017/
export MONGODB_DB_NAME=identity_verification

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing the System

### Running the Test Script

A test script is provided to demonstrate the complete verification flow:

```bash
# Make sure the backend is running
cd backend
python tests/test_verification_flow.py
```

This script will:
1. Create sample images for testing
2. Run facial verification
3. Run document verification
4. Check verification status
5. Grant access to a third party
6. Record a ZKP verification
7. Get verification history
8. Get risk analysis
9. Revoke access

### API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## MongoDB Integration

The system can operate in two modes:
1. **Mock Mode**: Stores data in memory (default when MongoDB is not available)
2. **MongoDB Mode**: Stores blockchain data in MongoDB for persistence

To enable MongoDB mode, set the environment variable `USE_MONGODB=true`.

### MongoDB Collections

The system uses the following collections:
- `verifications`: Stores verification records
- `access_grants`: Stores access grant records
- `zkp_verifications`: Stores Zero-Knowledge Proof verification records
- `identities`: Stores user identity records

### Accessing MongoDB Data

You can access the MongoDB data using:

```bash
# Connect to MongoDB container
docker exec -it privacy_mongodb_1 mongosh

# Select the database
use identity_verification

# Query collections
db.verifications.find()
db.access_grants.find()
db.zkp_verifications.find()
```

## Real-World Deployment Considerations

For a real-world deployment, consider:

1. **Replace Mock Services**: Replace the mock biometric and fraud detection services with real implementations
2. **Secure Blockchain Configuration**: Update the blockchain configuration with a real Ethereum node and secure private keys
3. **Add Authentication**: Implement proper authentication and authorization
4. **Database Backups**: Configure regular backups for MongoDB
5. **Monitoring**: Add monitoring and alerting for system components
6. **Scaling**: Set up horizontal scaling for API servers and database
7. **Security Hardening**: Implement security best practices for all components 