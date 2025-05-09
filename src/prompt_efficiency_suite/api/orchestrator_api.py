"""API endpoints for prompt orchestration."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from ..orchestrator import PromptOrchestrator

router = APIRouter()

class OrchestrateRequest(BaseModel):
    """Request model for prompt orchestration."""
    prompts: List[str]
    orchestration_type: str  # 'sequential', 'parallel', 'conditional'
    options: Optional[Dict[str, Any]] = None

class OrchestrateResponse(BaseModel):
    """Response model for prompt orchestration."""
    orchestrated_prompts: List[str]
    execution_plan: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

@router.post("/orchestrate", response_model=OrchestrateResponse)
async def orchestrate_prompts(request: OrchestrateRequest) -> OrchestrateResponse:
    """Orchestrate multiple prompts.
    
    Args:
        request: OrchestrateRequest containing prompts and options
        
    Returns:
        OrchestrateResponse with orchestrated prompts and plan
    """
    try:
        orchestrator = PromptOrchestrator()
        result = orchestrator.orchestrate(
            request.prompts,
            orchestration_type=request.orchestration_type,
            options=request.options
        )
        return OrchestrateResponse(
            orchestrated_prompts=result.orchestrated_prompts,
            execution_plan=result.execution_plan,
            metadata=result.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 