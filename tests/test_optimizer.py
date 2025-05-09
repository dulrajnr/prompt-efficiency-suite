import pytest
from prompt_efficiency_suite.optimizer import PromptOptimizer, OptimizationConfig, OptimizationResult
from prompt_efficiency_suite.tester import TestCase
from prompt_efficiency_suite.model_translator import ModelType

@pytest.fixture
def optimizer():
    return PromptOptimizer()

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
def sample_config():
    return OptimizationConfig(
        target_model=ModelType.GPT4,
        max_iterations=5,
        min_improvement=0.1,
        token_reduction_target=5,
        execution_time_target=0.5,
        preserve_patterns=["number", "sum"]
    )

def test_initialization(optimizer):
    """Test that the optimizer initializes correctly."""
    assert isinstance(optimizer.optimization_history, list)
    assert len(optimizer.optimization_history) == 0

def test_optimize_prompt(optimizer, sample_test_case, sample_config):
    """Test basic prompt optimization."""
    original_prompt = "Please tell me what is the sum of 2 plus 2?"
    
    result = optimizer.optimize_prompt(
        prompt=original_prompt,
        test_cases=[sample_test_case],
        config=sample_config
    )
    
    assert isinstance(result, OptimizationResult)
    assert result.original_prompt == original_prompt
    assert isinstance(result.optimized_prompt, str)
    assert isinstance(result.improvement_percentage, float)
    assert isinstance(result.token_reduction, int)
    assert isinstance(result.execution_time_reduction, float)
    assert isinstance(result.test_results, list)
    assert len(result.test_results) == 1

def test_optimization_history(optimizer, sample_test_case, sample_config):
    """Test optimization history functionality."""
    # Run an optimization
    result = optimizer.optimize_prompt(
        prompt="Test prompt",
        test_cases=[sample_test_case],
        config=sample_config
    )
    
    # Check history
    history = optimizer.get_optimization_history()
    assert len(history) == 1
    assert history[0][0] == "Test prompt"
    assert history[0][1] == result
    
    # Clear history
    optimizer.clear_optimization_history()
    assert len(optimizer.get_optimization_history()) == 0

def test_optimization_candidates(optimizer):
    """Test optimization candidate generation."""
    prompt = "This is a test prompt. It has multiple sentences. We want to optimize it."
    candidates = optimizer._generate_optimization_candidates(prompt)
    
    assert isinstance(candidates, list)
    assert len(candidates) > 0
    for candidate in candidates:
        assert isinstance(candidate, str)
        assert len(candidate) > 0

def test_preserve_patterns(optimizer):
    """Test pattern preservation in optimization."""
    prompt = "The number 42 is the sum of 40 and 2."
    preserve_patterns = ["number", "sum"]
    
    candidates = optimizer._generate_optimization_candidates(
        prompt,
        preserve_patterns=preserve_patterns
    )
    
    for candidate in candidates:
        assert "number" in candidate
        assert "sum" in candidate

def test_metrics_calculation(optimizer):
    """Test metrics calculation from test results."""
    # Create mock test results
    results = [
        {
            "success": True,
            "response": "4",
            "execution_time": 0.5,
            "token_usage": {"prompt": 10, "completion": 5}
        },
        {
            "success": False,
            "response": "5",
            "execution_time": 0.6,
            "token_usage": {"prompt": 10, "completion": 5}
        }
    ]
    
    metrics = optimizer._calculate_metrics(results)
    
    assert isinstance(metrics, dict)
    assert "total_tokens" in metrics
    assert "total_time" in metrics
    assert "success_rate" in metrics
    assert metrics["success_rate"] == 0.5

def test_improvement_calculation(optimizer):
    """Test improvement calculation."""
    original_metrics = {
        "total_tokens": 100,
        "total_time": 1.0
    }
    
    optimized_metrics = {
        "total_tokens": 80,
        "total_time": 0.8
    }
    
    improvement = optimizer._calculate_improvement(
        original_metrics,
        optimized_metrics
    )
    
    assert isinstance(improvement, float)
    assert 0 <= improvement <= 1

def test_better_candidate_detection(optimizer, sample_config):
    """Test better candidate detection."""
    original_metrics = {
        "total_tokens": 100,
        "total_time": 1.0,
        "success_rate": 0.8
    }
    
    better_metrics = {
        "total_tokens": 80,
        "total_time": 0.8,
        "success_rate": 0.9
    }
    
    worse_metrics = {
        "total_tokens": 120,
        "total_time": 1.2,
        "success_rate": 0.7
    }
    
    assert optimizer._is_better_candidate(
        better_metrics,
        original_metrics,
        sample_config
    )
    
    assert not optimizer._is_better_candidate(
        worse_metrics,
        original_metrics,
        sample_config
    )

def test_token_reduction_target(optimizer, sample_test_case):
    """Test token reduction target in optimization."""
    config = OptimizationConfig(
        target_model=ModelType.GPT4,
        token_reduction_target=10,
        min_improvement=0.0
    )
    
    result = optimizer.optimize_prompt(
        prompt="This is a very long prompt that should be optimized to reduce tokens",
        test_cases=[sample_test_case],
        config=config
    )
    
    assert result.token_reduction >= 10

def test_execution_time_target(optimizer, sample_test_case):
    """Test execution time target in optimization."""
    config = OptimizationConfig(
        target_model=ModelType.GPT4,
        execution_time_target=0.5,
        min_improvement=0.0
    )
    
    result = optimizer.optimize_prompt(
        prompt="This is a prompt that should be optimized for faster execution",
        test_cases=[sample_test_case],
        config=config
    )
    
    assert result.execution_time_reduction >= 0.5

def test_min_improvement(optimizer, sample_test_case):
    """Test minimum improvement threshold."""
    config = OptimizationConfig(
        target_model=ModelType.GPT4,
        min_improvement=0.2
    )
    
    result = optimizer.optimize_prompt(
        prompt="This is a prompt that should show significant improvement",
        test_cases=[sample_test_case],
        config=config
    )
    
    assert result.improvement_percentage >= 0.2

def test_initialization(optimizer):
    """Test that the optimizer initializes correctly."""
    assert optimizer.common_redundancies
    assert optimizer.structure_patterns

def test_optimize_prompt(optimizer):
    """Test basic prompt optimization."""
    prompt = """
    System: You are a helpful assistant.
    Context: This is some background information that is really very important.
    Instruction: Please kindly help me with this task in order to achieve the goal.
    """
    
    optimized, metrics = optimizer.optimize_prompt(
        prompt=prompt,
        model=ModelType.GPT4
    )
    
    assert isinstance(optimized, str)
    assert isinstance(metrics, OptimizationMetrics)
    assert metrics.original_tokens > 0
    assert metrics.optimized_tokens > 0
    assert 0 <= metrics.token_reduction <= 1
    assert 0 <= metrics.quality_score <= 1
    assert 0 <= metrics.structure_score <= 1

def test_optimize_prompt_with_config(optimizer):
    """Test prompt optimization with custom config."""
    prompt = "This is a test prompt that is really very important."
    
    config = OptimizationConfig(
        max_tokens=100,
        min_quality_score=0.9,
        preserve_structure=True,
        aggressive_optimization=True,
        target_cost_reduction=0.3
    )
    
    optimized, metrics = optimizer.optimize_prompt(
        prompt=prompt,
        model=ModelType.GPT4,
        config=config
    )
    
    assert metrics.quality_score >= config.min_quality_score
    assert metrics.token_reduction >= 0

def test_remove_redundancies(optimizer):
    """Test removal of redundant words and phrases."""
    text = "This is really very important and in order to achieve the goal."
    optimized = optimizer._remove_redundancies(text)
    
    assert "really" not in optimized
    assert "very" not in optimized
    assert "in order to" not in optimized

def test_optimize_structure(optimizer):
    """Test prompt structure optimization."""
    text = """
    System: You are a helpful assistant.
    Context: Some background info.
    Instruction: Do something.
    """
    
    optimized = optimizer._optimize_structure(text)
    
    assert "system:" in optimized.lower()
    assert "context:" in optimized.lower()
    assert "instruction:" in optimized.lower()

def test_optimize_context(optimizer):
    """Test context optimization for different models."""
    text = """
    Context: This is some background information.
    Instruction: Do something.
    """
    
    # GPT-4 should preserve context
    gpt4_optimized = optimizer._optimize_context(text, ModelType.GPT4)
    assert "context:" in gpt4_optimized.lower()
    
    # Other models should be more aggressive
    other_optimized = optimizer._optimize_context(text, ModelType.CLAUDE)
    assert "context:" not in other_optimized.lower()

def test_ensure_quality(optimizer):
    """Test quality preservation."""
    # Good quality prompt
    good_prompt = """
    System: You are a helpful assistant.
    Instruction: Please help me with this task.
    """
    
    optimized = optimizer._ensure_quality(good_prompt, 0.8)
    assert optimized == good_prompt
    
    # Low quality prompt
    bad_prompt = "help"
    optimized = optimizer._ensure_quality(bad_prompt, 0.8)
    assert optimized == bad_prompt  # Should not be modified

def test_calculate_quality_score(optimizer):
    """Test quality score calculation."""
    # Good prompt
    good_prompt = """
    System: You are a helpful assistant.
    Instruction: Please help me with this task.
    """
    
    score = optimizer._calculate_quality_score(good_prompt)
    assert 0.8 <= score <= 1.0
    
    # Bad prompt
    bad_prompt = "help"
    score = optimizer._calculate_quality_score(bad_prompt)
    assert score < 0.8

def test_calculate_structure_score(optimizer):
    """Test structure score calculation."""
    # Well-structured prompt
    good_prompt = """
    System: You are a helpful assistant.
    Context: Some background.
    Instruction: Do something.
    """
    
    score = optimizer._calculate_structure_score(good_prompt)
    assert score > 0.5
    
    # Poorly structured prompt
    bad_prompt = "help me"
    score = optimizer._calculate_structure_score(bad_prompt)
    assert score < 0.5

def test_get_optimization_suggestions(optimizer):
    """Test getting optimization suggestions."""
    prompt = """
    This is really very important and in order to achieve the goal,
    we need to do something that is in need of attention.
    """
    
    suggestions = optimizer.get_optimization_suggestions(prompt)
    assert len(suggestions) > 0
    assert any("redundant" in s.lower() for s in suggestions) 