from fastapi import APIRouter, Depends

from src.meta_supervisor import schemas
from src.meta_supervisor.services import nlu_service, routing_service
from src.meta_supervisor.services.agent_service import AgentService
from src.meta_supervisor.dependencies import get_agent_service

router = APIRouter()


@router.post("/process", response_model=schemas.CommonResponse, tags=["Supervisor"])
async def process_request(request: schemas.UserRequest):
    """
    Processes the user's natural language query, routes it, and returns the result.
    """
    try:
        # 1. Analyze intent and entities
        analysis_result = nlu_service.analyze(request.query)

        # 2. Route the request to the appropriate service
        final_result = await routing_service.route_request(analysis_result)

        return schemas.CommonResponse(data=final_result)
    except Exception as e:
        # Catch all exceptions for now and return a standardized error
        return schemas.CommonResponse(
            success=False,
            data=None,
            error_code="INTERNAL_SERVER_ERROR",
            error_message=str(e),
        )


@router.post("/query", response_model=schemas.CommonResponse, tags=["Supervisor"])
async def query(
    request: schemas.UserRequest,
    agent_service: AgentService = Depends(get_agent_service),
):
    """
    Queries using the agent service with integrated tools and services.
    """
    try:
        result = await agent_service.process_query(request.query)
        return schemas.CommonResponse(data=result)
    except Exception as e:
        return schemas.CommonResponse(
            success=False,
            data=None,
            error_code="INTERNAL_SERVER_ERROR",
            error_message=str(e),
        )


@router.post("/agent", response_model=schemas.CommonResponse, tags=["Supervisor"])
async def agent_query(
    request: schemas.UserRequest,
    agent_service: AgentService = Depends(get_agent_service),
):
    """
    Direct agent query without intent analysis.
    """
    try:
        result = await agent_service.query_with_agent(request.query)
        return schemas.CommonResponse(data=result)
    except Exception as e:
        return schemas.CommonResponse(
            success=False,
            data=None,
            error_code="INTERNAL_SERVER_ERROR",
            error_message=str(e),
        )
