import httpx
from typing import Any, Dict, Optional
from pydantic import BaseModel
import os
from datetime import datetime
import logging
from ..config import settings

logger = logging.getLogger(__name__)


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
        """외부 마켓 분석 API와 통신하여 분석 결과를 가져옵니다."""
        logger.info(f"Market analysis request received: {query}")

        try:
            request_data = QueryRequest(
                query=query,
                model=os.getenv("MAIN_LLM_MODEL", "gpt-4o-mini"),
                temperature=0.2,
            )

            logger.info(f"Attempting external API call to: {self.base_url}/query")
            response_data = await self._request(
                method="POST", endpoint="/query", json=request_data.model_dump()
            )

            response = QueryResponse(**response_data)

            result = {
                "query": query,
                "answer": response.answer,
                "timestamp": response.timestamp,
            }

            logger.info(
                f"External API response successful - Answer length: {len(response.answer)} chars"
            )
            return result

        except Exception as e:
            logger.warning(
                f"External API call failed: {str(e)}, using fallback analysis"
            )
            # API 연결 실패 시 fallback 응답 제공
            fallback_result = await self._get_fallback_analysis(query)
            logger.info(
                f"Fallback analysis generated - Answer length: {len(fallback_result['answer'])} chars"
            )
            return fallback_result

    async def _get_fallback_analysis(self, query: str) -> Dict[str, Any]:
        """API 연결 실패 시 기본 분석 결과를 제공합니다."""
        logger.info(f"Generating fallback analysis for query: {query}")

        # 쿼리에서 종목명 추출 시도
        stock_symbols = {
            "테슬라": "TSLA",
            "삼성전자": "005930",
            "애플": "AAPL",
            "구글": "GOOGL",
            "마이크로소프트": "MSFT",
            "엔비디아": "NVDA",
            "아마존": "AMZN",
            "넷플릭스": "NFLX",
            "메타": "META",
        }

        detected_stock = None
        for stock_name, symbol in stock_symbols.items():
            if stock_name in query:
                detected_stock = {"name": stock_name, "symbol": symbol}
                logger.info(f"Detected stock: {stock_name} ({symbol})")
                break

        # 분석 유형 감지
        analysis_type = "종합 분석"
        if "기술적" in query or "차트" in query:
            analysis_type = "기술적 분석"
        elif "기본적" in query or "펀더멘털" in query:
            analysis_type = "기본적 분석"
        elif "전망" in query or "예측" in query:
            analysis_type = "시장 전망"

        logger.info(f"Analysis type determined: {analysis_type}")

        # 기본 분석 결과 생성
        if detected_stock:
            analysis_result = f"""
**{detected_stock["name"]} ({detected_stock["symbol"]}) {analysis_type}**

⚠️ 현재 외부 시장 분석 API에 연결할 수 없어 기본 분석을 제공합니다.

**주요 포인트:**
• 실시간 데이터 분석을 위해서는 API 연결이 필요합니다
• 투자 결정 전 최신 시장 데이터를 별도로 확인하세요
• 전문적인 투자 조언은 금융 전문가와 상담하시기 바랍니다

**권장사항:**
1. 공식 금융 데이터 제공업체에서 최신 정보 확인
2. 다양한 분석 도구와 지표 활용
3. 리스크 관리 계획 수립

*이 분석은 API 연결 제한으로 인한 기본 정보입니다.*
            """.strip()
        else:
            analysis_result = f"""
**시장 분석 결과**

⚠️ 현재 외부 시장 분석 API에 연결할 수 없어 기본 분석을 제공합니다.

**요청 분석:** {query}

**일반적인 시장 분석 가이드:**
• 기술적 분석: 차트 패턴, 거래량, 이동평균선 등 분석
• 기본적 분석: 재무제표, 실적, 업계 동향 등 분석  
• 종합 분석: 기술적/기본적 분석을 통합한 투자 판단

**권장사항:**
1. 실시간 데이터를 위한 전문 분석 플랫폼 이용
2. 여러 정보원을 통한 교차 검증
3. 투자 전 전문가 상담 권장

*정확한 분석을 위해서는 API 연결이 복구되어야 합니다.*
            """.strip()

        return {
            "query": query,
            "answer": analysis_result,
            "timestamp": datetime.now().isoformat(),
            "source": "fallback_analysis",
            "status": "api_unavailable",
        }

    async def get_market_data(self, query: str = "시장 데이터 분석") -> Dict[str, Any]:
        return await self.analyze_market(query)

    async def get_technical_analysis(
        self, query: str = "기술적 분석"
    ) -> Dict[str, Any]:
        return await self.analyze_market(query)

    async def get_fundamental_analysis(
        self, query: str = "기본적 분석"
    ) -> Dict[str, Any]:
        return await self.analyze_market(query)
