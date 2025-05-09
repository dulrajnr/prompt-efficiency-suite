# Prompt Analyzer Documentation

## Overview

The Prompt Analyzer is a powerful component of the Prompt Efficiency Suite that helps analyze prompts for quality, effectiveness, and potential improvements. It provides detailed metrics, actionable suggestions, and insights to help create better prompts.

## Features

- **Quality Analysis**: Evaluate prompt clarity, specificity, and structure
- **Effectiveness Metrics**: Measure prompt effectiveness across multiple dimensions
- **Cost Estimation**: Estimate token usage and costs
- **Complexity Assessment**: Determine prompt complexity level
- **Improvement Suggestions**: Get actionable suggestions for prompt improvement
- **Strengths & Weaknesses**: Identify prompt strengths and areas for improvement

## Installation

```bash
pip install prompt-efficiency-suite
```

## Quick Start

```python
from prompt_efficiency_suite import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

# Initialize analyzer
analyzer = PromptAnalyzer()

# Analyze a prompt
result = analyzer.analyze_prompt(
    prompt="Your prompt here",
    model=ModelType.GPT4,
    target_complexity="medium"
)

# Access metrics
print(f"Overall Score: {result.metrics.overall_score}")
print(f"Clarity Score: {result.metrics.clarity_score}")
print(f"Token Count: {result.metrics.token_count}")

# Get suggestions
for suggestion in result.suggestions:
    print(suggestion)

# View strengths and weaknesses
print("\nStrengths:")
for strength in result.strengths:
    print(f"- {strength}")

print("\nWeaknesses:")
for weakness in result.weaknesses:
    print(f"- {weakness}")
```

## API Reference

### PromptAnalyzer

#### `analyze_prompt(prompt: str, model: ModelType, target_complexity: Optional[str] = None) -> AnalysisResult`

Analyze a prompt for quality, effectiveness, and potential improvements.

**Parameters:**
- `prompt`: The prompt to analyze
- `model`: The target model
- `target_complexity`: Optional target complexity level

**Returns:**
- AnalysisResult with metrics, suggestions, strengths, and weaknesses

**Example:**
```python
result = analyzer.analyze_prompt(
    prompt="Your prompt here",
    model=ModelType.GPT4,
    target_complexity="medium"
)
```

### AnalysisMetrics

Metrics for prompt analysis.

**Attributes:**
- `clarity_score`: Score for prompt clarity (0-1)
- `specificity_score`: Score for prompt specificity (0-1)
- `structure_score`: Score for prompt structure (0-1)
- `context_score`: Score for prompt context (0-1)
- `instruction_score`: Score for prompt instructions (0-1)
- `overall_score`: Overall quality score (0-1)
- `token_count`: Number of tokens in the prompt
- `estimated_cost`: Estimated cost for the prompt
- `complexity_level`: Complexity level (low, medium, high, very_high)

### AnalysisResult

Result of prompt analysis.

**Attributes:**
- `metrics`: AnalysisMetrics object
- `suggestions`: List of improvement suggestions
- `strengths`: List of prompt strengths
- `weaknesses`: List of prompt weaknesses
- `timestamp`: Analysis timestamp

## REST API

### POST /api/v1/analyze

Analyze a prompt.

**Request:**
```json
{
  "prompt": "Your prompt here",
  "model": "gpt-4",
  "target_complexity": "medium"
}
```

**Response:**
```json
{
  "metrics": {
    "clarity_score": 0.8,
    "specificity_score": 0.7,
    "structure_score": 0.9,
    "context_score": 0.6,
    "instruction_score": 0.8,
    "overall_score": 0.76,
    "token_count": 100,
    "estimated_cost": 0.1
  },
  "suggestions": [
    "Consider adding more context",
    "Make instructions more explicit"
  ],
  "strengths": [
    "High clarity with good use of clear language",
    "Well-structured with clear organization"
  ],
  "weaknesses": [
    "Weak context - needs more background",
    "Unclear instructions - needs more direction"
  ],
  "timestamp": "2024-03-20T12:00:00Z"
}
```

### GET /api/v1/metrics

Get detailed metrics for a prompt.

**Parameters:**
- `prompt`: The prompt to analyze
- `model`: The target model

**Response:**
```json
{
  "metrics": {
    "clarity_score": 0.8,
    "specificity_score": 0.7,
    "structure_score": 0.9,
    "context_score": 0.6,
    "instruction_score": 0.8,
    "overall_score": 0.76,
    "token_count": 100,
    "estimated_cost": 0.1,
    "complexity_level": "medium"
  }
}
```

### GET /api/v1/suggestions

Get improvement suggestions for a prompt.

**Parameters:**
- `prompt`: The prompt to analyze
- `model`: The target model
- `target_complexity`: Optional target complexity level

**Response:**
```json
{
  "suggestions": [
    "Consider adding more context",
    "Make instructions more explicit"
  ],
  "strengths": [
    "High clarity with good use of clear language",
    "Well-structured with clear organization"
  ],
  "weaknesses": [
    "Weak context - needs more background",
    "Unclear instructions - needs more direction"
  ]
}
```

## Analysis Dimensions

1. **Clarity**
   - Clear language usage
   - Explicit instructions
   - Unambiguous requirements
   - Proper formatting

2. **Specificity**
   - Detailed requirements
   - Concrete examples
   - Step-by-step instructions
   - Quantifiable metrics

3. **Structure**
   - Clear sections
   - Logical flow
   - Proper formatting
   - Consistent style

4. **Context**
   - Background information
   - Relevant details
   - Scope definition
   - Purpose clarification

5. **Instructions**
   - Action-oriented
   - Clear objectives
   - Output format
   - Success criteria

## Complexity Levels

1. **Low**
   - Up to 100 tokens
   - Up to 2 sections
   - Simple instructions
   - Minimal context

2. **Medium**
   - Up to 300 tokens
   - Up to 4 sections
   - Detailed instructions
   - Moderate context

3. **High**
   - Up to 600 tokens
   - Up to 6 sections
   - Complex instructions
   - Extensive context

4. **Very High**
   - More than 600 tokens
   - More than 6 sections
   - Complex requirements
   - Comprehensive context

## Best Practices

1. **Clarity**
   - Use clear, direct language
   - Avoid ambiguity
   - Be explicit about requirements
   - Use proper formatting

2. **Specificity**
   - Provide concrete examples
   - Include specific metrics
   - Give step-by-step instructions
   - Define success criteria

3. **Structure**
   - Use clear section markers
   - Maintain logical flow
   - Follow consistent format
   - Organize information well

4. **Context**
   - Provide relevant background
   - Define scope clearly
   - Explain purpose
   - Include necessary details

5. **Instructions**
   - Be action-oriented
   - Specify output format
   - Define success criteria
   - Include examples

## Troubleshooting

### Common Issues

1. **Low Clarity**
   - Check language usage
   - Review instructions
   - Verify formatting
   - Ensure explicitness

2. **Low Specificity**
   - Add more details
   - Include examples
   - Provide metrics
   - Give step-by-step guidance

3. **Poor Structure**
   - Use section markers
   - Improve organization
   - Check formatting
   - Ensure logical flow

4. **Weak Context**
   - Add background
   - Define scope
   - Explain purpose
   - Include relevant details

5. **Unclear Instructions**
   - Make more explicit
   - Add examples
   - Specify format
   - Define criteria

### Getting Help

- Check the [API Documentation](../api.md)
- Visit our [GitHub Issues](https://github.com/yourorg/prompt-efficiency-suite/issues)
- Contact support at support@prompt-efficiency-suite.com 