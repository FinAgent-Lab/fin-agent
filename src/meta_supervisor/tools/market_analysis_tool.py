from typing import Any, Dict
from pydantic import BaseModel, Field

from .base_tool import BaseAPITool
from ..services.market_analysis_service import MarketAnalysisService


class MarketAnalysisInput(BaseModel):
    """Input schema for market analysis tool."""

    query: str = Field(
        ...,
        description="Market research and fundamental analysis query (e.g., '삼성전자 기업 분석', '반도체 산업 전망', '경제 지표 분석', '시장 센티먼트', '기업 실적 분석')",
    )


class MarketAnalysisTool(BaseAPITool):
    """
    Tool for market analysis using the market analysis service.
    """

    name: str = "market_analysis"
    description: str = "시장 분석 에이전트 - 기업 기본 분석, 산업 동향, 경제 지표, 시장 센티먼트를 분석합니다. Generate comprehensive market research reports including fundamental analysis, sector trends, economic indicators, company financials, and market sentiment analysis for investment decision support"
    args_schema: type[BaseModel] = MarketAnalysisInput
    service: MarketAnalysisService = Field(default=None, exclude=True)

    def __init__(self):
        service = MarketAnalysisService()
        super().__init__(client=service)
        self.__dict__["service"] = service

    async def _arun(self, query: str) -> Dict[str, Any]:
        """
        Run market analysis for the given query.
        MarketAnalysisService를 통해 외부 API와 통신합니다.
        """
        return await self.service.analyze_market(query)
