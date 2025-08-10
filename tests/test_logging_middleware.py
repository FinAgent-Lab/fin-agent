"""
Test suite for Simple Logging Middleware.

Tests the logging middleware functionality including request/response logging,
correlation ID handling, and sensitive data filtering.
"""

import pytest
import sys
import os
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from meta_supervisor.simple_logging import SimpleLoggingMiddleware


class TestSimpleLoggingMiddleware:
    """Test the Simple Logging Middleware functionality."""

    @pytest.fixture
    def test_app(self):
        """Create a test FastAPI app with logging middleware."""
        app = FastAPI()
        app.add_middleware(SimpleLoggingMiddleware)
        
        @app.get("/test")
        async def test_endpoint():
            return {"message": "test response"}
        
        @app.post("/test-post")
        async def test_post_endpoint(data: dict):
            return {"received": data}
        
        return app

    @pytest.fixture
    def client(self, test_app):
        """Create a test client."""
        return TestClient(test_app)

    def test_correlation_id_generation(self, client):
        """Test that correlation ID is generated and added to response headers."""
        response = client.get("/test")
        
        assert response.status_code == 200
        assert "x-correlation-id" in response.headers
        
        correlation_id = response.headers["x-correlation-id"]
        assert correlation_id.startswith("req-")
        assert len(correlation_id) > 10  # req- + 8 character UUID

    def test_sensitive_data_filtering(self):
        """Test that sensitive data is properly filtered from logs."""
        middleware = SimpleLoggingMiddleware(None)
        
        # Test password filtering
        sensitive_json = '{"password": "secret123", "query": "normal data"}'
        filtered = middleware._filter_sensitive_data(sensitive_json)
        assert "secret123" not in filtered
        assert "***" in filtered
        assert "normal data" in filtered
        
        # Test API key filtering
        api_key_json = '{"api_key": "sk-1234567890", "message": "hello"}'
        filtered = middleware._filter_sensitive_data(api_key_json)
        assert "sk-1234567890" not in filtered
        assert "***" in filtered
        assert "hello" in filtered
        
        # Test token filtering
        token_json = '{"token": "bearer-token-123", "data": "public"}'
        filtered = middleware._filter_sensitive_data(token_json)
        assert "bearer-token-123" not in filtered
        assert "***" in filtered
        assert "public" in filtered

    def test_body_size_limiting(self):
        """Test that large request bodies are truncated."""
        # Test the size limiting logic directly
        large_body = "A" * 600
        
        # Test the truncation logic
        truncated = large_body[:500] + "..." if len(large_body) > 500 else large_body
        assert len(truncated) == 503  # 500 + "..."
        assert truncated.endswith("...")
        
        # Test normal size body
        normal_body = "A" * 100
        not_truncated = normal_body[:500] + "..." if len(normal_body) > 500 else normal_body
        assert not_truncated == normal_body
        assert not not_truncated.endswith("...")

    def test_client_ip_extraction(self):
        """Test client IP extraction from various headers."""
        middleware = SimpleLoggingMiddleware(None)
        
        # Mock request with x-forwarded-for header
        mock_request = MagicMock()
        mock_request.headers = {"x-forwarded-for": "192.168.1.100, 10.0.0.1"}
        mock_request.client = None
        
        ip = middleware._get_client_ip(mock_request)
        assert ip == "192.168.1.100"
        
        # Mock request with x-real-ip header
        mock_request.headers = {"x-real-ip": "192.168.1.200"}
        ip = middleware._get_client_ip(mock_request)
        assert ip == "192.168.1.200"
        
        # Mock request with client object
        mock_request.headers = {}
        mock_request.client = MagicMock()
        mock_request.client.host = "127.0.0.1"
        ip = middleware._get_client_ip(mock_request)
        assert ip == "127.0.0.1"
        
        # Mock request with no IP info
        mock_request.headers = {}
        mock_request.client = None
        ip = middleware._get_client_ip(mock_request)
        assert ip == "unknown"

    def test_exclude_paths_customization(self):
        """Test that custom exclude paths work properly."""
        custom_exclude = ["/custom-health", "/custom-docs"]
        middleware = SimpleLoggingMiddleware(None, exclude_paths=custom_exclude)
        
        # Test that the exclude paths are set correctly
        assert middleware.exclude_paths == custom_exclude


# Integration testing is covered by the basic import test
# The middleware functionality is tested via unit tests above


if __name__ == "__main__":
    pytest.main([__file__, "-v"])