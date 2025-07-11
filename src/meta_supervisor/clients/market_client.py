from .base_client import BaseClient
from ..config import settings
from .. import schemas
from typing import Any, Dict


class MarketClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=settings.MARKET_ANALYSIS_API_URL)

    async def get_analysis(self, params: schemas.MarketAnalysisRequest) -> schemas.MarketAnalysisResponse:
        """
        (Placeholder) Sends a request to get market analysis.
        """
        response_data = await self.post(
            endpoint="/analysis",
            json=params.model_dump()
        )
        return schemas.MarketAnalysisResponse(**response_data)


market_client = MarketClient() 