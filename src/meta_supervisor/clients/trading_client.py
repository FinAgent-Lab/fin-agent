from .base_client import BaseClient
from ..config import settings
from .. import schemas
from typing import Any, Dict


class TradingClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=settings.TRADING_STRATEGY_API_URL)

    async def create_strategy(self, params: schemas.TradingStrategyRequest) -> schemas.TradingStrategyResponse:
        """
        (Placeholder) Sends a request to create a new trading strategy.
        """
        response_data = await self.post(
            endpoint="/strategies",
            json=params.model_dump()
        )
        return schemas.TradingStrategyResponse(**response_data)


trading_client = TradingClient() 