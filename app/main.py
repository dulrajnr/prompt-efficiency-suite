import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .cicd.integration import CICDIntegration
from .trimmer.domain_aware import DomainAwareTrimmer

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Prompt Efficiency Suite",
    description="A unified platform for optimizing, managing, and monitoring LLM prompts",
    version="1.0.0",
)

# Initialize services
dictionary_path = os.getenv("DICTIONARY_PATH", "data/dicts")
trimmer = DomainAwareTrimmer(dictionary_path=dictionary_path)
cicd = CICDIntegration(
    max_tokens=int(os.getenv("MAX_DEFAULT_TOKENS", "1800")),
    build_failure=os.getenv("BUILD_FAILURE", "true").lower() == "true",
    dictionary_path=dictionary_path,
)


class TrimRequest(BaseModel):
    prompt: str
    domain: str
    min_importance: Optional[float] = 0.7


class TrimResponse(BaseModel):
    trimmed_prompt: str
    tokens_before: int
    tokens_after: int


@app.post("/api/v1/trim", response_model=TrimResponse)
async def trim_prompt(request: TrimRequest):
    try:
        tokens_before = trimmer.get_token_count(request.prompt)
        trimmed_prompt = trimmer.trim_prompt(request.prompt, request.domain, request.min_importance)
        tokens_after = trimmer.get_token_count(trimmed_prompt)

        return TrimResponse(
            trimmed_prompt=trimmed_prompt,
            tokens_before=tokens_before,
            tokens_after=tokens_after,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class BudgetCheckRequest(BaseModel):
    prompt: str


class BudgetCheckResponse(BaseModel):
    token_count: int
    max_tokens: int
    exceeds_budget: bool
    build_failure: bool


@app.post("/api/v1/check-budget", response_model=BudgetCheckResponse)
async def check_prompt_budget(request: BudgetCheckRequest):
    try:
        result = cicd.check_prompt_budget(request.prompt)
        return BudgetCheckResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
