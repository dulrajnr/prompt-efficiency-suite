"""API endpoints for prompt analysis."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from ..analyzer import PromptAnalyzer, AnalysisResult

router = APIRouter()

class AnalyzeRequest(BaseModel):
    """Request model for prompt analysis."""
    prompt: str
    options: Optional[Dict[str, Any]] = None

class BatchAnalyzeRequest(BaseModel):
    """Request model for batch prompt analysis."""
    prompts: List[str]
    options: Optional[Dict[str, Any]] = None

class BatchAnalyzeResponse(BaseModel):
    """Response model for batch prompt analysis."""
    results: List[AnalysisResult]
    summary: Dict[str, Any]

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_prompt(request: AnalyzeRequest) -> AnalysisResult:
    """Analyze a prompt for efficiency metrics.
    
    Args:
        request: AnalyzeRequest containing prompt and options
        
    Returns:
        AnalysisResult with metrics and suggestions
    """
    try:
        analyzer = PromptAnalyzer()
        result = analyzer.analyze(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/batch", response_model=BatchAnalyzeResponse)
async def analyze_prompts_batch(request: BatchAnalyzeRequest) -> BatchAnalyzeResponse:
    """Analyze multiple prompts in batch.
    
    Args:
        request: BatchAnalyzeRequest containing list of prompts and options
        
    Returns:
        BatchAnalyzeResponse with results and summary
    """
    try:
        analyzer = PromptAnalyzer()
        results = []
        total_tokens = 0
        total_complexity = 0
        total_clarity = 0
        
        for prompt in request.prompts:
            result = analyzer.analyze(prompt)
            results.append(result)
            total_tokens += result.metrics.token_count
            total_complexity += result.metrics.complexity_score
            total_clarity += result.metrics.clarity_score
        
        num_prompts = len(request.prompts)
        summary = {
            "total_prompts": num_prompts,
            "average_tokens": total_tokens / num_prompts if num_prompts > 0 else 0,
            "average_complexity": total_complexity / num_prompts if num_prompts > 0 else 0,
            "average_clarity": total_clarity / num_prompts if num_prompts > 0 else 0,
            "total_warnings": sum(len(r.warnings) for r in results),
            "total_suggestions": sum(len(r.suggestions) for r in results)
        }
        
        return BatchAnalyzeResponse(results=results, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/available")
async def get_available_metrics() -> Dict[str, Any]:
    """Get information about available analysis metrics.
    
    Returns:
        Dictionary describing available metrics and their descriptions
    """
    return {
        "metrics": {
            "token_count": "Number of tokens in the prompt",
            "character_count": "Number of characters in the prompt",
            "word_count": "Number of words in the prompt",
            "complexity_score": "Score indicating prompt complexity (0-1)",
            "redundancy_score": "Score indicating prompt redundancy (0-1)",
            "clarity_score": "Score indicating prompt clarity (0-1)",
            "efficiency_score": "Overall efficiency score (0-1)"
        },
        "scores": {
            "complexity": "Higher score indicates more complex language and structure",
            "redundancy": "Higher score indicates more redundant content",
            "clarity": "Higher score indicates clearer and more specific instructions",
            "efficiency": "Higher score indicates better overall prompt efficiency"
        }
    } 