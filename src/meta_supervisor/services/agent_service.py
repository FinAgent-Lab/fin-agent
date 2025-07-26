from typing import Any, Dict
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from .market_analysis_service import MarketAnalysisService
# from .trading_service import TradingService  # 외부 API 미구현으로 주석처리
# from .nlu_service import analyze  # 외부 기능 미구현으로 주석처리
from ..tools import MarketAnalysisTool  # , TradingTool  # TradingTool 주석처리


class AgentService:
    def __init__(
        self,
        market_service: MarketAnalysisService = None,
        # trading_service: TradingService = None,  # 외부 API 미구현으로 주석처리
        llm: ChatOpenAI = None
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
            self._agent = create_react_agent(
                model=self.llm,
                tools=tools,
            )
        return self._agent
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        # NLU 서비스가 미구현이므로 주석처리하고 직접 에이전트로 처리
        # analysis_result = analyze(query)
        # intent = analysis_result.intent
        # entities = analysis_result.entities
        
        # if intent == "market_analysis":
        #     symbol = entities.get("stock_code")
        #     if not symbol:
        #         return {"error": "주식 코드를 찾을 수 없습니다."}
        #     
        #     result = await self.market_service.analyze_market(
        #         symbol=symbol,
        #         analysis_type=entities.get("analysis_type", "technical")
        #     )
        #     return {"intent": intent, "result": result}
        # 
        # elif intent in ["strategy_creation", "strategy_execution"]:
        #     result = await self.trading_service.create_strategy(entities)
        #     return {"intent": intent, "result": result}
        # 
        # else:
        #     agent = await self.get_agent()
        #     result = await agent.ainvoke({"messages": [("user", query)]})
        #     return {"intent": "agent_response", "result": result}
        
        # 현재는 모든 쿼리를 에이전트로 직접 처리
        agent = await self.get_agent()
        result = await agent.ainvoke({"messages": [("user", query)]})
        return {"intent": "agent_response", "result": result}
    
    async def query_with_agent(self, query: str) -> Dict[str, Any]:
        agent = await self.get_agent()
        result = await agent.ainvoke({"messages": [("user", query)]})
        return result
    
    async def analyze_market_with_context(self, symbol: str, query: str) -> Dict[str, Any]:
        market_data = await self.market_service.analyze_market(symbol)
        
        context_query = f"""
        다음 시장 데이터를 바탕으로 질문에 답해주세요:
        주식코드: {symbol}
        시장 데이터: {market_data}
        
        질문: {query}
        """
        
        return await self.query_with_agent(context_query)