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
    optimized = optimizer.process_batch(sample_prompts)
    assert len(optimized) == len(sample_prompts)
    assert all(isinstance(p, str) for p in optimized)

def test_multimodal_compressor(sample_image_prompt):
    compressor = MultimodalCompressor()
    compressed = compressor.compress(sample_image_prompt)
    assert isinstance(compressed, dict)
    assert "text" in compressed
    assert "image" in compressed

def test_prompt_optimizer(sample_prompts):
    optimizer = PromptOptimizer()
    optimized = optimizer.optimize(sample_prompts[0])
    assert isinstance(optimized, str)
    assert len(optimized) > 0

def test_token_counter(sample_prompts):
    counter = TokenCounter()
    counts = counter.count_batch(sample_prompts)
    assert len(counts) == len(sample_prompts)
    assert all(isinstance(c, int) for c in counts)
    assert all(c > 0 for c in counts)

def test_quality_analyzer(sample_prompts):
    analyzer = QualityAnalyzer()
    scores = analyzer.analyze_batch(sample_prompts)
    assert len(scores) == len(sample_prompts)
    assert all(isinstance(s, float) for s in scores)
    assert all(0 <= s <= 1 for s in scores)

def test_cost_estimator(sample_prompts):
    estimator = CostEstimator()
    costs = estimator.estimate_batch_cost(sample_prompts)
    assert len(costs) == len(sample_prompts)
    assert all(isinstance(c, float) for c in costs)
    assert all(c >= 0 for c in costs)

def test_integration(sample_prompts):
    # Test the full pipeline
    batch_optimizer = BatchOptimizer()
    token_counter = TokenCounter()
    quality_analyzer = QualityAnalyzer()
    cost_estimator = CostEstimator()

    # Process batch
    optimized = batch_optimizer.process_batch(sample_prompts)
    assert len(optimized) == len(sample_prompts)

    # Count tokens
    counts = token_counter.count_batch(optimized)
    assert len(counts) == len(optimized)

    # Analyze quality
    scores = quality_analyzer.analyze_batch(optimized)
    assert len(scores) == len(optimized)

    # Estimate costs
    costs = cost_estimator.estimate_batch_cost(optimized)
    assert len(costs) == len(optimized)

def test_error_handling():
    optimizer = BatchOptimizer()
    with pytest.raises(ValueError):
        optimizer.process_batch([])

    counter = TokenCounter()
    with pytest.raises(ValueError):
        counter.count_batch([""])

    analyzer = QualityAnalyzer()
    with pytest.raises(ValueError):
        analyzer.analyze_batch([""])

    estimator = CostEstimator()
    with pytest.raises(ValueError):
        estimator.estimate_batch_cost([""]) 