"""API endpoints for prompt optimization."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..optimizer import PromptOptimizer

router = APIRouter()


class OptimizeRequest(BaseModel):
    """Request model for prompt optimization."""

    prompt: str
    optimization_targets: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None


class OptimizeResponse(BaseModel):
    """Response model for prompt optimization."""

    optimized_prompt: str
    improvements: List[str]
    metrics: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class BatchOptimizeRequest(BaseModel):
    """Request model for batch prompt optimization."""

    prompts: List[str]
    optimization_targets: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None


class BatchOptimizeResponse(BaseModel):
    """Response model for batch prompt optimization."""

    results: List[OptimizeResponse]
    summary: Dict[str, Any]


class OptimizationHistory(BaseModel):
    """Model for optimization history entry."""

    original_prompt: str
    optimized_prompt: str
    timestamp: datetime
    metrics: Dict[str, Any]
    optimization_targets: List[str]


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_prompt(request: OptimizeRequest) -> OptimizeResponse:
    """Optimize a prompt for efficiency.

    Args:
        request: OptimizeRequest containing prompt and options

    Returns:
        OptimizeResponse with optimized prompt and metrics
    """
    try:
        optimizer = PromptOptimizer()
        result = optimizer.optimize(
            request.prompt,
            optimization_targets=request.optimization_targets,
            options=request.options,
        )
        return OptimizeResponse(
            optimized_prompt=result.optimized_prompt,
            improvements=result.improvements,
            metrics=result.metrics,
            metadata=result.metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize/batch", response_model=BatchOptimizeResponse)
async def optimize_prompts_batch(
    request: BatchOptimizeRequest,
) -> BatchOptimizeResponse:
    """Optimize multiple prompts in batch.

    Args:
        request: BatchOptimizeRequest containing list of prompts and options

    Returns:
        BatchOptimizeResponse with results and summary
    """
    try:
        optimizer = PromptOptimizer()
        results = []
        total_improvements = 0
        total_token_reduction = 0

        for prompt in request.prompts:
            result = optimizer.optimize(
                prompt,
                optimization_targets=request.optimization_targets,
                options=request.options,
            )
            results.append(
                OptimizeResponse(
                    optimized_prompt=result.optimized_prompt,
                    improvements=result.improvements,
                    metrics=result.metrics,
                    metadata=result.metadata,
                )
            )
            total_improvements += len(result.improvements)
            if "token_reduction" in result.metrics:
                total_token_reduction += result.metrics["token_reduction"]

        summary = {
            "total_prompts": len(request.prompts),
            "total_improvements": total_improvements,
            "average_improvements": (
                total_improvements / len(request.prompts) if request.prompts else 0
            ),
            "total_token_reduction": total_token_reduction,
            "average_token_reduction": (
                total_token_reduction / len(request.prompts) if request.prompts else 0
            ),
        }

        return BatchOptimizeResponse(results=results, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/targets/available")
async def get_available_targets() -> Dict[str, Any]:
    """Get information about available optimization targets.

    Returns:
        Dictionary describing available optimization targets
    """
    return {
        "targets": {
            "clarity": "Improve prompt clarity and specificity",
            "efficiency": "Reduce token usage while maintaining effectiveness",
            "structure": "Improve prompt structure and organization",
            "redundancy": "Remove redundant content and phrases",
            "complexity": "Simplify complex language and structures",
        },
        "default_targets": ["clarity", "efficiency"],
        "recommendations": {
            "short_prompts": ["clarity", "structure"],
            "long_prompts": ["efficiency", "redundancy"],
            "complex_prompts": ["clarity", "complexity"],
            "technical_prompts": ["structure", "clarity"],
        },
    }
