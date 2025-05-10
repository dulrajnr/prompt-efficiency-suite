# Prompt Optimization Engine Documentation

## Overview

The Prompt Optimization Engine is a powerful component of the Prompt Efficiency Suite that helps optimize prompts for better performance and efficiency. It uses test cases to validate optimizations and provides detailed metrics about improvements in token usage and execution time.

## Features

- **Prompt Optimization**: Automatically optimize prompts while maintaining effectiveness
- **Test-Driven Optimization**: Validate optimizations against test cases
- **Performance Metrics**: Track token usage and execution time improvements
- **Pattern Preservation**: Maintain important patterns in optimized prompts
- **Iterative Optimization**: Multiple optimization strategies with improvement tracking
- **Optimization History**: Track and manage optimization results
- **Metadata Support**: Add custom metadata to optimizations

## Installation

```bash
pip install prompt-efficiency-suite
```

## Quick Start

```python
from prompt_efficiency_suite import PromptOptimizer
from prompt_efficiency_suite.model_translator import ModelType
from prompt_efficiency_suite.tester import TestCase

# Initialize optimizer
optimizer = PromptOptimizer()

# Create test cases
test_cases = [
    TestCase(
        name="Math Test",
        prompt="What is 2+2?",
        expected_response="4",
        expected_patterns=["number", "sum"],
        expected_tokens=10,
        timeout=5.0
    )
]

# Create optimization config
config = OptimizationConfig(
    target_model=ModelType.GPT4,
    max_iterations=5,
    min_improvement=0.1,
    token_reduction_target=5,
    execution_time_target=0.5,
    preserve_patterns=["number", "sum"]
)

# Optimize prompt
result = optimizer.optimize_prompt(
    prompt="Please tell me what is the sum of 2 plus 2?",
    test_cases=test_cases,
    config=config
)

# Check results
print(f"Original Prompt: {result.original_prompt}")
print(f"Optimized Prompt: {result.optimized_prompt}")
print(f"Improvement: {result.improvement_percentage:.2%}")
print(f"Token Reduction: {result.token_reduction}")
print(f"Time Reduction: {result.execution_time_reduction:.2f}s")
```

## API Reference

### PromptOptimizer

#### `optimize_prompt(prompt: str, test_cases: List[TestCase], config: OptimizationConfig) -> OptimizationResult`

Optimize a prompt based on test cases and configuration.

**Parameters:**
- `prompt`: The original prompt to optimize
- `test_cases`: List of test cases to validate optimization
- `config`: Optimization configuration

**Returns:**
- OptimizationResult with optimization metrics

### OptimizationConfig

Optimization configuration.

**Attributes:**
- `target_model`: Target model for optimization
- `max_iterations`: Maximum optimization iterations
- `min_improvement`: Minimum improvement threshold
- `token_reduction_target`: Target token reduction
- `execution_time_target`: Target execution time reduction
- `preserve_patterns`: Patterns to preserve in optimization
- `metadata`: Custom metadata

### OptimizationResult

Optimization result data.

**Attributes:**
- `original_prompt`: Original prompt
- `optimized_prompt`: Optimized prompt
- `improvement_percentage`: Overall improvement percentage
- `token_reduction`: Number of tokens reduced
- `execution_time_reduction`: Execution time reduction
- `test_results`: Test results for optimized prompt
- `metadata`: Custom metadata

## REST API

### POST /api/v1/optimize

Optimize a prompt.

**Request:**
```json
{
  "prompt": "Please tell me what is the sum of 2 plus 2?",
  "test_cases": [
    {
      "name": "Test Case 1",
      "prompt": "What is 2+2?",
      "expected_response": "4",
      "expected_patterns": ["number", "sum"],
      "expected_tokens": 10,
      "timeout": 5.0
    }
  ],
  "config": {
    "target_model": "gpt-4",
    "max_iterations": 5,
    "min_improvement": 0.1,
    "token_reduction_target": 5,
    "execution_time_target": 0.5,
    "preserve_patterns": ["number", "sum"],
    "metadata": {
      "key": "value"
    }
  }
}
```

**Response:**
```json
{
  "original_prompt": "Please tell me what is the sum of 2 plus 2?",
  "optimized_prompt": "What is 2+2?",
  "improvement_percentage": 0.15,
  "token_reduction": 5,
  "execution_time_reduction": 0.3,
  "test_results": [
    {
      "success": true,
      "response": "4",
      "execution_time": 0.5,
      "token_usage": {
        "prompt": 5,
        "completion": 5
      }
    }
  ],
  "metadata": {
    "key": "value"
  }
}
```

### GET /api/v1/history

Get optimization history.

**Response:**
```json
[
  {
    "original_prompt": "Please tell me what is the sum of 2 plus 2?",
    "result": {
      "optimized_prompt": "What is 2+2?",
      "improvement_percentage": 0.15,
      "token_reduction": 5,
      "execution_time_reduction": 0.3,
      "test_results": [
        {
          "success": true,
          "response": "4",
          "execution_time": 0.5,
          "token_usage": {
            "prompt": 5,
            "completion": 5
          }
        }
      ],
      "metadata": {
        "key": "value"
      }
    }
  }
]
```

### DELETE /api/v1/history

Clear optimization history.

**Response:**
```json
{
  "message": "Optimization history cleared successfully"
}
```

## Best Practices

1. **Test Case Design**
   - Use diverse test cases
   - Include edge cases
   - Set appropriate timeouts
   - Define clear expectations
   - Add relevant metadata

2. **Optimization Configuration**
   - Set realistic targets
   - Use appropriate iterations
   - Define minimum improvement
   - Preserve important patterns
   - Monitor performance

3. **Prompt Optimization**
   - Start with clear prompts
   - Use test-driven approach
   - Monitor effectiveness
   - Track improvements
   - Validate results

4. **Performance Monitoring**
   - Track token usage
   - Monitor execution time
   - Analyze improvements
   - Set performance targets
   - Log metrics

5. **Error Handling**
   - Handle timeouts
   - Validate results
   - Check patterns
   - Monitor errors
   - Track failures

## Troubleshooting

### Common Issues

1. **Optimization Failures**
   - Check test cases
   - Verify patterns
   - Review targets
   - Check timeouts
   - Examine errors

2. **Performance Issues**
   - Adjust targets
   - Check iterations
   - Review patterns
   - Monitor metrics
   - Analyze bottlenecks

3. **Validation Problems**
   - Verify test cases
   - Check patterns
   - Review expectations
   - Test edge cases
   - Update targets

4. **API Errors**
   - Check model type
   - Verify parameters
   - Review errors
   - Check limits
   - Monitor usage

5. **History Issues**
   - Clear old history
   - Check storage
   - Verify format
   - Monitor memory
   - Backup data

### Getting Help

- Check the [API Documentation](../api.md)
- Visit our [GitHub Issues](https://github.com/yourorg/prompt-efficiency-suite/issues)
- Contact support at support@prompt-efficiency-suite.com
