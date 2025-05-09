# Prompt Testing Engine Documentation

## Overview

The Prompt Testing Engine is a powerful component of the Prompt Efficiency Suite that helps test prompts against different models and scenarios. It provides comprehensive testing capabilities, including response validation, performance metrics, and test history tracking.

## Features

- **Single Test Cases**: Test individual prompts with specific expectations
- **Test Suites**: Run multiple related test cases together
- **Response Validation**: Validate responses against exact matches, patterns, and token limits
- **Performance Metrics**: Track execution time and token usage
- **Retry Mechanism**: Automatically retry failed tests
- **Timeout Handling**: Set timeouts for test cases
- **Test History**: Track and manage test results
- **Metadata Support**: Add custom metadata to tests and results

## Installation

```bash
pip install prompt-efficiency-suite
```

## Quick Start

```python
from prompt_efficiency_suite import PromptTester
from prompt_efficiency_suite.model_translator import ModelType

# Initialize tester
tester = PromptTester()

# Create a test case
test_case = TestCase(
    name="Math Test",
    prompt="What is 2+2?",
    expected_response="4",
    expected_patterns=["number", "sum"],
    expected_tokens=10,
    timeout=5.0
)

# Run the test
result = tester.run_test_case(
    test_case=test_case,
    model=ModelType.GPT4
)

# Check results
print(f"Success: {result.success}")
print(f"Response: {result.response}")
print(f"Execution Time: {result.execution_time}s")
print(f"Token Usage: {result.token_usage}")

# Create and run a test suite
test_suite = TestSuite(
    name="Math Test Suite",
    description="Test basic math operations",
    test_cases=[test_case],
    model=ModelType.GPT4
)

results = tester.run_test_suite(test_suite)
for result in results:
    print(f"Test Result: {result.success}")
```

## API Reference

### PromptTester

#### `run_test_case(test_case: TestCase, model: ModelType, max_retries: int = 3, timeout: Optional[float] = None) -> TestResult`

Run a single test case against the specified model.

**Parameters:**
- `test_case`: The test case to run
- `model`: The target model
- `max_retries`: Maximum number of retry attempts
- `timeout`: Maximum execution time in seconds

**Returns:**
- TestResult with test outcome and metrics

#### `run_test_suite(test_suite: TestSuite) -> List[TestResult]`

Run a complete test suite.

**Parameters:**
- `test_suite`: The test suite to run

**Returns:**
- List of TestResults for each test case

### TestCase

Test case configuration.

**Attributes:**
- `name`: Test case name
- `prompt`: The prompt to test
- `expected_response`: Expected exact response
- `expected_patterns`: List of patterns to check in response
- `expected_tokens`: Maximum allowed tokens
- `timeout`: Maximum execution time
- `metadata`: Custom metadata

### TestSuite

Test suite configuration.

**Attributes:**
- `name`: Suite name
- `description`: Suite description
- `test_cases`: List of test cases
- `model`: Target model
- `max_retries`: Maximum retry attempts
- `timeout`: Maximum execution time
- `metadata`: Custom metadata

### TestResult

Test result data.

**Attributes:**
- `success`: Whether the test passed
- `response`: Model's response
- `execution_time`: Time taken
- `token_usage`: Token usage statistics
- `error`: Error message if failed
- `metadata`: Custom metadata

## REST API

### POST /api/v1/test-case

Run a single test case.

**Request:**
```json
{
  "name": "Test Case 1",
  "prompt": "What is 2+2?",
  "expected_response": "4",
  "expected_patterns": ["number", "sum"],
  "expected_tokens": 10,
  "timeout": 5.0,
  "metadata": {
    "key": "value"
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "4",
  "execution_time": 0.5,
  "token_usage": {
    "prompt": 10,
    "completion": 20
  },
  "metadata": {
    "key": "value"
  }
}
```

### POST /api/v1/test-suite

Run a test suite.

**Request:**
```json
{
  "name": "Math Test Suite",
  "description": "Test basic math operations",
  "test_cases": [
    {
      "name": "Test Case 1",
      "prompt": "What is 2+2?",
      "expected_response": "4"
    },
    {
      "name": "Test Case 2",
      "prompt": "What is 3+3?",
      "expected_response": "6"
    }
  ],
  "model": "gpt-4",
  "max_retries": 3,
  "timeout": 10.0,
  "metadata": {
    "key": "value"
  }
}
```

**Response:**
```json
[
  {
    "success": true,
    "response": "4",
    "execution_time": 0.5,
    "token_usage": {
      "prompt": 10,
      "completion": 20
    }
  },
  {
    "success": true,
    "response": "6",
    "execution_time": 0.4,
    "token_usage": {
      "prompt": 10,
      "completion": 20
    }
  }
]
```

### GET /api/v1/history

Get test history.

**Response:**
```json
[
  {
    "test_case": {
      "name": "Test Case 1",
      "prompt": "What is 2+2?",
      "expected_response": "4"
    },
    "result": {
      "success": true,
      "response": "4",
      "execution_time": 0.5,
      "token_usage": {
        "prompt": 10,
        "completion": 20
      }
    }
  }
]
```

### DELETE /api/v1/history

Clear test history.

**Response:**
```json
{
  "message": "Test history cleared successfully"
}
```

## Best Practices

1. **Test Case Design**
   - Use clear, descriptive names
   - Set appropriate timeouts
   - Include expected patterns
   - Set token limits
   - Add relevant metadata

2. **Test Suite Organization**
   - Group related test cases
   - Use consistent naming
   - Set appropriate retry limits
   - Include suite-level timeouts
   - Add descriptive metadata

3. **Response Validation**
   - Use exact matches when possible
   - Include multiple patterns
   - Set reasonable token limits
   - Consider response variations
   - Handle edge cases

4. **Error Handling**
   - Set appropriate timeouts
   - Use retry mechanism
   - Check error messages
   - Log failed tests
   - Track error patterns

5. **Performance Monitoring**
   - Track execution times
   - Monitor token usage
   - Set performance thresholds
   - Log performance metrics
   - Analyze trends

## Troubleshooting

### Common Issues

1. **Test Failures**
   - Check expected responses
   - Verify patterns
   - Review token limits
   - Check timeouts
   - Examine error messages

2. **Performance Issues**
   - Adjust timeouts
   - Check token usage
   - Review retry settings
   - Monitor execution times
   - Analyze bottlenecks

3. **Validation Problems**
   - Verify patterns
   - Check token counts
   - Review response format
   - Test edge cases
   - Update expectations

4. **API Errors**
   - Check model type
   - Verify parameters
   - Review error messages
   - Check API limits
   - Monitor rate limits

5. **History Issues**
   - Clear old history
   - Check storage limits
   - Verify data format
   - Monitor memory usage
   - Backup important data

### Getting Help

- Check the [API Documentation](../api.md)
- Visit our [GitHub Issues](https://github.com/yourorg/prompt-efficiency-suite/issues)
- Contact support at support@prompt-efficiency-suite.com 