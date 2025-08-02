import httpx
from typing import Any, Dict, Optional
from .. import schemas
from ..config import settings


class TradingService:
    def __init__(self):
        self.base_url = settings.TRADING_STRATEGY_API_BASE_URL

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """HTTP request handler for trading strategy API."""
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method, url=url, params=params, json=json, timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise Exception(f"Trading Strategy API request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"Trading Strategy API returned error: {e.response.status_code} {e.response.text}"
            )

    async def create_strategy(
        self, parameters: Dict[str, Any]
    ) -> schemas.TradingStrategyResponse:
        request = schemas.TradingStrategyRequest(parameters=parameters)
        response_data = await self._request(
            method="POST", endpoint="/strategies", json=request.model_dump()
        )
        return schemas.TradingStrategyResponse(**response_data)

    async def execute_trade(
        self, symbol: str, action: str, quantity: int, price: float = None
    ) -> schemas.TradingStrategyResponse:
        trade_params = {"symbol": symbol, "action": action, "quantity": quantity}
        if price:
            trade_params["price"] = price

        return await self.create_strategy(trade_params)

    async def get_portfolio(self) -> schemas.TradingStrategyResponse:
        portfolio_params = {"action": "get_portfolio"}
        return await self.create_strategy(portfolio_params)

    async def get_positions(
        self, symbol: str = None
    ) -> schemas.TradingStrategyResponse:
        position_params = {"action": "get_positions"}
        if symbol:
            position_params["symbol"] = symbol
        return await self.create_strategy(position_params)
