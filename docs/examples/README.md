# Examples

This directory contains examples demonstrating various features of the Prompt Efficiency Suite.

## Basic Usage Examples

### Prompt Analysis
```python
from prompt_efficiency_suite import PromptAnalyzer

analyzer = PromptAnalyzer()
result = analyzer.analyze("Your prompt here")
print(f"Readability score: {result.readability_score}")
print(f"Complexity score: {result.complexity_score}")
```

### Prompt Optimization
```python
from prompt_efficiency_suite import PromptOptimizer

optimizer = PromptOptimizer()
result = optimizer.optimize(
    prompt="Your prompt here",
    target_ratio=0.7
)
print(f"Optimized prompt: {result.optimized_prompt}")
print(f"Compression ratio: {result.compression_ratio}")
```

### Repository Scanning
```python
from prompt_efficiency_suite import RepositoryScanner

scanner = RepositoryScanner()
results = scanner.scan_repository("/path/to/repo")
for file_result in results:
    print(f"File: {file_result.file_path}")
    print(f"Prompts found: {len(file_result.prompts)}")
```

## Advanced Examples

### Batch Processing
```python
from prompt_efficiency_suite import BulkOptimizer

optimizer = BulkOptimizer()
results = optimizer.optimize_batch(
    prompts=["Prompt 1", "Prompt 2"],
    target_ratio=0.7
)
for result in results:
    print(f"Original: {result.original_prompt}")
    print(f"Optimized: {result.optimized_prompt}")
```

### Cost Management
```python
from prompt_efficiency_suite import CostEstimator

estimator = CostEstimator()
cost = estimator.estimate_cost(
    prompt="Your prompt here",
    model="gpt-4"
)
print(f"Estimated cost: ${cost:.4f}")
```

### Macro System
```python
from prompt_efficiency_suite import MacroManager

manager = MacroManager()
manager.register_macro(
    name="summary",
    template="Summarize the following text: {text}",
    parameters=["text"]
)
result = manager.apply_macro("summary", text="Your text here")
```

## Integration Examples

### FastAPI Integration
```python
from fastapi import FastAPI
from prompt_efficiency_suite.api import app

api = FastAPI()
api.include_router(app.router)
```

### CLI Usage
```bash
# Analyze a prompt
prompt-efficiency analyze "Your prompt here"

# Optimize a prompt
prompt-efficiency optimize "Your prompt here" --target-ratio 0.7

# Scan a repository
prompt-efficiency scan /path/to/repo

# Estimate costs
prompt-efficiency estimate-cost "Your prompt here" --model gpt-4
```

## Configuration Examples

### Basic Configuration
```yaml
# config.yaml
api:
  max_default_tokens: 1800
  build_failure: true

security:
  ssl_verify: true
  rate_limit: 100

logging:
  level: INFO
  mask_sensitive: true
```

### Advanced Configuration
```yaml
# config.yaml
optimizer:
  model_name: "gpt-4"
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

## Error Handling Examples

### Basic Error Handling
```python
from prompt_efficiency_suite import PromptEfficiencyError

try:
    result = optimizer.optimize("Your prompt here")
except PromptEfficiencyError as e:
    print(f"Error: {e.message}")
    print(f"Error code: {e.code}")
```

### Advanced Error Handling
```python
from prompt_efficiency_suite import (
    PromptEfficiencyError,
    ValidationError,
    APIError
)

try:
    result = optimizer.optimize("Your prompt here")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except APIError as e:
    print(f"API error: {e.message}")
    print(f"Status code: {e.status_code}")
except PromptEfficiencyError as e:
    print(f"General error: {e.message}")
```

## Contributing Examples

If you have additional examples to share, please:

1. Create a new markdown file in this directory
2. Follow the existing format
3. Include clear code examples
4. Add comments explaining the code
5. Submit a pull request

## Need Help?

If you need help with any of these examples or have questions about implementation, please:

1. Check the [documentation](../)
2. Open an issue on GitHub
3. Join our community discussions
