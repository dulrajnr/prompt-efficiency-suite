# Prompt Efficiency Suite Usage Guide

## Quick Start

1. Install the package:
```bash
pip install prompt-efficiency-suite
```

2. Initialize the suite:
```python
from prompt_efficiency_suite import PromptEfficiencySuite

suite = PromptEfficiencySuite(
    api_key="your_api_key",
    default_domain="technical"
)
```

## Domain-Aware Trimming

### Basic Usage

```python
# Trim a single prompt
result = suite.trim(
    text="Your prompt text here",
    domain="technical",
    preserve_ratio=0.7
)

print(f"Original tokens: {result.original_tokens}")
print(f"Trimmed tokens: {result.trimmed_tokens}")
print(f"Preserved terms: {result.preserved_terms}")
```

### Custom Dictionary

```python
# Load custom domain dictionary
suite.load_domain_dictionary(
    domain="legal",
    dictionary_path="path/to/legal_terms.json"
)

# Trim with custom dictionary
result = suite.trim(
    text="Legal document text",
    domain="legal",
    preserve_ratio=0.8
)
```

## Adaptive Budgeting

### Track Usage

```python
# Track token usage
suite.track_usage(
    model="gpt-4",
    tokens=1000,
    cost=0.5
)

# Get metrics
metrics = suite.get_metrics(model="gpt-4")
print(f"Total tokens: {metrics.total_tokens}")
print(f"Total cost: ${metrics.total_cost}")
```

### Set Budget Alerts

```python
# Configure budget alerts
suite.configure_budget_alert(
    model="gpt-4",
    token_threshold=1000,
    cost_threshold=1.0,
    alert_email="team@example.com"
)
```

## Batch Optimization

### Optimize Multiple Prompts

```python
# Batch optimize prompts
results = suite.optimize_batch(
    prompts=[
        {"text": "Prompt 1", "domain": "technical"},
        {"text": "Prompt 2", "domain": "legal"}
    ],
    optimization_level="aggressive"
)

for result in results:
    print(f"Original: {result.original}")
    print(f"Optimized: {result.optimized}")
    print(f"Token savings: {result.savings.tokens}")
```

### Repository Scanning

```python
# Scan repository for optimization opportunities
opportunities = suite.scan_repository(
    path="./prompts",
    min_occurrences=3
)

for opp in opportunities:
    print(f"Pattern: {opp.pattern}")
    print(f"Occurrences: {opp.occurrences}")
    print(f"Potential savings: {opp.potential_savings} tokens")
```

## CI/CD Integration

### Run Tests

```python
# Run test suite
test_results = suite.run_tests(
    test_path="./tests",
    coverage=True
)

print(f"Passed tests: {test_results.passed_tests}")
print(f"Coverage: {test_results.coverage}%")
```

### Deploy

```python
# Deploy application
deployment = suite.deploy(
    environment="test",
    version="1.0.0",
    artifacts=["build", "docs"]
)

print(f"Deployment status: {deployment.status}")
print(f"Duration: {deployment.duration}s")
```

## Code-Aware Compression

### Compress Code

```python
# Compress code while preserving structure
compressed = suite.compress_code(
    code="""
    def example():
        # This is a comment
        print('Hello')
    """,
    language="python",
    preserve_comments=False
)

print(f"Original size: {compressed.original_size}")
print(f"Compressed size: {compressed.compressed_size}")
print(f"Compression ratio: {compressed.compression_ratio}")
```

## Best Practices

1. **Domain Dictionaries**
   - Keep dictionaries up to date
   - Use hierarchical structure for complex domains
   - Include common variations of terms

2. **Budget Management**
   - Set realistic thresholds
   - Monitor usage patterns
   - Adjust budgets based on historical data

3. **Batch Processing**
   - Process similar prompts together
   - Use appropriate optimization levels
   - Review optimization suggestions

4. **Code Compression**
   - Test compressed code thoroughly
   - Preserve critical comments
   - Use language-specific settings

## Troubleshooting

### Common Issues

1. **Domain Terms Not Preserved**
   - Check dictionary format
   - Verify term importance scores
   - Ensure proper domain selection

2. **High Token Usage**
   - Review preservation ratio
   - Check for redundant terms
   - Optimize prompt structure

3. **Test Failures**
   - Check test configuration
   - Verify test dependencies
   - Review test coverage

### Getting Help

- Check the [API Documentation](api.md)
- Visit our [GitHub Issues](https://github.com/yourorg/prompt-efficiency-suite/issues)
- Contact support at support@prompt-efficiency-suite.com 