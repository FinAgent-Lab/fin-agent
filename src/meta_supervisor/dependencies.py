from functools import lru_cache
from langchain_openai import ChatOpenAI

from .config import settings
from .services.market_analysis_service import MarketAnalysisService
from .services.trading_service import TradingService
from .services.agent_service import AgentService


@lru_cache()
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.MAIN_LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        timeout=600,          # 3분 타임아웃 설정
        request_timeout=500,   # 개별 요청 1분 타임아웃
        max_retries=2         # 재시도 2회
    )


@lru_cache()
def get_market_analysis_service() -> MarketAnalysisService:
    return MarketAnalysisService()


@lru_cache()
def get_trading_service() -> TradingService:
    return TradingService()


@lru_cache()
def get_agent_service() -> AgentService:
    return AgentService(
        market_service=get_market_analysis_service(),
        llm=get_llm()
    )