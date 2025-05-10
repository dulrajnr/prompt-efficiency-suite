# REST API Documentation

## Overview

The Prompt Efficiency Suite provides a comprehensive REST API for interacting with all features of the system. This document details all available endpoints, their usage, and examples.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require JWT token-based authentication. To obtain a token:

```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

Response:
```json
{
    "access_token": "your.jwt.token",
    "token_type": "bearer"
}
```

Include the token in subsequent requests:
```http
Authorization: Bearer your.jwt.token
```

## Rate Limiting

- Authenticated users: 100 requests per minute
- Unauthenticated users: 10 requests per minute
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`: Maximum requests per window
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time until rate limit resets

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
    "estimated_cost": 0.0025,
    "token_count": 150,
    "currency": "USD",
    "model": "gpt-4"
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
    "repository_path": "/path/to/repo",
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
    "prompts_found": 25,
    "analysis_results": [
        {
            "file_path": "src/main.py",
            "line_number": 42,
            "prompt": "Found prompt text",
            "analysis": {
                "quality_score": 0.85,
                "suggestions": ["Add more context"]
            }
        }
    ],
    "summary": {
        "total_tokens": 1500,
        "estimated_cost": 0.025,
        "optimization_potential": 0.15
    }
}
```

### Model Translation

#### Translate Prompt
```http
POST /translate
```

Translates a prompt between different models.

**Request Body:**
```json
{
    "prompt": "Your prompt text here",
    "source_model": "gpt-4",
    "target_model": "claude-2",
    "options": {
        "preserve_style": true,
        "optimize_tokens": true
    }
}
```

**Response:**
```json
{
    "translated_prompt": "Translated prompt text",
    "token_count": {
        "original": 150,
        "translated": 145
    },
    "style_preserved": true
}
```

### Health Check

#### Check Health
```http
GET /health
```

Checks the health status of the API and its components.

**Response:**
```json
{
    "status": "healthy",
    "components": {
        "api": "healthy",
        "database": "healthy",
        "cache": "healthy",
        "model_services": "healthy"
    },
    "version": "1.0.0",
    "uptime": "2d 5h 30m"
}
```

### Metrics

#### Get Metrics
```http
GET /metrics
```

Returns Prometheus metrics for monitoring.

**Response:**
```
# HELP prompt_efficiency_requests_total Total number of requests
# TYPE prompt_efficiency_requests_total counter
prompt_efficiency_requests_total{endpoint="/analyze"} 150
prompt_efficiency_requests_total{endpoint="/optimize"} 75

# HELP prompt_efficiency_token_usage_total Total tokens used
# TYPE prompt_efficiency_token_usage_total counter
prompt_efficiency_token_usage_total{model="gpt-4"} 15000
prompt_efficiency_token_usage_total{model="claude-2"} 12000
```

### Web UI

#### Dashboard
```http
GET /ui/dashboard
```

Access the web UI dashboard.

**Response:**
- HTML page with interactive dashboard
- Real-time metrics and visualizations
- Usage statistics and trends

#### Leaderboard
```http
GET /ui/leaderboard
```

Access the benchmark leaderboard.

**Response:**
- HTML page with benchmark results
- Performance comparisons
- Historical data

#### Dictionary Health
```http
GET /ui/dictionary/health
```

Check the health of the dictionary service.

**Response:**
```json
{
    "status": "healthy",
    "entries": 15000,
    "last_update": "2024-03-20T10:00:00Z",
    "coverage": {
        "domains": ["technical", "medical", "legal"],
        "languages": ["en", "es", "fr"]
    }
}
```

### Grafana Integration

#### Dashboard Data
```http
GET /grafana/dashboard
```

Access Grafana dashboard data.

**Response:**
```json
{
    "dashboard": {
        "id": "prompt-efficiency",
        "title": "Prompt Efficiency Metrics",
        "panels": [
            {
                "title": "Token Usage",
                "type": "graph",
                "datasource": "prometheus"
            },
            {
                "title": "Cost Analysis",
                "type": "graph",
                "datasource": "prometheus"
            }
        ]
    }
}
```

## Error Handling

All endpoints follow a consistent error response format:

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

Common error codes:
- `AUTH_REQUIRED`: Authentication required
- `INVALID_TOKEN`: Invalid or expired token
- `RATE_LIMITED`: Rate limit exceeded
- `INVALID_REQUEST`: Invalid request parameters
- `SERVER_ERROR`: Internal server error

## Best Practices

1. Always include authentication token
2. Handle rate limiting appropriately
3. Use appropriate content types
4. Implement proper error handling
5. Cache responses when possible
6. Monitor usage and costs
7. Follow security guidelines

## Examples

### Python Example
```python
import requests

def analyze_prompt(prompt: str, api_key: str) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "http://localhost:8000/api/v1/analyze",
        headers=headers,
        json={"prompt": prompt}
    )

    return response.json()
```

### JavaScript Example
```javascript
async function optimizePrompt(prompt, apiKey) {
    const response = await fetch('http://localhost:8000/api/v1/optimize', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });

    return await response.json();
}
```

## Support

For API support:
1. Check the [API Status Page](https://status.prompt.com)
2. Review the [API Documentation](https://docs.prompt.com/api)
3. Contact [API Support](mailto:api-support@prompt.com)
