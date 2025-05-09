import pytest
from prompt_efficiency_suite import (
    BatchOptimizer,
    MultimodalCompressor,
    PromptOptimizer,
    TokenCounter,
    QualityAnalyzer,
    CostEstimator
)

# Test data
SAMPLE_PROMPTS = [
    "Write a story about a robot learning to paint",
    "Explain quantum computing to a 10-year-old",
    "Create a recipe for chocolate chip cookies",
    "Describe the process of photosynthesis",
    "Write a poem about the ocean"
]

@pytest.fixture
def batch_optimizer():
    """Create a BatchOptimizer instance for testing"""
    return BatchOptimizer()

@pytest.fixture
def multimodal_compressor():
    """Create a MultimodalCompressor instance for testing"""
    return MultimodalCompressor()

@pytest.fixture
def prompt_optimizer():
    """Create a PromptOptimizer instance for testing"""
    return PromptOptimizer()

@pytest.fixture
def token_counter():
    """Create a TokenCounter instance for testing"""
    return TokenCounter()

@pytest.fixture
def quality_analyzer():
    """Create a QualityAnalyzer instance for testing"""
    return QualityAnalyzer()

@pytest.fixture
def cost_estimator():
    """Create a CostEstimator instance for testing"""
    return CostEstimator()

def test_batch_optimizer():
    optimizer = BatchOptimizer()
    prompts = ["Test prompt 1", "Test prompt 2"]
    optimized = optimizer.optimize_batch(prompts)
    assert len(optimized) == len(prompts)
    assert all(isinstance(p, str) for p in optimized)

def test_multimodal_compressor():
    compressor = MultimodalCompressor()
    text = "This is a test text"
    compressed = compressor.compress(text)
    assert isinstance(compressed, str)
    assert len(compressed) <= len(text)

def test_prompt_optimizer():
    optimizer = PromptOptimizer()
    prompt = "This is a test prompt"
    optimized = optimizer.optimize(prompt)
    assert isinstance(optimized, str)
    assert len(optimized) <= len(prompt)

def test_token_counter():
    counter = TokenCounter()
    text = "This is a test text"
    count = counter.count_tokens(text)
    assert isinstance(count, int)
    assert count > 0

def test_quality_analyzer():
    analyzer = QualityAnalyzer()
    prompt = "This is a test prompt"
    score = analyzer.analyze(prompt)
    assert isinstance(score, float)
    assert 0 <= score <= 1

def test_cost_estimator():
    estimator = CostEstimator()
    prompt = "This is a test prompt"
    cost = estimator.estimate_cost(prompt)
    assert isinstance(cost, float)
    assert cost >= 0 