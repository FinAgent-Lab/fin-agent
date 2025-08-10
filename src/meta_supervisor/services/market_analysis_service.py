import httpx
from typing import Any, Dict, Optional
from pydantic import BaseModel
import os
from datetime import datetime
import logging
from ..config import settings

logger = logging.getLogger(__name__)


class QueryRequest(BaseModel):
    """External market analysis API request format"""

    query: str
    model: Optional[str] = os.getenv("MAIN_LLM_MODEL", "gpt-4o-mini")
    temperature: Optional[float] = 0.2


class QueryResponse(BaseModel):
    """External market analysis API response format"""

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
        print(url)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method, url=url, params=params, json=json, timeout=180.0
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
        """Simple proxy to external market analysis API."""
        logger.info(f"Market analysis request: {query}")

        try:
            request_data = QueryRequest(
                query=query,
                # model=os.getenv("MAIN_LLM_MODEL", "gpt-4o-mini"),
                temperature=0.2,
            )

            response_data = await self._request(
                method="POST", endpoint="/api/query", json=request_data.model_dump()
            )

            response = QueryResponse(**response_data)

            logger.info(f"API response successful - {len(response.answer)} chars")
            return {
                "query": query,
                "answer": response.answer,
                "timestamp": response.timestamp,
            }

        except Exception as e:
            logger.warning(f"External API failed: {e}")
            return self._simple_fallback(query, str(e))

    def _simple_fallback(self, query: str, error: str) -> Dict[str, Any]:
        """Simple fallback when external API is unavailable."""
        logger.info(f"Generating simple fallback for query: {query}")
        
        return {
            "query": query,
            "answer": "Market analysis service is temporarily unavailable. Please try again later.",
            "timestamp": datetime.now().isoformat(),
            "source": "fallback",
            "status": "api_unavailable",
            "error": error
        }

    async def get_market_data(self, query: str = "Market data analysis") -> Dict[str, Any]:
        return await self.analyze_market(query)

    async def get_technical_analysis(self, query: str = "Technical analysis") -> Dict[str, Any]:
        return await self.analyze_market(query)

    async def get_fundamental_analysis(self, query: str = "Fundamental analysis") -> Dict[str, Any]:
        return await self.analyze_market(query)
