"""
Trading Tool for message-based API interaction.
"""
from typing import Dict, Any
from pydantic import BaseModel, Field

from .base_tool import BaseAPITool
from ..services.trading_service import TradingService


class TradingInput(BaseModel):
    """Input schema for trading tool."""
    message: str = Field(
        ..., 
        description="Trading analysis or execution query (e.g., '삼성전자 차트 분석', 'RSI 지표 확인', '매수 시점 분석', '포트폴리오 리밸런싱', '기술적 분석', '매매 전략')"
    )


class TradingTool(BaseAPITool):
    """
    Tool for interacting with the trading service using message-based API.
    
    Sends simple message queries and receives role/content responses.
    """
    
    name: str = "trading"
    description: str = "매매 에이전트 - 주식 거래, 차트 분석, 기술적 지표 분석을 수행합니다. Execute trading strategies, chart analysis, technical indicators (RSI, MACD, Bollinger Bands), price pattern recognition, portfolio management, and risk assessment for informed trading decisions"
    args_schema: type[BaseModel] = TradingInput
    service: TradingService = Field(default=None, exclude=True)
    
    def __init__(self):
        service = TradingService()
        super().__init__(client=service)
        self.__dict__["service"] = service
    
    async def _arun(self, message: str) -> Dict[str, Any]:
        """
        Send a trading query message.
        
        Args:
            message: Query message to send
            
        Returns:
            Dictionary with role, content, and success status
        """
        try:
            response = await self.service.send_query(message)
            
            return {
                "role": response.role,
                "content": response.content,
                "success": response.role != "error"
            }
            
        except Exception as e:
            return {
                "role": "error",
                "content": f"Failed to process trading query: {str(e)}",
                "success": False
            }