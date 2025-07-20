import httpx
from typing import Any, Dict, Optional
from pydantic import BaseModel
import os
from ..config import settings


class QueryRequest(BaseModel):
    """외부 마켓 분석 API 요청 포맷"""
    query: str
    model: Optional[str] = os.getenv("MAIN_LLM_MODEL", "gpt-4o-mini")
    temperature: Optional[float] = 0.2


class QueryResponse(BaseModel):
    """외부 마켓 분석 API 응답 포맷"""
    answer: str
    timestamp: str


class MarketAnalysisService:
    def __init__(self):
        self.base_url = settings.MARKET_ANALYSIS_API_BASE_URL
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """HTTP request handler for external market analysis API."""
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method, url=url, params=params, json=json, timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise Exception(f"Market Analysis API request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"Market Analysis API returned error: {e.response.status_code} {e.response.text}"
            )
    
    async def analyze_market(self, query: str) -> Dict[str, Any]:
        """외부 마켓 분석 API와 통신하여 분석 결과를 가져옵니다."""
        try:
            request_data = QueryRequest(
                query=query,
                model=os.getenv("MAIN_LLM_MODEL", "gpt-4o-mini"),
                temperature=0.2
            )
            
            response_data = await self._request(
                method="POST",
                endpoint="/analyze",
                json=request_data.model_dump()
            )
            
            response = QueryResponse(**response_data)
            
            return {
                "query": query,
                "answer": response.answer,
                "timestamp": response.timestamp
            }
            
        except Exception as e:
            return {
                "error": f"Market analysis failed: {str(e)}",
                "query": query
            }
    
    async def get_market_data(self, query: str = "시장 데이터 분석") -> Dict[str, Any]:
        return await self.analyze_market(query)
    
    async def get_technical_analysis(self, query: str = "기술적 분석") -> Dict[str, Any]:
        return await self.analyze_market(query)
    
    async def get_fundamental_analysis(self, query: str = "기본적 분석") -> Dict[str, Any]:
        return await self.analyze_market(query)