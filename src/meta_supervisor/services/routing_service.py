from ..clients.trading_client import trading_client
from ..clients.market_client import market_client
from .. import schemas
from typing import Any

# Mapping from intent to the corresponding client and method
INTENT_TO_CLIENT_MAP = {
    "market_analysis": {
        "client": market_client,
        "method": "get_analysis"
    },
    "strategy_creation": {
        "client": trading_client,
        "method": "create_strategy"
    },
    # "backtest" and "strategy_execution" can be added later
}


async def route_request(analysis: schemas.IntentAnalysisResult) -> Any:
    """
    Routes the request to the appropriate backend client based on intent.
    """
    intent = analysis.intent
    if intent not in INTENT_TO_CLIENT_MAP:
        return {"error": f"Intent '{intent}' is not supported."}

    client_info = INTENT_TO_CLIENT_MAP[intent]
    client = client_info["client"]
    method_name = client_info["method"]
    method_to_call = getattr(client, method_name)

    # This is a simplified way to create request params from entities.
    # In a real scenario, this would be more robust.
    params_data = analysis.entities
    
    # Here we would map entities to the correct Pydantic request model.
    # For now, we'll assume the entities map directly.
    if intent == "market_analysis":
        symbol = params_data.get("stock_code")
        if not symbol:
            return {"error": "Stock symbol (stock_code) not found in the query."}

        # Provide a default for the missing field
        request_model = schemas.MarketAnalysisRequest(
            symbol=symbol,
            analysis_type=params_data.get("analysis_type", "technical")
        )
    elif intent == "strategy_creation":
        request_model = schemas.TradingStrategyRequest(parameters=params_data)
    else:
        # Fallback for unhandled intents that are in the map
        return {"error": f"Request model for intent '{intent}' not implemented."}

    response = await method_to_call(request_model)
    return response 