from typing import Any, Dict
from pydantic import BaseModel, Field

from .base_tool import BaseAPITool
from ..services.market_analysis_service import MarketAnalysisService


class MarketAnalysisInput(BaseModel):
    """Input schema for market analysis tool."""
    query: str = Field(..., description="Market analysis query (e.g., '삼성전자 기술적 분석', '시장 전망 분석')")


class MarketAnalysisTool(BaseAPITool):
    """
    Tool for market analysis using the market analysis service.
    """
    
    name: str = "market_analysis"
    description: str = "해당 주식에 대한 자세한 시장 분석 보고서를 생성합니다. Analyze stock market data for given symbols with technical or fundamental analysis and generate comprehensive market analysis reports"
    args_schema: type[BaseModel] = MarketAnalysisInput
    service: MarketAnalysisService = Field(default=None, exclude=True)
    
    def __init__(self):
        service = MarketAnalysisService()
        super().__init__(client=service)
        self.__dict__['service'] = service
    
    async def _arun(self, query: str) -> Dict[str, Any]:
        """
        Run market analysis for the given query.
        MarketAnalysisService를 통해 외부 API와 통신합니다.
        """
        return await self.service.analyze_market(query)