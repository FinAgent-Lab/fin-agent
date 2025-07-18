import httpx
from typing import Optional, Dict, Any

from ..config import settings


class BaseClient:
    def __init__(self, service_name: str, base_url: str):
        self.service_name = service_name
        self.base_url = base_url

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """A generic async request maker."""
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method, url=url, params=params, json=json, timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            # Log the error properly in a real application
            # For now, re-raise as a generic exception
            raise Exception(f"API request failed to {self.service_name}: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"API request to {self.service_name} returned an error: "
                f"{e.response.status_code} {e.response.text}"
            ) 

    