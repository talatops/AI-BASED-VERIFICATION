from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Privacy-Preserving Identity Verification API",
    description="API for the blockchain-based AI identity verification system",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Import routers from other modules
from api.routers import auth, identity, permissions, blockchain, user

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(identity.router, prefix="/api/identity", tags=["Identity Verification"])
app.include_router(permissions.router, prefix="/api/permissions", tags=["Permission Management"])
app.include_router(blockchain.router, prefix="/api/blockchain", tags=["Blockchain"])
app.include_router(user.router, prefix="/api/user", tags=["User Profile"])

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Check if the API is running."""
    return {"status": "ok", "message": "API is running"} 