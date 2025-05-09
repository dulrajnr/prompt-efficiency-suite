import pytest
from prompt_efficiency_suite.tester import PromptTester, TestCase, TestSuite, TestResult
from prompt_efficiency_suite.model_translator import ModelType

@pytest.fixture
def tester():
    return PromptTester()

@pytest.fixture
def sample_test_case():
    return TestCase(
        name="Test Case 1",
        prompt="What is 2+2?",
        expected_response="4",
        expected_patterns=["number", "sum"],
        expected_tokens=10,
        timeout=5.0
    )

@pytest.fixture
def sample_test_suite(sample_test_case):
    return TestSuite(
        name="Math Test Suite",
        description="Test basic math operations",
        test_cases=[sample_test_case],
        model=ModelType.GPT4,
        max_retries=3,
        timeout=10.0
    )

def test_initialization(tester):
    """Test that the tester initializes correctly."""
    assert isinstance(tester.test_history, list)
    assert len(tester.test_history) == 0

def test_run_test_case(tester, sample_test_case):
    """Test running a single test case."""
    result = tester.run_test_case(
        test_case=sample_test_case,
        model=ModelType.GPT4
    )
    
    assert isinstance(result, TestResult)
    assert isinstance(result.success, bool)
    assert isinstance(result.response, str)
    assert isinstance(result.execution_time, float)
    assert isinstance(result.token_usage, dict)
    assert "prompt" in result.token_usage
    assert "completion" in result.token_usage

def test_run_test_suite(tester, sample_test_suite):
    """Test running a complete test suite."""
    results = tester.run_test_suite(sample_test_suite)
    
    assert isinstance(results, list)
    assert len(results) == len(sample_test_suite.test_cases)
    for result in results:
        assert isinstance(result, TestResult)

def test_validate_response_exact_match(tester, sample_test_case):
    """Test response validation with exact match."""
    # Test exact match
    assert tester._validate_response("4", sample_test_case)
    assert not tester._validate_response("5", sample_test_case)

def test_validate_response_patterns(tester, sample_test_case):
    """Test response validation with patterns."""
    # Test pattern matching
    assert tester._validate_response("The number 4 is the sum", sample_test_case)
    assert not tester._validate_response("The answer is 4", sample_test_case)

def test_validate_response_tokens(tester, sample_test_case):
    """Test response validation with token count."""
    # Test token count
    assert tester._validate_response("4", sample_test_case)  # 1 token
    assert not tester._validate_response(
        "The answer is four and this is a very long response that exceeds the token limit",
        sample_test_case
    )

def test_test_history(tester, sample_test_case):
    """Test test history functionality."""
    # Run a test
    result = tester.run_test_case(
        test_case=sample_test_case,
        model=ModelType.GPT4
    )
    
    # Check history
    history = tester.get_test_history()
    assert len(history) == 1
    assert history[0][0] == sample_test_case
    assert history[0][1] == result
    
    # Clear history
    tester.clear_test_history()
    assert len(tester.get_test_history()) == 0

def test_retry_mechanism(tester, sample_test_case):
    """Test retry mechanism for failed tests."""
    # Create a test case that will fail
    failing_case = TestCase(
        name="Failing Test",
        prompt="This will fail",
        expected_response="This should never match",
        timeout=1.0
    )
    
    result = tester.run_test_case(
        test_case=failing_case,
        model=ModelType.GPT4,
        max_retries=3
    )
    
    assert not result.success
    assert result.error is not None

def test_timeout_handling(tester):
    """Test timeout handling."""
    # Create a test case with very short timeout
    timeout_case = TestCase(
        name="Timeout Test",
        prompt="This should timeout",
        timeout=0.001  # Very short timeout
    )
    
    result = tester.run_test_case(
        test_case=timeout_case,
        model=ModelType.GPT4
    )
    
    assert not result.success
    assert result.error is not None

def test_metadata_handling(tester):
    """Test metadata handling in test cases and results."""
    metadata = {"key": "value", "number": 42}
    
    test_case = TestCase(
        name="Metadata Test",
        prompt="Test prompt",
        metadata=metadata
    )
    
    result = tester.run_test_case(
        test_case=test_case,
        model=ModelType.GPT4
    )
    
    assert result.metadata is not None
    assert isinstance(result.metadata, dict)

def test_multiple_test_cases(tester):
    """Test running multiple test cases in a suite."""
    test_cases = [
        TestCase(
            name=f"Test Case {i}",
            prompt=f"Test prompt {i}",
            expected_response=f"Response {i}"
        )
        for i in range(3)
    ]
    
    test_suite = TestSuite(
        name="Multiple Test Suite",
        description="Test multiple cases",
        test_cases=test_cases,
        model=ModelType.GPT4
    )
    
    results = tester.run_test_suite(test_suite)
    
    assert len(results) == len(test_cases)
    for result in results:
        assert isinstance(result, TestResult) 