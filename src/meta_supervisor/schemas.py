from pydantic import BaseModel
from typing import Optional, Dict, Any, TypeVar, Generic

T = TypeVar("T")


class CommonResponse(BaseModel, Generic[T]):
    """
    Common response model for all API endpoints.
    """

    success: bool = True
    data: Optional[T] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class UserRequest(BaseModel):
    """
    Represents a user's request containing a natural language query.
    """

    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class IntentAnalysisResult(BaseModel):
    """
    Represents the result of NLU intent and entity analysis.
    """

    intent: str
    entities: Dict[str, Any]
    confidence: Optional[float] = None


# Placeholder models for backend services
class TradingStrategyRequest(BaseModel):
    parameters: Dict[str, Any]


class TradingStrategyResponse(BaseModel):
    strategy_id: str
    backtest_result: Dict[str, Any]
    chart_url: Optional[str] = None


class MarketAnalysisRequest(BaseModel):
    symbol: str
    analysis_type: str  # e.g., "technical", "fundamental"


class MarketAnalysisResponse(BaseModel):
    report: str
    data: Dict[str, Any]
    chart_url: Optional[str] = None
