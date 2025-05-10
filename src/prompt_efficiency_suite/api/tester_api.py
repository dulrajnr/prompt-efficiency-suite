"""API endpoints for prompt testing."""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..tester import PromptTester, TestCase, TestSuite

router = APIRouter()


class TestRequest(BaseModel):
    """Request model for prompt testing."""

    prompt: str
    test_cases: List[TestCase]
    options: Optional[Dict[str, Any]] = None


class TestResponse(BaseModel):
    """Response model for prompt testing."""

    test_results: List[Dict[str, Any]]
    summary: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


@router.post("/test", response_model=TestResponse)
async def test_prompt(request: TestRequest) -> TestResponse:
    """Test a prompt against test cases.

    Args:
        request: TestRequest containing prompt and test cases

    Returns:
        TestResponse with test results and summary
    """
    try:
        tester = PromptTester()
        suite = TestSuite(test_cases=request.test_cases)
        results = tester.run_tests(request.prompt, suite)

        return TestResponse(
            test_results=[result.to_dict() for result in results.test_results],
            summary=results.get_summary(),
            metadata=results.metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
