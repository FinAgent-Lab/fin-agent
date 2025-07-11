from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings are loaded from environment variables.
    The .env file is used for local development.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Meta-Supervisor Settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # Backend API Endpoints
    TRADING_STRATEGY_API_URL: str = "http://localhost:8001"
    MARKET_ANALYSIS_API_URL: str = "http://localhost:8002"


settings = Settings() 