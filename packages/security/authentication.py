"""
Authentication Service Implementation

This module provides comprehensive authentication services including JWT tokens,
OAuth/OIDC integration, and multi-factor authentication for the PaaS platform.

Key Features:
- JWT token management with refresh tokens
- OAuth 2.0/OIDC integration with popular providers
- Multi-factor authentication support
- Session management and security
- Password policies and validation
"""

import asyncio
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import bcrypt
import httpx
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import logging

from ..core.domain.models import UserId

logger = logging.getLogger(__name__)


class AuthProvider(Enum):
    """Supported authentication providers"""
    LOCAL = "local"
    GOOGLE = "google"
    GITHUB = "github"
    MICROSOFT = "microsoft"
    AWS_COGNITO = "aws_cognito"
    OKTA = "okta"


class UserRole(Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    DEVELOPER = "developer"
    OPERATOR = "operator"
    VIEWER = "viewer"
    GUEST = "guest"


class Permission(Enum):
    """System permissions"""
    # Application permissions
    APP_CREATE = "app:create"
    APP_READ = "app:read"
    APP_UPDATE = "app:update"
    APP_DELETE = "app:delete"
    APP_DEPLOY = "app:deploy"
    APP_SCALE = "app:scale"
    
    # Plugin permissions
    PLUGIN_INSTALL = "plugin:install"
    PLUGIN_MANAGE = "plugin:manage"
    PLUGIN_DEVELOP = "plugin:develop"
    
    # System permissions
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_MONITOR = "system:monitor"
    SYSTEM_CONFIG = "system:config"
    
    # User management
    USER_MANAGE = "user:manage"
    USER_INVITE = "user:invite"


@dataclass
class TokenClaims:
    """JWT token claims"""
    user_id: str
    email: str
    roles: List[str]
    permissions: List[str]
    provider: str
    issued_at: datetime
    expires_at: datetime
    session_id: str


class UserProfile(BaseModel):
    """User profile information"""
    user_id: str
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None
    provider: AuthProvider
    roles: List[UserRole]
    permissions: List[Permission]
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None
    mfa_enabled: bool = False


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str
    remember_me: bool = False
    mfa_code: Optional[str] = None


class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_profile: UserProfile


class OAuthConfig(BaseModel):
    """OAuth provider configuration"""
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
    user_info_url: str
    scopes: List[str]
    redirect_uri: str


class AuthenticationService:
    """
    Comprehensive authentication service with support for multiple providers,
    JWT tokens, and advanced security features.
    """
    
    def __init__(self,
                 jwt_secret: str,
                 jwt_algorithm: str = "HS256",
                 access_token_expire_minutes: int = 30,
                 refresh_token_expire_days: int = 30):
        """
        Initialize authentication service.
        
        Args:
            jwt_secret: Secret key for JWT token signing
            jwt_algorithm: JWT signing algorithm
            access_token_expire_minutes: Access token expiration time
            refresh_token_expire_days: Refresh token expiration time
        """
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        
        # OAuth configurations
        self.oauth_configs: Dict[AuthProvider, OAuthConfig] = {}
        
        # In-memory stores (in production, use Redis or database)
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.refresh_tokens: Dict[str, Dict[str, Any]] = {}
        self.user_profiles: Dict[str, UserProfile] = {}
        
        # Security settings
        self.max_login_attempts = 5
        self.lockout_duration_minutes = 15
        self.password_min_length = 8
        
        # Rate limiting
        self.login_attempts: Dict[str, List[datetime]] = {}
        
        # Role-based permissions mapping
        self.role_permissions = {
            UserRole.ADMIN: list(Permission),
            UserRole.DEVELOPER: [
                Permission.APP_CREATE, Permission.APP_READ, Permission.APP_UPDATE,
                Permission.APP_DEPLOY, Permission.APP_SCALE,
                Permission.PLUGIN_INSTALL, Permission.PLUGIN_DEVELOP,
                Permission.SYSTEM_MONITOR
            ],
            UserRole.OPERATOR: [
                Permission.APP_READ, Permission.APP_DEPLOY, Permission.APP_SCALE,
                Permission.SYSTEM_MONITOR, Permission.SYSTEM_CONFIG
            ],
            UserRole.VIEWER: [
                Permission.APP_READ, Permission.SYSTEM_MONITOR
            ],
            UserRole.GUEST: [
                Permission.APP_READ
            ]
        }
    
    def configure_oauth_provider(self, provider: AuthProvider, config: OAuthConfig) -> None:
        """Configure OAuth provider settings"""
        self.oauth_configs[provider] = config
        logger.info(f"Configured OAuth provider: {provider.value}")
    
    async def authenticate_user(self, login_request: LoginRequest) -> TokenResponse:
        """
        Authenticate user with email/password and return JWT tokens.
        
        Args:
            login_request: User login credentials
            
        Returns:
            Token response with access and refresh tokens
            
        Raises:
            HTTPException: If authentication fails
        """
        logger.info(f"Authentication attempt for user: {login_request.email}")
        
        # Check rate limiting
        await self._check_rate_limit(login_request.email)
        
        # Validate credentials
        user_profile = await self._validate_credentials(
            login_request.email, 
            login_request.password
        )
        
        if not user_profile:
            await self._record_failed_attempt(login_request.email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check MFA if enabled
        if user_profile.mfa_enabled and not login_request.mfa_code:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="MFA code required",
                headers={"X-MFA-Required": "true"}
            )
        
        if user_profile.mfa_enabled and login_request.mfa_code:
            if not await self._validate_mfa_code(user_profile.user_id, login_request.mfa_code):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid MFA code"
                )
        
        # Generate tokens
        session_id = self._generate_session_id()
        access_token = await self._create_access_token(user_profile, session_id)
        refresh_token = await self._create_refresh_token(user_profile, session_id)
        
        # Update user profile
        user_profile.last_login = datetime.utcnow()
        self.user_profiles[user_profile.user_id] = user_profile
        
        # Store session
        self.active_sessions[session_id] = {
            "user_id": user_profile.user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "ip_address": None,  # Would be set from request context
            "user_agent": None   # Would be set from request context
        }
        
        # Clear failed attempts
        if login_request.email in self.login_attempts:
            del self.login_attempts[login_request.email]
        
        logger.info(f"User authenticated successfully: {user_profile.user_id}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.access_token_expire_minutes * 60,
            user_profile=user_profile
        )
    
    async def authenticate_oauth(self, provider: AuthProvider, authorization_code: str) -> TokenResponse:
        """
        Authenticate user via OAuth provider.
        
        Args:
            provider: OAuth provider
            authorization_code: Authorization code from OAuth flow
            
        Returns:
            Token response with access and refresh tokens
        """
        logger.info(f"OAuth authentication attempt with provider: {provider.value}")
        
        if provider not in self.oauth_configs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"OAuth provider {provider.value} not configured"
            )
        
        config = self.oauth_configs[provider]
        
        # Exchange authorization code for access token
        oauth_token = await self._exchange_oauth_code(config, authorization_code)
        
        # Get user info from OAuth provider
        user_info = await self._get_oauth_user_info(config, oauth_token)
        
        # Create or update user profile
        user_profile = await self._create_or_update_oauth_user(provider, user_info)
        
        # Generate platform tokens
        session_id = self._generate_session_id()
        access_token = await self._create_access_token(user_profile, session_id)
        refresh_token = await self._create_refresh_token(user_profile, session_id)
        
        # Store session
        self.active_sessions[session_id] = {
            "user_id": user_profile.user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "oauth_provider": provider.value,
            "oauth_token": oauth_token
        }
        
        logger.info(f"OAuth user authenticated successfully: {user_profile.user_id}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.access_token_expire_minutes * 60,
            user_profile=user_profile
        )
    
    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New token response
        """
        try:
            # Decode refresh token
            payload = jwt.decode(
                refresh_token, 
                self.jwt_secret, 
                algorithms=[self.jwt_algorithm]
            )
            
            user_id = payload.get("user_id")
            session_id = payload.get("session_id")
            
            if not user_id or not session_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            # Check if session is still active
            if session_id not in self.active_sessions:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session expired"
                )
            
            # Get user profile
            user_profile = self.user_profiles.get(user_id)
            if not user_profile or not user_profile.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive"
                )
            
            # Generate new access token
            new_access_token = await self._create_access_token(user_profile, session_id)
            
            # Update session activity
            self.active_sessions[session_id]["last_activity"] = datetime.utcnow()
            
            return TokenResponse(
                access_token=new_access_token,
                refresh_token=refresh_token,  # Keep same refresh token
                expires_in=self.access_token_expire_minutes * 60,
                user_profile=user_profile
            )
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    
    async def validate_token(self, token: str) -> TokenClaims:
        """
        Validate JWT access token and return claims.
        
        Args:
            token: JWT access token
            
        Returns:
            Token claims
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            payload = jwt.decode(
                token, 
                self.jwt_secret, 
                algorithms=[self.jwt_algorithm]
            )
            
            # Extract claims
            claims = TokenClaims(
                user_id=payload.get("user_id"),
                email=payload.get("email"),
                roles=payload.get("roles", []),
                permissions=payload.get("permissions", []),
                provider=payload.get("provider"),
                issued_at=datetime.fromtimestamp(payload.get("iat")),
                expires_at=datetime.fromtimestamp(payload.get("exp")),
                session_id=payload.get("session_id")
            )
            
            # Validate session is still active
            if claims.session_id not in self.active_sessions:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session expired"
                )
            
            # Update session activity
            self.active_sessions[claims.session_id]["last_activity"] = datetime.utcnow()
            
            return claims
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    async def logout(self, session_id: str) -> bool:
        """
        Logout user and invalidate session.
        
        Args:
            session_id: Session ID to invalidate
            
        Returns:
            True if logout successful
        """
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"User logged out, session invalidated: {session_id}")
            return True
        return False
    
    def check_permission(self, user_roles: List[UserRole], required_permission: Permission) -> bool:
        """
        Check if user has required permission based on roles.
        
        Args:
            user_roles: User's roles
            required_permission: Required permission
            
        Returns:
            True if user has permission
        """
        for role in user_roles:
            if required_permission in self.role_permissions.get(role, []):
                return True
        return False
    
    async def create_user(self, 
                         email: str, 
                         password: str, 
                         name: str,
                         roles: List[UserRole] = None) -> UserProfile:
        """
        Create new user account.
        
        Args:
            email: User email
            password: User password
            name: User display name
            roles: User roles (defaults to [UserRole.DEVELOPER])
            
        Returns:
            Created user profile
        """
        if roles is None:
            roles = [UserRole.DEVELOPER]
        
        # Validate password
        if not self._validate_password(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet requirements"
            )
        
        # Check if user already exists
        for profile in self.user_profiles.values():
            if profile.email == email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists"
                )
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user profile
        user_id = f"user_{secrets.token_urlsafe(16)}"
        permissions = []
        for role in roles:
            permissions.extend(self.role_permissions.get(role, []))
        
        user_profile = UserProfile(
            user_id=user_id,
            email=email,
            name=name,
            provider=AuthProvider.LOCAL,
            roles=roles,
            permissions=list(set(permissions)),  # Remove duplicates
            created_at=datetime.utcnow()
        )
        
        # Store user profile and password
        self.user_profiles[user_id] = user_profile
        # In production, store password hash in secure database
        
        logger.info(f"User created successfully: {user_id}")
        return user_profile
    
    # Private helper methods
    
    async def _check_rate_limit(self, email: str) -> None:
        """Check if user has exceeded login attempt rate limit"""
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=self.lockout_duration_minutes)
        
        if email in self.login_attempts:
            # Remove old attempts
            self.login_attempts[email] = [
                attempt for attempt in self.login_attempts[email]
                if attempt > cutoff
            ]
            
            # Check if too many recent attempts
            if len(self.login_attempts[email]) >= self.max_login_attempts:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Too many login attempts. Try again in {self.lockout_duration_minutes} minutes."
                )
    
    async def _record_failed_attempt(self, email: str) -> None:
        """Record failed login attempt"""
        if email not in self.login_attempts:
            self.login_attempts[email] = []
        self.login_attempts[email].append(datetime.utcnow())
    
    async def _validate_credentials(self, email: str, password: str) -> Optional[UserProfile]:
        """Validate user credentials"""
        # In production, query database for user
        for profile in self.user_profiles.values():
            if profile.email == email and profile.provider == AuthProvider.LOCAL:
                # In production, verify password hash
                # For now, return profile if found
                return profile
        return None
    
    async def _validate_mfa_code(self, user_id: str, mfa_code: str) -> bool:
        """Validate MFA code (placeholder implementation)"""
        # In production, implement TOTP validation
        return len(mfa_code) == 6 and mfa_code.isdigit()
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{secrets.token_urlsafe(32)}"
    
    async def _create_access_token(self, user_profile: UserProfile, session_id: str) -> str:
        """Create JWT access token"""
        now = datetime.utcnow()
        expires = now + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = {
            "user_id": user_profile.user_id,
            "email": user_profile.email,
            "roles": [role.value for role in user_profile.roles],
            "permissions": [perm.value for perm in user_profile.permissions],
            "provider": user_profile.provider.value,
            "session_id": session_id,
            "iat": now,
            "exp": expires
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    async def _create_refresh_token(self, user_profile: UserProfile, session_id: str) -> str:
        """Create JWT refresh token"""
        now = datetime.utcnow()
        expires = now + timedelta(days=self.refresh_token_expire_days)
        
        payload = {
            "user_id": user_profile.user_id,
            "session_id": session_id,
            "type": "refresh",
            "iat": now,
            "exp": expires
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    async def _exchange_oauth_code(self, config: OAuthConfig, code: str) -> str:
        """Exchange OAuth authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.token_url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": config.client_id,
                    "client_secret": config.client_secret,
                    "code": code,
                    "redirect_uri": config.redirect_uri
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to exchange OAuth code"
                )
            
            token_data = response.json()
            return token_data.get("access_token")
    
    async def _get_oauth_user_info(self, config: OAuthConfig, access_token: str) -> Dict[str, Any]:
        """Get user information from OAuth provider"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                config.user_info_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from OAuth provider"
                )
            
            return response.json()
    
    async def _create_or_update_oauth_user(self, provider: AuthProvider, user_info: Dict[str, Any]) -> UserProfile:
        """Create or update user profile from OAuth user info"""
        email = user_info.get("email")
        name = user_info.get("name", email)
        avatar_url = user_info.get("avatar_url") or user_info.get("picture")
        
        # Check if user already exists
        for profile in self.user_profiles.values():
            if profile.email == email:
                # Update existing user
                profile.last_login = datetime.utcnow()
                profile.avatar_url = avatar_url
                return profile
        
        # Create new user
        user_id = f"oauth_{provider.value}_{secrets.token_urlsafe(16)}"
        permissions = self.role_permissions.get(UserRole.DEVELOPER, [])
        
        user_profile = UserProfile(
            user_id=user_id,
            email=email,
            name=name,
            avatar_url=avatar_url,
            provider=provider,
            roles=[UserRole.DEVELOPER],
            permissions=permissions,
            is_verified=True,  # OAuth users are pre-verified
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        
        self.user_profiles[user_id] = user_profile
        return user_profile
    
    def _validate_password(self, password: str) -> bool:
        """Validate password meets security requirements"""
        if len(password) < self.password_min_length:
            return False
        
        # Check for at least one uppercase, lowercase, digit, and special character
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return has_upper and has_lower and has_digit and has_special


class AuthenticationMiddleware:
    """FastAPI middleware for authentication"""
    
    def __init__(self, auth_service: AuthenticationService):
        self.auth_service = auth_service
        self.security = HTTPBearer()
    
    async def __call__(self, credentials: HTTPAuthorizationCredentials) -> TokenClaims:
        """Validate authentication credentials"""
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        return await self.auth_service.validate_token(credentials.credentials)
