from functools import lru_cache
from langchain_openai import ChatOpenAI

from .services.market_analysis_service import MarketAnalysisService
from .services.trading_service import TradingService
from .services.agent_service import AgentService


@lru_cache()
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-3.5-turbo")


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
        trading_service=get_trading_service(),
        llm=get_llm()
    )