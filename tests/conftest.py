"""
Pytest configuration and fixtures for FinAgent Meta-Supervisor tests.
"""

import os
import pytest
from unittest.mock import patch


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables before any tests run."""
    test_env = {
        "OPENAI_API_KEY": "test-openai-key-for-testing",
        "MARKET_ANALYSIS_API_BASE_URL": "http://localhost:8001/test",
        "TRADING_STRATEGY_API_BASE_URL": "http://localhost:8002/test",
        "MAIN_LLM_MODEL": "gpt-4o-mini",
        "ENVIRONMENT": "testing",
    }

    with patch.dict(os.environ, test_env, clear=False):
        yield


@pytest.fixture
def mock_environment():
    """Provide a clean environment for individual tests."""
    test_env = {
        "OPENAI_API_KEY": "test-key",
        "MARKET_ANALYSIS_API_BASE_URL": "http://test-market-api",
        "TRADING_STRATEGY_API_BASE_URL": "http://test-trading-api",
    }

    with patch.dict(os.environ, test_env, clear=False):
        yield test_env
