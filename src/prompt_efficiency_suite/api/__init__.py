"""API package for the prompt efficiency suite."""

import os
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# JWT settings
SECRET_KEY = os.environ.get("PROMPT_EFFICIENCY_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("PROMPT_EFFICIENCY_SECRET_KEY environment variable must be set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="Prompt Efficiency Suite API",
    description="API for optimizing and managing prompts",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
    """Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Import and include routers
from .analyzer_api import router as analyzer_router
from .model_translator_api import router as translator_router
from .optimizer_api import router as optimizer_router
from .orchestrator_api import router as orchestrator_router
from .tester_api import router as tester_router

app.include_router(analyzer_router, prefix="/api/v1/analyzer", tags=["analyzer"])
app.include_router(translator_router, prefix="/api/v1/translator", tags=["translator"])
app.include_router(optimizer_router, prefix="/api/v1/optimizer", tags=["optimizer"])
app.include_router(
    orchestrator_router, prefix="/api/v1/orchestrator", tags=["orchestrator"]
)
app.include_router(tester_router, prefix="/api/v1/tester", tags=["tester"])
