from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools

from .base_client import BaseClient
from .. import schemas
from ..config import settings



class MarketClient(BaseClient):
    async def get_analysis(self, params: schemas.MarketAnalysisRequest) -> schemas.MarketAnalysisResponse:
        """
        Requests market analysis from the market-analysis-team API.
        """
        response_data = await self._request(
            method="GET",
            endpoint="/analyze",
            params=params.model_dump()
        )
        return schemas.MarketAnalysisResponse(**response_data)

class MarketMCPClient():
    def __init__(self):
        ...

    async def get_tools(self):
        async with sse_client(url=settings.MARKET_ANALYSIS_API_BASE_URL) as (read, write):
            async with ClientSession(read, write) as session:
                tools = await load_mcp_tools(session)
        return tools


        

market_client = MarketClient(
    service_name="Market Analysis",
    base_url=settings.MARKET_ANALYSIS_API_BASE_URL
) 