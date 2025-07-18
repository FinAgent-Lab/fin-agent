from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables and .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    TRADING_STRATEGY_API_BASE_URL: str = "http://trading-strategy-team/api/v1"
    MARKET_ANALYSIS_API_BASE_URL: str = "http://market-analysis-team/api/v1"


settings = Settings() 