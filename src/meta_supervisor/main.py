from fastapi import FastAPI

from .routers import api

app = FastAPI(
    title="Meta Supervisor",
    description="Orchestration agent for Fin-Agent services.",
    version="0.1.0",
)

app.include_router(api.router, prefix="/api")


@app.get("/", tags=["Health Check"])
async def root():
    """
    Root endpoint with basic information.
    """
    return {
        "service": "Meta Supervisor",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Comprehensive health check endpoint for monitoring and Docker health checks.
    """
    from datetime import datetime
    import os
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "Meta Supervisor",
        "version": "0.1.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "checks": {}
    }
    
    # Check if required environment variables are set
    required_env_vars = ["OPENAI_API_KEY", "MARKET_ANALYSIS_API_BASE_URL", "TRADING_STRATEGY_API_BASE_URL"]
    env_check = {"status": "healthy", "missing": []}
    
    for var in required_env_vars:
        if not os.getenv(var):
            env_check["missing"].append(var)
    
    if env_check["missing"]:
        env_check["status"] = "warning"
        health_data["status"] = "degraded"
    
    health_data["checks"]["environment"] = env_check
    
    # Basic service availability check
    try:
        from .services.market_analysis_service import MarketAnalysisService
        MarketAnalysisService()  # Verify instantiation is possible
        health_data["checks"]["market_analysis_service"] = {"status": "healthy", "available": True}
    except Exception as e:
        health_data["checks"]["market_analysis_service"] = {"status": "error", "error": str(e)}
        health_data["status"] = "unhealthy"
    
    return health_data 