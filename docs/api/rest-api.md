# REST API Documentation

## Overview

The Prompt Efficiency Suite provides a comprehensive REST API for programmatic access to all features.

## Base URL

```
https://api.prompt.com/v1
```

## Authentication

All API requests require authentication using JWT tokens.

### Obtaining a Token

```bash
curl -X POST https://api.prompt.com/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

### Using the Token

```bash
curl -H "Authorization: Bearer your_token" https://api.prompt.com/v1/health
```

## Rate Limiting

- Authenticated users: 100 requests per minute
- Unauthenticated users: 10 requests per minute

Rate limit headers are included in all responses:
- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Time until rate limit resets

## Endpoints

### 1. Prompt Analysis

#### Analyze Prompt
```http
POST /analyze
```

**Request Body:**
```json
{
  "prompt": "Your prompt text",
  "options": {
    "include_quality_metrics": true,
    "include_cost_estimate": true,
    "include_pattern_analysis": true
  }
}
```

**Response:**
```json
{
  "quality_metrics": {
    "clarity": 0.85,
    "completeness": 0.92,
    "consistency": 0.88
  },
  "cost_estimate": {
    "tokens": 150,
    "cost": 0.003,
    "currency": "USD"
  },
  "pattern_analysis": {
    "patterns_found": ["technical", "instruction"],
    "suggestions": ["Add more context", "Specify output format"]
  }
}
```

### 2. Prompt Optimization

#### Optimize Prompt
```http
POST /optimize
```

**Request Body:**
```json
{
  "prompt": "Your prompt text",
  "options": {
    "target_ratio": 0.8,
    "preserve_quality": true,
    "optimization_strategy": "cost"
  }
}
```

**Response:**
```json
{
  "optimized_prompt": "Optimized prompt text",
  "metrics": {
    "original_tokens": 150,
    "optimized_tokens": 120,
    "quality_preserved": 0.95
  }
}
```

### 3. Cost Estimation

#### Estimate Cost
```http
POST /estimate-cost
```

**Request Body:**
```json
{
  "prompt": "Your prompt text",
  "model": "gpt-4",
  "options": {
    "include_breakdown": true
  }
}
```

**Response:**
```json
{
  "total_cost": 0.003,
  "breakdown": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "cost_per_token": 0.00002
  }
}
```

### 4. Repository Scanning

#### Scan Repository
```http
POST /scan-repository
```

**Request Body:**
```json
{
  "repository_url": "https://github.com/username/repo",
  "options": {
    "include_analysis": true,
    "include_suggestions": true,
    "file_patterns": ["*.py", "*.js"]
  }
}
```

**Response:**
```json
{
  "scan_results": {
    "total_files": 100,
    "prompts_found": 25,
    "analysis_results": [...],
    "suggestions": [...]
  }
}
```

### 5. Model Translation

#### Translate Prompt
```http
POST /translate
```

**Request Body:**
```json
{
  "prompt": "Your prompt text",
  "source_model": "gpt-4",
  "target_model": "claude-2",
  "options": {
    "preserve_style": true
  }
}
```

**Response:**
```json
{
  "translated_prompt": "Translated prompt text",
  "metrics": {
    "quality_score": 0.92,
    "token_count": 120
  }
}
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

### Common Error Codes

- `AUTHENTICATION_FAILED`: Invalid or expired token
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INVALID_REQUEST`: Malformed request
- `MODEL_UNAVAILABLE`: Requested model is not available
- `INTERNAL_ERROR`: Server-side error

## Best Practices

### 1. Authentication
- Store tokens securely
- Implement token refresh
- Handle authentication errors

### 2. Rate Limiting
- Implement exponential backoff
- Monitor rate limit headers
- Cache responses when appropriate

### 3. Error Handling
- Implement proper error handling
- Log error responses
- Retry on appropriate errors

### 4. Performance
- Use compression
- Implement caching
- Batch requests when possible

## SDK Examples

### Python
```python
from prompt_efficiency import PromptEfficiencyClient

client = PromptEfficiencyClient(api_key="your_api_key")

# Analyze prompt
result = client.analyze_prompt(
    prompt="Your prompt text",
    include_quality_metrics=True
)

# Optimize prompt
optimized = client.optimize_prompt(
    prompt="Your prompt text",
    target_ratio=0.8
)
```

### JavaScript
```javascript
const { PromptEfficiencyClient } = require('prompt-efficiency');

const client = new PromptEfficiencyClient('your_api_key');

// Analyze prompt
const result = await client.analyzePrompt({
    prompt: 'Your prompt text',
    includeQualityMetrics: true
});

// Optimize prompt
const optimized = await client.optimizePrompt({
    prompt: 'Your prompt text',
    targetRatio: 0.8
});
```

## Support

- API Status: https://status.prompt.com
- Documentation: https://docs.prompt.com
- Support Email: api-support@prompt.com
- GitHub Issues: https://github.com/yourusername/prompt-efficiency-suite/issues
