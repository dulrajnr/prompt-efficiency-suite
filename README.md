# Prompt Efficiency Suite

A comprehensive toolkit for optimizing and managing prompts for large language models.

## Features

- **Batch Processing**: Efficiently process multiple prompts in parallel
- **Multimodal Compression**: Optimize prompts containing both text and images
- **Prompt Optimization**: Improve prompt quality and effectiveness
- **Token Counting**: Accurate token counting for various LLM models
- **Quality Analysis**: Evaluate prompt quality and effectiveness
- **Cost Estimation**: Calculate costs for different LLM models

## Installation

```bash
pip install prompt-efficiency-suite
```

## Quick Start

```python
from prompt_efficiency_suite import (
    BatchOptimizer,
    MultimodalCompressor,
    PromptOptimizer,
    TokenCounter,
    QualityAnalyzer,
    CostEstimator
)

# Initialize components
batch_optimizer = BatchOptimizer()
compressor = MultimodalCompressor()
optimizer = PromptOptimizer()
token_counter = TokenCounter()
quality_analyzer = QualityAnalyzer()
cost_estimator = CostEstimator()

# Process a batch of prompts
prompts = [
    "Explain quantum computing",
    "Describe the process of photosynthesis",
    "What is machine learning?"
]

# Optimize prompts
optimized_prompts = batch_optimizer.process_batch(prompts)

# Count tokens
token_counts = token_counter.count_batch(optimized_prompts)

# Analyze quality
quality_scores = quality_analyzer.analyze_batch(optimized_prompts)

# Estimate costs
costs = cost_estimator.estimate_batch_cost(optimized_prompts)
```

## Components

### BatchOptimizer
Processes multiple prompts efficiently using parallel processing.

### MultimodalCompressor
Optimizes prompts containing both text and images.

### PromptOptimizer
Improves prompt quality and effectiveness.

### TokenCounter
Accurately counts tokens for various LLM models.

### QualityAnalyzer
Evaluates prompt quality and effectiveness.

### CostEstimator
Calculates costs for different LLM models.

## Requirements

- Python 3.8 or higher
- spaCy 3.7.0 or higher
- tiktoken 0.3.0 or higher
- numpy 1.21.0 or higher
- Pillow 10.0.0 or higher
- scikit-learn 0.24.2 or higher

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 