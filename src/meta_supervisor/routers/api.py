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


@router.post("/query", response_model=schemas.ResponseBody, tags=["Supervisor"])
async def query(
    request: schemas.UserRequest,
    agent_service: AgentService = Depends(get_agent_service),
):
    """
    Queries using the agent service with integrated tools and services.
    """
    try:
        result = await agent_service.process_query(request.query)
        
        # 안전한 문자열 추출
        raw_result = result.get("result")
        if isinstance(raw_result, str):
            answer = raw_result
        elif isinstance(raw_result, dict) and "messages" in raw_result:
            # AI 메시지 내용 추출
            messages = raw_result["messages"]
            if messages and hasattr(messages[-1], 'content'):
                answer = messages[-1].content
            else:
                answer = str(raw_result)
        else:
            answer = str(raw_result) if raw_result is not None else "응답을 처리할 수 없습니다."
        
        return schemas.ResponseBody(answer=answer)
    except Exception as e:
        return schemas.ResponseBody(
            answer=str(e),
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
