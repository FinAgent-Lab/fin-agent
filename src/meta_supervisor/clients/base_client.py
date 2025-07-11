import httpx
from typing import Optional, Dict, Any

from ..config import settings


class BaseClient:
    def __init__(self, base_url: str, default_timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = default_timeout

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                # Handle HTTP errors (e.g., 4xx, 5xx)
                print(f"HTTP error occurred: {e}")
                raise
            except httpx.RequestError as e:
                # Handle network-related errors
                print(f"An error occurred while requesting {e.request.url!r}.")
                raise

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        response = await self._request("GET", endpoint, params=params, headers=headers)
        return response.json()

    async def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        response = await self._request("POST", endpoint, json=json, headers=headers)
        return response.json() 