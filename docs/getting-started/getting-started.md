# Getting Started with Prompt Efficiency Suite

This guide will help you get started with the Prompt Efficiency Suite, from installation to basic usage.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Basic Installation

```bash
pip install prompt-efficiency-suite
```

### Development Installation

For development or to contribute to the project:

```bash
git clone https://github.com/yourusername/prompt-efficiency-suite.git
cd prompt-efficiency-suite
pip install -e ".[dev]"
```

## Basic Usage

### 1. Optimizing a Prompt

```python
from prompt_efficiency_suite import BaseCompressor, PromptAnalyzer, MetricsTracker

# Initialize components
compressor = BaseCompressor()
analyzer = PromptAnalyzer()
metrics_tracker = MetricsTracker()

# Optimize a prompt
result = await compressor.compress(
    "Your prompt here",
    target_ratio=0.5  # Target 50% compression
)

# Analyze the result
analysis = analyzer.analyze(result.compressed_text)

# Print results
print(f"Original tokens: {result.original_tokens}")
print(f"Compressed tokens: {result.compressed_tokens}")
print(f"Compression ratio: {result.compression_ratio}")
```

### 2. Managing Token Budgets

```python
from prompt_efficiency_suite import AdaptiveBudgetManager
from datetime import timedelta

# Initialize budget manager
budget_manager = AdaptiveBudgetManager(
    initial_budget=10000,
    allocation_period=timedelta(days=1)
)

# Check remaining budget
remaining = budget_manager.get_remaining_budget()
print(f"Remaining budget: {remaining} tokens")

# Record usage
budget_manager.record_usage(metrics)
```

### 3. Using Macros

```python
from prompt_efficiency_suite import MacroManager, MacroDefinition

# Initialize macro manager
macro_manager = MacroManager()

# Create a macro
macro = MacroDefinition(
    name="greeting",
    template="Hello, {name}! How can I help you today?",
    description="A friendly greeting template",
    parameters=["name"]
)

# Register the macro
macro_manager.register_macro(macro)

# Use the macro
expanded = macro_manager.expand_macro("greeting", {"name": "Alice"})
```

## Configuration

### Basic Configuration

Create a `config.yaml` file:

```yaml
compressor:
  model_name: "gpt-3.5-turbo"
  target_ratio: 0.5
  min_quality_score: 0.7

analyzer:
  model_name: "en_core_web_sm"
  metrics:
    - clarity
    - completeness
    - consistency

budget:
  initial_budget: 10000
  allocation_period_days: 1
  min_budget: 1000
  max_budget: 1000000
```

### Loading Configuration

```python
from prompt_efficiency_suite import load_config

# Load configuration
config = load_config("config.yaml")

# Use configuration
compressor = BaseCompressor(**config["compressor"])
analyzer = PromptAnalyzer(**config["analyzer"])
```

## Command Line Interface

The suite provides a command-line interface for common operations:

```bash
# Optimize a prompt
prompt-efficiency optimize "Your prompt here" --target-ratio 0.5

# Scan a repository
prompt-efficiency scan /path/to/repo --output results.json

# Analyze a prompt
prompt-efficiency analyze "Your prompt here" --output analysis.json

# Manage budget
prompt-efficiency budget config.yaml --initial-budget 10000 --period 7
```

## Next Steps

1. Read the [Core Components](components.md) documentation to understand the main features
2. Check out [Examples](examples.md) for more usage scenarios
3. Review [Best Practices](best-practices.md) for optimal usage
4. Explore [Advanced Features](advanced-features.md) for more complex use cases

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'prompt_efficiency_suite'**
   - Ensure the package is installed correctly
   - Check your Python environment

2. **Configuration Loading Error**
   - Verify the config file exists and is properly formatted
   - Check file permissions

3. **Token Budget Issues**
   - Verify your API keys and quotas
   - Check budget allocation settings

### Getting Help

- Check the [FAQ](faq.md)
- Search [existing issues](https://github.com/yourusername/prompt-efficiency-suite/issues)
- Create a new issue if needed
- Contact support@promptefficiencysuite.com
