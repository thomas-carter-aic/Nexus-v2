"""
Test suite for AIC AI Platform Authentication Service
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta

from src.main import app, SECRET_KEY, ALGORITHM

client = TestClient(app)

class TestAuthService:
    """Test cases for authentication service."""

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_login_success(self):
        """Test successful login."""
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            "username": "admin",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self):
        """Test login with non-existent user."""
        login_data = {
            "username": "nonexistent",
            "password": "password"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401

    def test_register_new_user(self):
        """Test user registration."""
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_active"] is True

    def test_register_existing_user(self):
        """Test registration with existing username."""
        register_data = {
            "username": "admin",
            "email": "admin2@example.com",
            "password": "password123"
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_get_current_user_valid_token(self):
        """Test getting current user with valid token."""
        # First login to get a token
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        login_response = client.post("/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Use token to get user info
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["email"] == "admin@aic-aipaas.com"

    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401

    def test_get_current_user_no_token(self):
        """Test getting current user without token."""
        response = client.get("/auth/me")
        assert response.status_code == 403

    def test_validate_token_valid(self):
        """Test token validation with valid token."""
        # First login to get a token
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        login_response = client.post("/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Validate token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/auth/validate", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["user"] == "admin"

    def test_validate_token_invalid(self):
        """Test token validation with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/auth/validate", headers=headers)
        assert response.status_code == 401

    def test_token_expiration(self):
        """Test token expiration handling."""
        # Create an expired token
        expired_payload = {
            "sub": "admin",
            "exp": datetime.utcnow() - timedelta(minutes=1)
        }
        expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Clean up after each test."""
        yield
        # Reset any test data if needed
        pass
