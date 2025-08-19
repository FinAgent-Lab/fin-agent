from typing import Any, Dict
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from .market_analysis_service import MarketAnalysisService

# from .trading_service import TradingService  # 외부 API 미구현으로 주석처리
from ..tools import MarketAnalysisTool  # , TradingTool  # TradingTool 주석처리


class AgentService:
    def __init__(
        self,
        market_service: MarketAnalysisService = None,
        # trading_service: TradingService = None,  # 외부 API 미구현으로 주석처리
        llm: ChatOpenAI = None,
    ):
        self.market_service = market_service or MarketAnalysisService()
        # self.trading_service = trading_service or TradingService()  # 외부 API 미구현으로 주석처리
        self.llm = llm
        self._agent = None

    async def get_agent(self):
        if self._agent is None:
            tools = [
                MarketAnalysisTool(),
                # TradingTool()  # 외부 API 미구현으로 주석처리
            ]
            
            system_prompt = """You are a professional financial analysis assistant specializing in stock market analysis and investment research.

**Your Role:**
- Provide accurate, data-driven financial analysis and market insights
- Use available tools to gather real-time market information when needed
- Explain complex financial concepts in clear, accessible language
- Support both Korean and English queries with appropriate responses

**Tool Usage Guidelines:**
- Use the market_analysis tool for specific stock analysis, market trends, and technical/fundamental analysis
- Always verify stock symbols/codes before making analysis requests
- Provide context and interpretation of the data returned by tools
- When tools are unavailable, clearly state the limitations of your response

**Response Standards:**
- Structure responses with clear sections (Overview, Analysis, Key Points, etc.)
- Include relevant metrics, trends, and technical indicators when available
- Provide balanced perspectives including both opportunities and risks
- Use bullet points and formatting for better readability

**Important Disclaimers:**
- All information provided is for educational and informational purposes only
- This is not financial advice or investment recommendations
- Users should conduct their own research and consult financial advisors
- Past performance does not guarantee future results
- Market data may not be real-time and could have delays

**Communication Style:**
- Professional yet approachable tone
- Factual and objective analysis
- Clear explanations of technical terms
- Responsive to user's specific questions and concerns

Always prioritize accuracy, transparency, and user education in your responses."""
            
            self._agent = create_react_agent(
                model=self.llm,
                tools=tools,
                prompt=system_prompt,
            )
        return self._agent

    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process user query directly with agent."""
        agent = await self.get_agent()
        result = await agent.ainvoke({"messages": [("user", query)]})
        return {"intent": "agent_response", "result": result}

    async def query_with_agent(self, query: str) -> Dict[str, Any]:
        agent = await self.get_agent()
        result = await agent.ainvoke({"messages": [("user", query)]})
        return result

    async def analyze_market_with_context(
        self, symbol: str, query: str
    ) -> Dict[str, Any]:
        market_data = await self.market_service.analyze_market(symbol)

        context_query = f"""
        다음 시장 데이터를 바탕으로 질문에 답해주세요:
        주식코드: {symbol}
        시장 데이터: {market_data}
        
        질문: {query}
        """

        return await self.query_with_agent(context_query)
