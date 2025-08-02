from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables and .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # API Endpoints
    TRADING_STRATEGY_API_BASE_URL: str = "http://trading-strategy-team/api/v1"
    MARKET_ANALYSIS_API_BASE_URL: str = "http://market-analysis-team/api/v1"

    # LLM Configuration
    MAIN_LLM_MODEL: str = "gpt-4o-mini"

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"


settings = Settings()
