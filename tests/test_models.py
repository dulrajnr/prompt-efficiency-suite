import pytest

from prompt_efficiency_suite.models import (
    ModelType,
    PromptAnalysis,
    PromptMetrics,
    TestCase,
    TestResult,
    TestSuite,
)


def test_prompt_analysis_initialization() -> None:
    """Test prompt analysis initialization."""
    metrics = PromptMetrics(
        token_count=100,
        word_count=50,
        sentence_count=5,
        avg_word_length=4.5,
        quality_score=0.8,
    )
    analysis = PromptAnalysis(
        prompt="Test prompt",
        metrics=metrics,
        suggestions=["suggestion1", "suggestion2"],
    )
    assert analysis.prompt == "Test prompt"
    assert analysis.metrics == metrics
    assert analysis.suggestions == ["suggestion1", "suggestion2"]


def test_prompt_metrics_initialization() -> None:
    """Test prompt metrics initialization."""
    metrics = PromptMetrics(
        token_count=100,
        word_count=50,
        sentence_count=5,
        avg_word_length=4.5,
        quality_score=0.8,
    )
    assert metrics.token_count == 100
    assert metrics.word_count == 50
    assert metrics.sentence_count == 5
    assert metrics.avg_word_length == 4.5
    assert metrics.quality_score == 0.8


def test_test_case_initialization() -> None:
    """Test test case initialization."""
    test_case = TestCase(
        name="test_case_1",
        expected_response="expected response",
        expected_patterns=["pattern1", "pattern2"],
        expected_tokens=10,
        timeout=5.0,
    )
    assert test_case.name == "test_case_1"
    assert test_case.expected_response == "expected response"
    assert test_case.expected_patterns == ["pattern1", "pattern2"]
    assert test_case.expected_tokens == 10
    assert test_case.timeout == 5.0


def test_test_suite_initialization() -> None:
    """Test test suite initialization."""
    test_suite = TestSuite(
        description="Test suite", model=ModelType.GPT4, max_retries=3, timeout=10.0
    )
    assert test_suite.description == "Test suite"
    assert test_suite.model == ModelType.GPT4
    assert test_suite.max_retries == 3
    assert test_suite.timeout == 10.0
    assert isinstance(test_suite.test_cases, list)
    assert len(test_suite.test_cases) == 0


def test_test_result_initialization() -> None:
    """Test test result initialization."""
    result = TestResult(
        success=True, response="test response", execution_time=1.5, token_usage=100
    )
    assert result.success is True
    assert result.response == "test response"
    assert result.execution_time == 1.5
    assert result.token_usage == 100
