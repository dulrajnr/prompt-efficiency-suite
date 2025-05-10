# Command Line Interface (CLI)

The Prompt Efficiency Suite CLI provides a powerful command-line interface for all features of the system.

## Installation

```bash
pip install prompt-efficiency-suite
```

## Basic Usage

```bash
prompt-efficiency [command] [options]
```

## Commands

### 1. Core Commands

#### Analyze Prompt
```bash
prompt-efficiency analyze "Your prompt text" [options]
```

Options:
- `--output`: Output format (json, yaml, text)
- `--model`: Model to use for analysis
- `--include-patterns`: Include pattern recognition
- `--include-suggestions`: Include improvement suggestions

Example:
```bash
prompt-efficiency analyze "Write a function to sort a list" --output json --include-suggestions
```

#### Optimize Prompt
```bash
prompt-efficiency optimize "Your prompt text" [options]
```

Options:
- `--method`: Optimization method (trim, compress, enhance)
- `--target-ratio`: Target compression ratio
- `--preserve-terms`: Terms to preserve
- `--min-quality`: Minimum quality threshold

Example:
```bash
prompt-efficiency optimize "Your prompt" --method compress --target-ratio 0.8
```

#### Estimate Cost
```bash
prompt-efficiency estimate-cost "Your prompt text" [options]
```

Options:
- `--model`: Model to estimate for
- `--currency`: Currency for cost
- `--include-breakdown`: Include token breakdown

Example:
```bash
prompt-efficiency estimate-cost "Your prompt" --model gpt-4 --currency USD
```

#### Count Tokens
```bash
prompt-efficiency count-tokens "Your prompt text" [options]
```

Options:
- `--model`: Model to count for
- `--include-breakdown`: Include token breakdown

Example:
```bash
prompt-efficiency count-tokens "Your prompt" --model gpt-4
```

### 2. Repository Management

#### Scan Repository
```bash
prompt-efficiency scan-repository [path] [options]
```

Options:
- `--include-analysis`: Include prompt analysis
- `--include-suggestions`: Include improvement suggestions
- `--file-patterns`: File patterns to scan
- `--output`: Output format

Example:
```bash
prompt-efficiency scan-repository ./src --include-analysis --file-patterns "*.py,*.js"
```

#### Bulk Optimize
```bash
prompt-efficiency bulk-optimize [path] [options]
```

Options:
- `--method`: Optimization method
- `--target-ratio`: Target compression ratio
- `--min-quality`: Minimum quality threshold
- `--output`: Output format

Example:
```bash
prompt-efficiency bulk-optimize ./prompts --method compress --target-ratio 0.8
```

### 3. Macro Management

#### Install Macro
```bash
prompt-efficiency macro install [name] [options]
```

Options:
- `--source`: Source URL or path
- `--version`: Macro version
- `--force`: Force installation

Example:
```bash
prompt-efficiency macro install api-doc --source https://github.com/user/macro
```

#### List Macros
```bash
prompt-efficiency macro list [options]
```

Options:
- `--installed`: Show only installed macros
- `--available`: Show available macros
- `--format`: Output format

Example:
```bash
prompt-efficiency macro list --installed --format json
```

#### Apply Macro
```bash
prompt-efficiency macro apply [name] [input] [options]
```

Options:
- `--params`: Macro parameters
- `--output`: Output format
- `--validate`: Validate result

Example:
```bash
prompt-efficiency macro apply api-doc "Your API" --params "method=GET"
```

### 4. Budget Management

#### Show Metrics
```bash
prompt-efficiency budget metrics [options]
```

Options:
- `--period`: Time period
- `--model`: Model to show metrics for
- `--format`: Output format

Example:
```bash
prompt-efficiency budget metrics --period last_week --model gpt-4
```

#### Set Budget
```bash
prompt-efficiency budget set [amount] [options]
```

Options:
- `--period`: Budget period
- `--model`: Model to set budget for
- `--currency`: Currency

Example:
```bash
prompt-efficiency budget set 100 --period monthly --model gpt-4
```

### 5. Content Processing

#### Trim Prompt
```bash
prompt-efficiency trim "Your prompt text" [options]
```

Options:
- `--target-length`: Target length
- `--preserve-terms`: Terms to preserve
- `--method`: Trimming method

Example:
```bash
prompt-efficiency trim "Your prompt" --target-length 100
```

#### Compress Content
```bash
prompt-efficiency compress "Your content" [options]
```

Options:
- `--method`: Compression method
- `--target-ratio`: Target ratio
- `--preserve-structure`: Preserve structure

Example:
```bash
prompt-efficiency compress "Your content" --method semantic
```

### 6. CI/CD Integration

#### Run Tests
```bash
prompt-efficiency test [options]
```

Options:
- `--path`: Test path
- `--parallel`: Run tests in parallel
- `--timeout`: Test timeout
- `--retry`: Retry failed tests

Example:
```bash
prompt-efficiency test --path ./tests --parallel
```

#### Deploy Package
```bash
prompt-efficiency deploy [options]
```

Options:
- `--version`: Package version
- `--target`: Deployment target
- `--force`: Force deployment

Example:
```bash
prompt-efficiency deploy --version 1.0.0 --target production
```

### 7. Benchmark Management

#### Create Benchmark
```bash
prompt-efficiency benchmark create [options]
```

Options:
- `--name`: Benchmark name
- `--description`: Benchmark description
- `--tasks`: Benchmark tasks
- `--metrics`: Metrics to track

Example:
```bash
prompt-efficiency benchmark create --name "API Performance" --tasks "task1,task2"
```

#### Submit Results
```bash
prompt-efficiency benchmark submit [results] [options]
```

Options:
- `--benchmark`: Benchmark name
- `--format`: Results format
- `--validate`: Validate results

Example:
```bash
prompt-efficiency benchmark submit results.json --benchmark "API Performance"
```

## Configuration

### Global Configuration
```bash
prompt-efficiency config set [key] [value]
```

Example:
```bash
prompt-efficiency config set api_key "your-api-key"
```

### Configuration File
```yaml
api:
  key: "your-api-key"
  url: "http://localhost:8000"
  timeout: 30

defaults:
  model: "gpt-4"
  currency: "USD"
  output_format: "json"

optimization:
  default_method: "compress"
  target_ratio: 0.8
  min_quality: 0.7

scanning:
  file_patterns: ["*.py", "*.js"]
  exclude_patterns: ["tests/*", "docs/*"]
```

## Environment Variables

- `PROMPT_EFFICIENCY_API_KEY`: API key
- `PROMPT_EFFICIENCY_API_URL`: API URL
- `PROMPT_EFFICIENCY_DEFAULT_MODEL`: Default model
- `PROMPT_EFFICIENCY_DEFAULT_CURRENCY`: Default currency

## Output Formats

### JSON
```json
{
  "result": {
    "quality_score": 0.85,
    "suggestions": ["Add more context"]
  }
}
```

### YAML
```yaml
result:
  quality_score: 0.85
  suggestions:
    - Add more context
```

### Text
```
Quality Score: 0.85
Suggestions:
- Add more context
```

## Error Handling

### Common Errors
- `APIError`: API connection or authentication error
- `ValidationError`: Invalid input or parameters
- `ConfigurationError`: Configuration issues
- `ExecutionError`: Command execution failure

### Error Output
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": {
      "field": "Additional details"
    }
  }
}
```

## Best Practices

1. **Configuration**
   - Use environment variables for sensitive data
   - Keep configuration file in version control
   - Use different configurations for different environments

2. **Output**
   - Use JSON format for programmatic use
   - Use YAML for readability
   - Use text format for quick checks

3. **Error Handling**
   - Check error codes
   - Handle API errors gracefully
   - Validate input before processing

4. **Performance**
   - Use appropriate batch sizes
   - Enable parallel processing when possible
   - Cache results when appropriate

## Examples

### Complete Workflow
```bash
# Analyze prompt
prompt-efficiency analyze "Your prompt" --output json > analysis.json

# Optimize based on analysis
prompt-efficiency optimize "Your prompt" --method compress --target-ratio 0.8 > optimized.txt

# Estimate cost
prompt-efficiency estimate-cost "Your prompt" --model gpt-4 --currency USD

# Scan repository
prompt-efficiency scan-repository ./src --include-analysis --output json > scan.json

# Apply macro
prompt-efficiency macro apply api-doc "Your API" --params "method=GET" > api.txt
```

### CI/CD Integration
```bash
# Run tests
prompt-efficiency test --path ./tests --parallel

# Deploy if tests pass
if [ $? -eq 0 ]; then
    prompt-efficiency deploy --version 1.0.0 --target production
fi
```

### Budget Management
```bash
# Set monthly budget
prompt-efficiency budget set 100 --period monthly --model gpt-4

# Monitor usage
prompt-efficiency budget metrics --period last_week --model gpt-4
```

## Support

### Getting Help
```bash
# Show help
prompt-efficiency --help

# Show command help
prompt-efficiency [command] --help

# Show version
prompt-efficiency --version
```

### Documentation
- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Examples](examples/)

### Support Channels
- Email: support@prompt.com
- GitHub Issues: https://github.com/yourusername/prompt-efficiency-suite/issues
- Documentation: https://docs.prompt.com
