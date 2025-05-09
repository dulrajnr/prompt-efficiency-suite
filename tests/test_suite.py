import pytest
from prompt_efficiency_suite import (
    BatchOptimizer,
    MultimodalCompressor,
    PromptOptimizer,
    TokenCounter,
    QualityAnalyzer,
    CostEstimator
)

@pytest.fixture
def sample_prompts():
    return [
        "Explain quantum computing in simple terms",
        "Describe the process of photosynthesis",
        "What is machine learning and how does it work?"
    ]

@pytest.fixture
def sample_image_prompt():
    return {
        "text": "Describe this image of a sunset",
        "image_path": "tests/data/sample_image.jpg"
    }

def test_batch_optimizer(sample_prompts):
    optimizer = BatchOptimizer()
    optimized = optimizer.optimize_batch(sample_prompts)
    assert len(optimized) == len(sample_prompts)
    assert all(isinstance(p, str) for p in optimized)

def test_multimodal_compressor():
    compressor = MultimodalCompressor()
    text = "This is a test text"
    compressed = compressor.compress(text)
    assert isinstance(compressed, str)
    assert len(compressed) <= len(text)

def test_prompt_optimizer(sample_prompts):
    optimizer = PromptOptimizer()
    optimized = optimizer.optimize(sample_prompts[0])
    assert isinstance(optimized, str)
    assert len(optimized) > 0

def test_token_counter(sample_prompts):
    counter = TokenCounter()
    count = counter.count_tokens(sample_prompts[0])
    assert isinstance(count, int)
    assert count > 0

def test_quality_analyzer(sample_prompts):
    analyzer = QualityAnalyzer()
    score = analyzer.analyze(sample_prompts[0])
    assert isinstance(score, float)
    assert 0 <= score <= 1

def test_cost_estimator(sample_prompts):
    estimator = CostEstimator()
    cost = estimator.estimate_cost(sample_prompts[0])
    assert isinstance(cost, float)
    assert cost >= 0

def test_integration(sample_prompts):
    # Test the full pipeline
    batch_optimizer = BatchOptimizer()
    token_counter = TokenCounter()
    quality_analyzer = QualityAnalyzer()
    cost_estimator = CostEstimator()

    # Process batch
    optimized = batch_optimizer.optimize_batch(sample_prompts)
    assert len(optimized) == len(sample_prompts)

    # Count tokens
    count = token_counter.count_tokens(optimized[0])
    assert isinstance(count, int)
    assert count > 0

    # Analyze quality
    score = quality_analyzer.analyze(optimized[0])
    assert isinstance(score, float)
    assert 0 <= score <= 1

    # Estimate costs
    cost = cost_estimator.estimate_cost(optimized[0])
    assert isinstance(cost, float)
    assert cost >= 0

def test_error_handling():
    optimizer = BatchOptimizer()
    with pytest.raises(ValueError):
        optimizer.optimize_batch([])

    counter = TokenCounter()
    with pytest.raises(ValueError):
        counter.count_tokens("")

    analyzer = QualityAnalyzer()
    with pytest.raises(ValueError):
        analyzer.analyze("")

    estimator = CostEstimator()
    with pytest.raises(ValueError):
        estimator.estimate_cost("") 