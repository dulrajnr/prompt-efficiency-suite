# Prompt Efficiency Suite API Documentation

## Overview

The Prompt Efficiency Suite provides a RESTful API for analyzing, optimizing, and managing prompts for large language models. This documentation covers all available endpoints, request/response formats, and usage examples.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require authentication using a Bearer token:

```http
Authorization: Bearer <your-token>
```

## Endpoints

### Prompt Analysis

#### Analyze Prompt
```http
POST /analyze
```

Analyzes a prompt for quality and provides suggestions.

**Request Body:**
```json
{
    "prompt": "Your prompt text here",
    "options": {
        "include_patterns": true,
        "include_suggestions": true
    }
}
```

**Response:**
```json
{
    "clarity_score": 0.85,
    "structure_score": 0.92,
    "complexity_score": 0.78,
    "quality_score": 0.85,
    "patterns": ["chain_of_thought", "few_shot"],
    "suggestions": [
        "Consider adding more context",
        "Break down complex instructions"
    ]
}
```

### Prompt Optimization

#### Optimize Prompt
```http
POST /optimize
```

Optimizes a prompt for better performance.

**Request Body:**
```json
{
    "prompt": "Your prompt text here",
    "method": "trim",  // or "compress", "enhance"
    "options": {
        "preserve_ratio": 0.8,
        "domain_terms": ["term1", "term2"]
    }
}
```

**Response:**
```json
{
    "optimized_prompt": "Optimized prompt text",
    "savings": {
        "tokens": 150,
        "percentage": 25.5
    },
    "quality_score": 0.92
}
```

### Cost Estimation

#### Estimate Cost
```http
POST /estimate-cost
```

Estimates the cost of using a prompt with a specific model.

**Request Body:**
```json
{
    "prompt": "Your prompt text here",
    "model": "gpt-4",
    "currency": "USD"
}
```

**Response:**
```json
{
    "input_tokens": 150,
    "estimated_output_tokens": 200,
    "total_cost": 0.0125,
    "currency": "USD"
}
```

### Repository Scanning

#### Scan Repository
```http
POST /scan-repository
```

Scans a repository for prompts and analyzes them.

**Request Body:**
```json
{
    "directory": "/path/to/repo",
    "include_patterns": ["*.py", "*.md"],
    "exclude_patterns": ["tests/*", "docs/*"]
}
```

**Response:**
```json
{
    "total_files": 100,
    "prompts_found": 25,
    "average_quality": 0.85,
    "estimated_cost": 12.50,
    "currency": "USD",
    "details": [
        {
            "file": "path/to/file.py",
            "quality_score": 0.92,
            "estimated_cost": 0.50
        }
    ]
}
```

### Model Translation

#### Translate Prompt
```http
POST /translate
```

Translates a prompt optimized for one model to work with another model.

**Request Body:**
```json
{
    "prompt": "Your prompt text here",
    "source_model": "gpt-4",
    "target_model": "gpt-3.5-turbo"
}
```

**Response:**
```json
{
    "translated_prompt": "Translated prompt text",
    "warnings": [
        "Some GPT-4 specific features may not work as expected"
    ]
}
```

## Error Handling

All endpoints return standard HTTP status codes and error messages:

```json
{
    "error": {
        "code": "INVALID_REQUEST",
        "message": "Detailed error message",
        "details": {
            "field": "prompt",
            "issue": "required field missing"
        }
    }
}
```

Common error codes:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

## Rate Limiting

API requests are rate-limited to:
- 100 requests per minute for authenticated users
- 10 requests per minute for unauthenticated users

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1625097600
```

## Metrics

The API exposes Prometheus metrics at `/metrics`:

- `prompt_analysis_total`: Total number of prompts analyzed
- `prompt_optimization_total`: Total number of prompts optimized
- `cost_estimation_total`: Total number of cost estimations
- `prompt_analysis_duration_seconds`: Time spent analyzing prompts
- `prompt_optimization_duration_seconds`: Time spent optimizing prompts
- `active_prompt_analyses`: Number of active analyses
- `active_prompt_optimizations`: Number of active optimizations

## WebSocket API

For real-time prompt analysis and optimization, a WebSocket API is available at `/ws`:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    const result = JSON.parse(event.data);
    console.log(result);
};

ws.send(JSON.stringify({
    "action": "analyze",
    "prompt": "Your prompt text here"
}));
```

## SDK Examples

### Python
```python
from prompt_efficiency_suite import PromptEfficiencyClient

client = PromptEfficiencyClient(api_key="your-api-key")

# Analyze prompt
result = client.analyze_prompt("Your prompt text here")
print(result.quality_score)

# Optimize prompt
optimized = client.optimize_prompt(
    prompt="Your prompt text here",
    method="trim",
    options={"preserve_ratio": 0.8}
)
print(optimized.savings)
```

### JavaScript
```javascript
const { PromptEfficiencyClient } = require('prompt-efficiency-suite');

const client = new PromptEfficiencyClient('your-api-key');

// Analyze prompt
client.analyzePrompt('Your prompt text here')
    .then(result => console.log(result.qualityScore));

// Optimize prompt
client.optimizePrompt('Your prompt text here', {
    method: 'trim',
    options: { preserveRatio: 0.8 }
})
    .then(optimized => console.log(optimized.savings));
```

## Support

For API support:
- Email: api-support@prompt-efficiency.com
- Documentation: https://docs.prompt-efficiency.com
- GitHub Issues: https://github.com/prompt-efficiency/suite/issues
