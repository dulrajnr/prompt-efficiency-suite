# Prompt Efficiency Suite

A comprehensive toolkit for optimizing and managing prompts in AI applications.

## Features

- **Prompt Compression**: Reduce token usage while maintaining quality
- **Prompt Analysis**: Analyze prompts for quality, readability, and efficiency
- **Metrics Tracking**: Monitor usage, costs, and performance
- **Batch Processing**: Optimize multiple prompts efficiently
- **Macro System**: Create and manage reusable prompt templates
- **Repository Scanning**: Find and analyze prompts in codebases
- **Adaptive Budgeting**: Manage token budgets dynamically
- **Command Line Interface**: Easy-to-use CLI for common operations

## Installation

```bash
pip install prompt-efficiency-suite
```

For development installation:

```bash
git clone https://github.com/yourusername/prompt-efficiency-suite.git
cd prompt-efficiency-suite
pip install -e ".[dev]"
```

## Quick Start

```python
from prompt_efficiency_suite import BaseCompressor, PromptAnalyzer

# Initialize components
compressor = BaseCompressor()
analyzer = PromptAnalyzer()

# Compress a prompt
result = await compressor.compress(
    text="Your prompt here",
    target_ratio=0.7
)

# Analyze the compressed prompt
analysis = analyzer.analyze(result.compressed_text)

print(f"Compression ratio: {result.compression_ratio:.2f}")
print(f"Readability score: {analysis.readability_score:.2f}")
```

## Documentation

- [Getting Started](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Best Practices](docs/best-practices.md)
- [Examples](docs/examples.md)
- [Contributing](docs/contributing.md)

## Features in Detail

### Prompt Compression

```python
from prompt_efficiency_suite import BaseCompressor

compressor = BaseCompressor()
result = await compressor.compress(
    text="Your prompt here",
    target_ratio=0.7
)
```

### Prompt Analysis

```python
from prompt_efficiency_suite import PromptAnalyzer

analyzer = PromptAnalyzer()
analysis = analyzer.analyze("Your prompt here")
```

### Metrics Tracking

```python
from prompt_efficiency_suite import MetricsTracker

tracker = MetricsTracker()
tracker.add_metrics(
    EfficiencyMetrics(
        prompt_id="prompt_1",
        token_count=150,
        cost=0.0003,
        success_rate=0.95
    )
)
```

### Batch Processing

```python
from prompt_efficiency_suite import BulkOptimizer

optimizer = BulkOptimizer(
    compressor=compressor,
    analyzer=analyzer,
    metrics_tracker=tracker
)

results = await optimizer.optimize_batch(
    prompts=["Prompt 1", "Prompt 2"],
    target_ratio=0.7
)
```

### Macro System

```python
from prompt_efficiency_suite import MacroManager, MacroDefinition

manager = MacroManager()
macro = MacroDefinition(
    name="summary",
    template="Summarize: {text}",
    parameters=["text"]
)
manager.register_macro(macro)
```

### Repository Scanning

```python
from prompt_efficiency_suite import RepositoryScanner

scanner = RepositoryScanner()
locations = scanner.scan_repository("/path/to/repo")
```

### Adaptive Budgeting

```python
from prompt_efficiency_suite import AdaptiveBudgetManager

budget_manager = AdaptiveBudgetManager(
    initial_budget=100000,
    allocation_period=timedelta(days=1)
)
```

## Command Line Interface

```bash
# Optimize a prompt
prompt-efficiency optimize "Your prompt here" --target-ratio 0.7

# Scan a repository
prompt-efficiency scan /path/to/repo

# Analyze a prompt
prompt-efficiency analyze "Your prompt here"

# Manage budget
prompt-efficiency budget --initial 100000 --period 1d
```

## Configuration

Create a `config.yaml` file:

```yaml
compressor:
  model_name: "gpt-3.5-turbo"
  target_ratio: 0.7
  min_quality_score: 0.8

analyzer:
  model_name: "en_core_web_sm"
  metrics:
    - readability
    - complexity
    - redundancy

budget:
  initial_budget: 100000
  allocation_period_days: 1
  min_budget: 10000
  max_budget: 1000000
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/prompt-efficiency-suite/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/prompt-efficiency-suite/discussions)

## Citation

If you use this project in your research, please cite:

```bibtex
@software{prompt_efficiency_suite,
  author = {Prompt Efficiency Suite Team},
  title = {Prompt Efficiency Suite},
  year = {2024},
  url = {https://github.com/yourusername/prompt-efficiency-suite}
}
``` 