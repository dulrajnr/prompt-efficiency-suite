"""API endpoints for model translation."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..model_translator import ModelTranslator

router = APIRouter()


class TranslateRequest(BaseModel):
    """Request model for prompt translation."""

    prompt: str
    source_model: str
    target_model: str
    options: Optional[Dict[str, Any]] = None


class TranslateResponse(BaseModel):
    """Response model for prompt translation."""

    translated_prompt: str
    metadata: Optional[Dict[str, Any]] = None


class TranslationHistory(BaseModel):
    """Model for translation history entry."""

    original_prompt: str
    translated_prompt: str
    source_model: str
    target_model: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class ModelCompatibility(BaseModel):
    """Model for model compatibility information."""

    source_model: str
    target_model: str
    compatibility_score: float
    potential_issues: List[str]
    recommendations: List[str]


@router.post("/translate", response_model=TranslateResponse)
async def translate_prompt(request: TranslateRequest) -> TranslateResponse:
    """Translate a prompt between different models.

    Args:
        request: TranslateRequest containing prompt and model info

    Returns:
        TranslateResponse with translated prompt
    """
    try:
        translator = ModelTranslator()
        translated = translator.translate(
            request.prompt, request.source_model, request.target_model, request.options
        )
        return TranslateResponse(
            translated_prompt=translated,
            metadata={
                "source_model": request.source_model,
                "target_model": request.target_model,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/compatible")
async def get_compatible_models() -> Dict[str, Any]:
    """Get information about compatible model pairs.

    Returns:
        Dictionary of compatible model pairs and their characteristics
    """
    return {
        "compatible_pairs": [
            {
                "source": "gpt-4",
                "target": "gpt-3.5-turbo",
                "compatibility": "high",
                "notes": "Most features transfer well, but complex reasoning may need simplification",
            },
            {
                "source": "gpt-3.5-turbo",
                "target": "gpt-4",
                "compatibility": "high",
                "notes": "Can add more complexity and detail",
            },
            {
                "source": "claude-2",
                "target": "gpt-4",
                "compatibility": "medium",
                "notes": "May need adjustments for different instruction styles",
            },
        ],
        "model_capabilities": {
            "gpt-4": {
                "max_tokens": 8192,
                "strengths": [
                    "complex reasoning",
                    "detailed analysis",
                    "creative tasks",
                ],
                "limitations": ["cost", "speed"],
            },
            "gpt-3.5-turbo": {
                "max_tokens": 4096,
                "strengths": ["speed", "cost", "general tasks"],
                "limitations": ["complex reasoning", "detailed analysis"],
            },
            "claude-2": {
                "max_tokens": 100000,
                "strengths": ["long context", "detailed analysis"],
                "limitations": ["availability", "cost"],
            },
        },
    }


@router.post("/check-compatibility", response_model=ModelCompatibility)
async def check_model_compatibility(request: TranslateRequest) -> ModelCompatibility:
    """Check compatibility between source and target models for a specific prompt.

    Args:
        request: TranslateRequest containing prompt and model info

    Returns:
        ModelCompatibility with compatibility information
    """
    try:
        translator = ModelTranslator()
        compatibility = translator.check_compatibility(
            request.prompt, request.source_model, request.target_model
        )
        return ModelCompatibility(
            source_model=request.source_model,
            target_model=request.target_model,
            compatibility_score=compatibility.score,
            potential_issues=compatibility.issues,
            recommendations=compatibility.recommendations,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/supported")
async def get_supported_models() -> Dict[str, Any]:
    """Get list of supported models and their characteristics.

    Returns:
        Dictionary of supported models and their details
    """
    return {
        "models": {
            "gpt-4": {
                "type": "chat",
                "context_length": 8192,
                "capabilities": ["chat", "completion", "function_calling"],
                "recommended_use": "Complex tasks requiring deep reasoning",
            },
            "gpt-3.5-turbo": {
                "type": "chat",
                "context_length": 4096,
                "capabilities": ["chat", "completion"],
                "recommended_use": "General purpose tasks and quick responses",
            },
            "claude-2": {
                "type": "chat",
                "context_length": 100000,
                "capabilities": ["chat", "completion", "long_context"],
                "recommended_use": "Tasks requiring long context or detailed analysis",
            },
        },
        "translation_support": {
            "high_compatibility": ["gpt-4", "gpt-3.5-turbo"],
            "medium_compatibility": ["claude-2", "gpt-4"],
            "low_compatibility": ["specialized_models"],
        },
    }
