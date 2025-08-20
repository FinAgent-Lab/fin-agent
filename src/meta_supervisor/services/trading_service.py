"""
Trading Service for message-based API communication.
"""
import httpx
from pydantic import BaseModel
from ..config import settings


class QueryRequest(BaseModel):
    """Simple request model for trading API - only contains message."""
    message: str


class QueryResponse(BaseModel):
    """Simple response model from trading API."""
    role: str
    content: str

class TradingService:
    """
    Simple trading service client that communicates with the trading server
    using a message-based API.
    
    Request format: {"message": "..."}
    Response format: {"role": "...", "content": "..."}
    """
    
    def __init__(self):
        self.base_url = settings.TRADING_STRATEGY_API_BASE_URL
        self.timeout = 30.0
    
    async def send_query(self, message: str) -> QueryResponse:
        """
        Send a message query to the trading server.
        
        Args:
            message: The message string to send
            
        Returns:
            QueryResponse with role and content from the server
        """
        request = QueryRequest(message=message)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/agent/trade/chat",
                    json=request.model_dump(),
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                return QueryResponse(**data)
                
        except httpx.RequestError as e:
            return QueryResponse(
                role="error",
                content=f"Trading API request failed: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            return QueryResponse(
                role="error", 
                content=f"Trading API error {e.response.status_code}: {e.response.text}"
            )
        except Exception as e:
            return QueryResponse(
                role="error",
                content=f"Unexpected error: {str(e)}"
            )