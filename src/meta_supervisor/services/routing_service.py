from .market_analysis_service import MarketAnalysisService
from .trading_service import TradingService
from .. import schemas
from typing import Any

# Mapping from intent to the corresponding service and method
INTENT_TO_SERVICE_MAP = {
    "market_analysis": {"service": MarketAnalysisService(), "method": "analyze_market"},
    "strategy_creation": {"service": TradingService(), "method": "create_strategy"},
    # "backtest" and "strategy_execution" can be added later
}


async def route_request(analysis: schemas.IntentAnalysisResult) -> Any:
    """
    Routes the request to the appropriate backend service based on intent.
    """
    intent = analysis.intent
    if intent not in INTENT_TO_SERVICE_MAP:
        return {"error": f"Intent '{intent}' is not supported."}

    service_info = INTENT_TO_SERVICE_MAP[intent]
    service = service_info["service"]
    method_name = service_info["method"]
    method_to_call = getattr(service, method_name)

    # This is a simplified way to create request params from entities.
    # In a real scenario, this would be more robust.
    params_data = analysis.entities

    # Here we would map entities to the appropriate service method.
    if intent == "market_analysis":
        symbol = params_data.get("stock_code")
        if not symbol:
            return {"error": "Stock symbol (stock_code) not found in the query."}

        analysis_type = params_data.get("analysis_type", "technical")
        response = await method_to_call(symbol, analysis_type)
    elif intent == "strategy_creation":
        response = await method_to_call(params_data)
    else:
        # Fallback for unhandled intents that are in the map
        return {"error": f"Service method for intent '{intent}' not implemented."}

    return response
