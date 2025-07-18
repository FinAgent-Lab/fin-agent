from .base_client import BaseClient
from ..config import settings
from .. import schemas
from typing import Any, Dict


class TradingClient(BaseClient):
    async def create_strategy(self, params: schemas.TradingStrategyRequest) -> schemas.TradingStrategyResponse:
        """
        Requests strategy creation from the trading-strategy-team API.
        """
        response_data = await self._request(
            method="POST",
            endpoint="/strategies",
            json=params.model_dump()
        )
        return schemas.TradingStrategyResponse(**response_data)


trading_client = TradingClient(
    service_name="Trading Strategy",
    base_url=settings.TRADING_STRATEGY_API_BASE_URL
) 