"""
OAuth2/OIDC Configuration for AIC AI Platform
Enterprise SSO integration with multiple providers
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import redis
from sqlalchemy import create_engine, Column, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/oauth2")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# OAuth2 Provider Configurations
OAUTH2_PROVIDERS = {
    "google": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "authorization_url": "https://accounts.google.com/o/oauth2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "scopes": ["openid", "email", "profile"],
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback/google")
    },
    "microsoft": {
        "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
        "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
        "authorization_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "userinfo_url": "https://graph.microsoft.com/v1.0/me",
        "scopes": ["openid", "email", "profile"],
        "redirect_uri": os.getenv("MICROSOFT_REDIRECT_URI", "http://localhost:8000/auth/callback/microsoft")
    },
    "okta": {
        "client_id": os.getenv("OKTA_CLIENT_ID"),
        "client_secret": os.getenv("OKTA_CLIENT_SECRET"),
        "authorization_url": f"https://{os.getenv('OKTA_DOMAIN')}/oauth2/default/v1/authorize",
        "token_url": f"https://{os.getenv('OKTA_DOMAIN')}/oauth2/default/v1/token",
        "userinfo_url": f"https://{os.getenv('OKTA_DOMAIN')}/oauth2/default/v1/userinfo",
        "scopes": ["openid", "email", "profile"],
        "redirect_uri": os.getenv("OKTA_REDIRECT_URI", "http://localhost:8000/auth/callback/okta")
    },
    "auth0": {
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
        "authorization_url": f"https://{os.getenv('AUTH0_DOMAIN')}/authorize",
        "token_url": f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token",
        "userinfo_url": f"https://{os.getenv('AUTH0_DOMAIN')}/userinfo",
        "scopes": ["openid", "email", "profile"],
        "redirect_uri": os.getenv("AUTH0_REDIRECT_URI", "http://localhost:8000/auth/callback/auth0")
    }
}

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis client
redis_client = redis.from_url(REDIS_URL)

# Database Models
class OAuthProvider(Base):
    __tablename__ = "oauth_providers"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    authorization_url = Column(String, nullable=False)
    token_url = Column(String, nullable=False)
    userinfo_url = Column(String, nullable=False)
    scopes = Column(Text)  # JSON array
    redirect_uri = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    token_type = Column(String, default="Bearer")
    expires_at = Column(DateTime)
    scope = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class OAuthState(Base):
    __tablename__ = "oauth_states"
    
    state = Column(String, primary_key=True)
    provider = Column(String, nullable=False)
    redirect_uri = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class OAuthProviderConfig(BaseModel):
    name: str
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
    userinfo_url: str
    scopes: List[str]
    redirect_uri: str

class OAuthAuthorizationRequest(BaseModel):
    provider: str
    redirect_uri: Optional[str] = None
    state: Optional[str] = None

class OAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

class UserInfo(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    provider: str
    provider_id: str

# OAuth2 Manager Class
class OAuth2Manager:
    """Manages OAuth2/OIDC authentication flows"""
    
    def __init__(self):
        self.providers = OAUTH2_PROVIDERS
        self.http_client = httpx.AsyncClient()
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get OAuth2 provider configuration"""
        if provider not in self.providers:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")
        
        config = self.providers[provider]
        if not config.get("client_id") or not config.get("client_secret"):
            raise HTTPException(status_code=500, detail=f"Provider {provider} not configured")
        
        return config
    
    def generate_authorization_url(self, provider: str, state: str, redirect_uri: Optional[str] = None) -> str:
        """Generate OAuth2 authorization URL"""
        config = self.get_provider_config(provider)
        
        params = {
            "client_id": config["client_id"],
            "response_type": "code",
            "scope": " ".join(config["scopes"]),
            "redirect_uri": redirect_uri or config["redirect_uri"],
            "state": state
        }
        
        # Add provider-specific parameters
        if provider == "microsoft":
            params["response_mode"] = "query"
        elif provider == "okta":
            params["nonce"] = state  # Use state as nonce for simplicity
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{config['authorization_url']}?{query_string}"
    
    async def exchange_code_for_token(self, provider: str, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        config = self.get_provider_config(provider)
        
        data = {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        try:
            response = await self.http_client.post(
                config["token_url"],
                data=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Token exchange failed for {provider}: {e}")
            raise HTTPException(status_code=400, detail="Token exchange failed")
    
    async def get_user_info(self, provider: str, access_token: str) -> Dict[str, Any]:
        """Get user information from OAuth2 provider"""
        config = self.get_provider_config(provider)
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = await self.http_client.get(
                config["userinfo_url"],
                headers=headers
            )
            response.raise_for_status()
            user_data = response.json()
            
            # Normalize user data across providers
            normalized_user = self.normalize_user_data(provider, user_data)
            return normalized_user
            
        except httpx.HTTPError as e:
            logger.error(f"User info request failed for {provider}: {e}")
            raise HTTPException(status_code=400, detail="Failed to get user information")
    
    def normalize_user_data(self, provider: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize user data from different providers"""
        
        if provider == "google":
            return {
                "id": user_data.get("id"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "picture": user_data.get("picture"),
                "provider": provider,
                "provider_id": user_data.get("id")
            }
        elif provider == "microsoft":
            return {
                "id": user_data.get("id"),
                "email": user_data.get("mail") or user_data.get("userPrincipalName"),
                "name": user_data.get("displayName"),
                "picture": None,  # Microsoft Graph requires separate call
                "provider": provider,
                "provider_id": user_data.get("id")
            }
        elif provider == "okta":
            return {
                "id": user_data.get("sub"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "picture": user_data.get("picture"),
                "provider": provider,
                "provider_id": user_data.get("sub")
            }
        elif provider == "auth0":
            return {
                "id": user_data.get("sub"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "picture": user_data.get("picture"),
                "provider": provider,
                "provider_id": user_data.get("sub")
            }
        else:
            # Generic normalization
            return {
                "id": user_data.get("sub") or user_data.get("id"),
                "email": user_data.get("email"),
                "name": user_data.get("name") or user_data.get("displayName"),
                "picture": user_data.get("picture"),
                "provider": provider,
                "provider_id": user_data.get("sub") or user_data.get("id")
            }
    
    async def refresh_token(self, provider: str, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        config = self.get_provider_config(provider)
        
        data = {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        try:
            response = await self.http_client.post(
                config["token_url"],
                data=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Token refresh failed for {provider}: {e}")
            raise HTTPException(status_code=400, detail="Token refresh failed")

# JWT Token Manager
class JWTManager:
    """Manages JWT token creation and validation"""
    
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 30
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

# Global instances
oauth2_manager = OAuth2Manager()
jwt_manager = JWTManager()

# Helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_state() -> str:
    """Generate random state for OAuth2 flow"""
    import secrets
    return secrets.token_urlsafe(32)

def store_oauth_state(state: str, provider: str, redirect_uri: str, db: Session):
    """Store OAuth2 state in database"""
    expires_at = datetime.utcnow() + timedelta(minutes=10)  # 10 minutes
    
    oauth_state = OAuthState(
        state=state,
        provider=provider,
        redirect_uri=redirect_uri,
        expires_at=expires_at
    )
    
    db.add(oauth_state)
    db.commit()

def verify_oauth_state(state: str, provider: str, db: Session) -> Optional[OAuthState]:
    """Verify OAuth2 state"""
    oauth_state = db.query(OAuthState).filter(
        OAuthState.state == state,
        OAuthState.provider == provider,
        OAuthState.expires_at > datetime.utcnow()
    ).first()
    
    if oauth_state:
        # Clean up used state
        db.delete(oauth_state)
        db.commit()
    
    return oauth_state

def store_oauth_token(user_id: str, provider: str, token_data: Dict[str, Any], db: Session):
    """Store OAuth2 token in database"""
    
    # Calculate expiration time
    expires_at = None
    if token_data.get("expires_in"):
        expires_at = datetime.utcnow() + timedelta(seconds=token_data["expires_in"])
    
    # Check if token already exists
    existing_token = db.query(OAuthToken).filter(
        OAuthToken.user_id == user_id,
        OAuthToken.provider == provider
    ).first()
    
    if existing_token:
        # Update existing token
        existing_token.access_token = token_data["access_token"]
        existing_token.refresh_token = token_data.get("refresh_token")
        existing_token.expires_at = expires_at
        existing_token.scope = token_data.get("scope")
        existing_token.updated_at = datetime.utcnow()
    else:
        # Create new token
        oauth_token = OAuthToken(
            id=f"{user_id}_{provider}",
            user_id=user_id,
            provider=provider,
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_at=expires_at,
            scope=token_data.get("scope")
        )
        db.add(oauth_token)
    
    db.commit()

# Configuration for FastAPI OAuth2
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/auth/oauth2/authorize",
    tokenUrl="/auth/oauth2/token"
)
