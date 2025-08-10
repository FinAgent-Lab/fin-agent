"""
Test suite for API endpoints.

Tests the FastAPI endpoints to ensure they handle requests and responses correctly.
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, AsyncMock
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

    @patch('meta_supervisor.services.agent_service.AgentService.process_query')
    def test_query_endpoint_string_response(self, mock_process_query, client):
        """Test /api/query endpoint with string response from agent."""
        # Mock agent service to return a simple string result
        mock_process_query.return_value = {
            "intent": "agent_response",
            "result": "테슬라 주식은 현재 좋은 투자 기회입니다."
        }
        
        response = client.post(
            "/api/query",
            json={"query": "테슬라 주식 어때?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "테슬라 주식은 현재 좋은 투자 기회입니다."

    @patch('meta_supervisor.services.agent_service.AgentService.process_query')
    def test_query_endpoint_complex_response(self, mock_process_query, client):
        """Test /api/query endpoint with complex agent response containing messages."""
        # Mock agent service to return complex LangChain-style response
        class MockMessage:
            def __init__(self, content):
                self.content = content
        
        mock_process_query.return_value = {
            "intent": "agent_response",
            "result": {
                "messages": [
                    MockMessage("사용자 질문"),
                    MockMessage("AI 응답: 삼성전자 주식 분석 결과입니다.")
                ],
                "usage_metadata": {"reasoning": 0}
            }
        }
        
        response = client.post(
            "/api/query",
            json={"query": "삼성전자 분석해줘"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "AI 응답: 삼성전자 주식 분석 결과입니다."

    @patch('meta_supervisor.services.agent_service.AgentService.process_query')
    def test_query_endpoint_dict_without_messages(self, mock_process_query, client):
        """Test /api/query endpoint with dict response without messages."""
        mock_process_query.return_value = {
            "intent": "agent_response",
            "result": {"analysis": "시장 분석 데이터", "confidence": 0.85}
        }
        
        response = client.post(
            "/api/query",
            json={"query": "시장 분석"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        # Should convert dict to string
        assert "analysis" in data["answer"]
        assert "confidence" in data["answer"]

    @patch('meta_supervisor.services.agent_service.AgentService.process_query')
    def test_query_endpoint_none_result(self, mock_process_query, client):
        """Test /api/query endpoint with None result."""
        mock_process_query.return_value = {
            "intent": "agent_response",
            "result": None
        }
        
        response = client.post(
            "/api/query",
            json={"query": "빈 응답 테스트"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "응답을 처리할 수 없습니다."

    @patch('meta_supervisor.services.agent_service.AgentService.process_query')
    def test_query_endpoint_exception_handling(self, mock_process_query, client):
        """Test /api/query endpoint exception handling."""
        mock_process_query.side_effect = Exception("Agent service error")
        
        response = client.post(
            "/api/query",
            json={"query": "에러 테스트"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "Agent service error" in data["answer"]

    def test_query_endpoint_invalid_request(self, client):
        """Test /api/query endpoint with invalid request format."""
        response = client.post(
            "/api/query",
            json={}  # Missing required 'query' field
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_query_endpoint_with_optional_fields(self, client):
        """Test /api/query endpoint with optional user_id and session_id."""
        with patch('meta_supervisor.services.agent_service.AgentService.process_query') as mock_process_query:
            mock_process_query.return_value = {
                "intent": "agent_response",
                "result": "테스트 응답"
            }
            
            response = client.post(
                "/api/query",
                json={
                    "query": "테스트 쿼리",
                    "user_id": "test_user_123",
                    "session_id": "session_456"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["answer"] == "테스트 응답"


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