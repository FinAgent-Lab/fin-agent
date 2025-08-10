"""
Test suite for API endpoints.

Tests the FastAPI endpoints to ensure they handle requests and responses correctly.
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from meta_supervisor.main import app
from meta_supervisor import schemas


class TestAPIEndpoints:
    """Test API endpoint functionality."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI application."""
        return TestClient(app)

    def test_health_endpoint(self, client):
        """Test that health endpoint returns proper status."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["service"] == "Meta Supervisor"

    def test_root_endpoint(self, client):
        """Test that root endpoint returns basic info."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "Meta Supervisor"
        assert data["version"] == "0.1.0"
        assert data["status"] == "running"

    def test_query_endpoint_invalid_request(self, client):
        """Test /api/query endpoint with invalid request format."""
        response = client.post(
            "/api/query",
            json={}  # Missing required 'query' field
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestSchemaValidation:
    """Test Pydantic schema validation."""

    def test_user_request_validation(self):
        """Test UserRequest schema validation."""
        # Valid request
        valid_request = schemas.UserRequest(query="테스트 쿼리")
        assert valid_request.query == "테스트 쿼리"
        assert valid_request.user_id is None
        assert valid_request.session_id is None

        # Request with optional fields
        full_request = schemas.UserRequest(
            query="테스트 쿼리",
            user_id="user123",
            session_id="session456"
        )
        assert full_request.user_id == "user123"
        assert full_request.session_id == "session456"

    def test_response_body_validation(self):
        """Test ResponseBody schema validation."""
        # Valid response
        response = schemas.ResponseBody(answer="테스트 응답")
        assert response.answer == "테스트 응답"

        # Should reject non-string answers
        with pytest.raises(Exception):
            schemas.ResponseBody(answer={"invalid": "dict"})

    def test_common_response_validation(self):
        """Test CommonResponse schema validation."""
        # Success response
        success_response = schemas.CommonResponse(data={"result": "success"})
        assert success_response.success is True
        assert success_response.error_code is None

        # Error response
        error_response = schemas.CommonResponse(
            success=False,
            error_code="TEST_ERROR",
            error_message="Test error message"
        )
        assert error_response.success is False
        assert error_response.error_code == "TEST_ERROR"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])