from typing import Any, Dict
from pydantic import BaseModel, Field

from .base_tool import BaseAPITool
from ..services.trading_service import TradingService


class TradingStrategyInput(BaseModel):
    """Input schema for trading strategy tool."""
    parameters: Dict[str, Any] = Field(..., description="Trading strategy parameters")


class TradingTool(BaseAPITool):
    """
    Tool for creating trading strategies using the trading service.
    """
    
    name: str = "trading_strategy"
    description: str = "Create and backtest trading strategies with given parameters"
    args_schema: type[BaseModel] = TradingStrategyInput
    
    def __init__(self):
        self.service = TradingService()
        super().__init__(client=self.service)
    
    async def _arun(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a trading strategy with the given parameters.
        """
        try:
            response = await self.service.create_strategy(parameters)
            
            return {
                "strategy_id": response.strategy_id,
                "backtest_result": response.backtest_result,
                "chart_url": response.chart_url,
                "parameters": parameters
            }
            
        except Exception as e:
            return {
                "error": f"Trading strategy creation failed: {str(e)}",
                "parameters": parameters
            }