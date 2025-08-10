"""
Basic test suite for FinAgent Meta-Supervisor.

This module contains fundamental tests to ensure core application components
are working correctly and can be imported without errors.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))


class TestApplicationImports:
    """Test that core application modules can be imported successfully."""

    def test_main_app_import(self):
        """Test that the main FastAPI application can be imported."""
        try:
            from meta_supervisor.main import app

            assert app is not None
            assert hasattr(app, "title")
        except ImportError as e:
            pytest.fail(f"Failed to import main app: {e}")

    def test_config_import(self):
        """Test that configuration module can be imported."""
        try:
            from meta_supervisor.config import settings

            assert settings is not None
        except ImportError as e:
            pytest.fail(f"Failed to import config: {e}")

    def test_services_import(self):
        """Test that service modules can be imported."""
        try:
            from meta_supervisor.services.market_analysis_service import (
                MarketAnalysisService,
            )

            assert MarketAnalysisService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import MarketAnalysisService: {e}")

    def test_routers_import(self):
        """Test that router modules can be imported."""
        try:
            from meta_supervisor.routers.api import router

            assert router is not None
        except ImportError as e:
            pytest.fail(f"Failed to import API router: {e}")


class TestMarketAnalysisService:
    """Test the MarketAnalysisService functionality."""

    @pytest.fixture
    def market_service(self):
        """Create a MarketAnalysisService instance for testing."""
        from meta_supervisor.services.market_analysis_service import (
            MarketAnalysisService,
        )

        return MarketAnalysisService()

    def test_service_initialization(self, market_service):
        """Test that MarketAnalysisService initializes correctly."""
        assert market_service is not None
        assert hasattr(market_service, "base_url")
        assert hasattr(market_service, "analyze_market")

    def test_fallback_functionality(self, market_service):
        """Test the _simple_fallback method functionality."""
        # Test the actual fallback method that exists
        result = market_service._simple_fallback("테슬라 분석", "test error")

        assert result is not None
        assert "query" in result
        assert "answer" in result
        assert "timestamp" in result
        assert "source" in result
        assert "error" in result
        assert result["source"] == "fallback"
        assert result["status"] == "api_unavailable"
        assert result["query"] == "테슬라 분석"


class TestConfiguration:
    """Test application configuration."""

    def test_environment_variables(self):
        """Test that required environment variables are handled correctly."""
        # Test that config loads without errors (using session-level env vars)
        try:
            from meta_supervisor.config import settings

            assert settings is not None
            assert settings.OPENAI_API_KEY is not None
            assert len(settings.OPENAI_API_KEY) > 0
            assert "http" in settings.MARKET_ANALYSIS_API_BASE_URL
        except Exception as e:
            pytest.fail(f"Configuration failed with test env vars: {e}")

    def test_default_model_setting(self):
        """Test default LLM model setting."""
        from meta_supervisor.services.market_analysis_service import QueryRequest

        request = QueryRequest(query="test query")
        # Should have a default model
        assert request.model is not None
        assert isinstance(request.model, str)


class TestApplicationHealth:
    """Test basic application health and functionality."""

    def test_python_version_compatibility(self):
        """Test that we're running on a supported Python version."""
        version = sys.version_info
        assert version.major == 3
        assert version.minor >= 10, (
            f"Python 3.10+ required, got {version.major}.{version.minor}"
        )

    def test_required_packages_available(self):
        """Test that required packages are available."""
        required_packages = [
            "fastapi",
            "httpx",
            "pydantic",
            "uvicorn",
            "langchain",
            "langgraph",
        ]

        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                pytest.fail(f"Required package '{package}' is not available")

    def test_basic_service_functionality(self):
        """Test that services can perform basic operations."""
        from meta_supervisor.services.market_analysis_service import (
            MarketAnalysisService,
        )

        service = MarketAnalysisService()

        # Test that fallback functionality works
        result = service._simple_fallback("test query", "test error")
        assert result is not None
        assert isinstance(result, dict)
        assert "answer" in result
        assert "source" in result
        assert result["source"] == "fallback"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
