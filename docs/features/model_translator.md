# Model Translator Documentation

## Overview

The Model Translator is a powerful component of the Prompt Efficiency Suite that enables seamless translation of prompts between different LLM models. It handles style adaptation, format conversion, and token optimization while maintaining prompt quality.

## Features

- **Cross-Model Translation**: Convert prompts between GPT-4, Claude, and other models
- **Style Adaptation**: Adjust writing style to match target model preferences
- **Format Conversion**: Handle model-specific formatting requirements
- **Token Optimization**: Optimize prompts for token usage and cost
- **Model Comparison**: Compare prompt performance across different models

## Installation

```bash
pip install prompt-efficiency-suite
```

## Quick Start

```python
from prompt_efficiency_suite import ModelTranslator, ModelType

# Initialize translator
translator = ModelTranslator()

# Translate a prompt
translated = translator.translate_prompt(
    prompt="Your prompt here",
    source_model=ModelType.GPT4,
    target_model=ModelType.CLAUDE,
    preserve_style=True
)

# Compare models
results = translator.compare_models(
    prompt="Your prompt here",
    models=[ModelType.GPT4, ModelType.CLAUDE]
)
```

## API Reference

### ModelTranslator

#### `translate_prompt(prompt: str, source_model: ModelType, target_model: ModelType, preserve_style: bool = True) -> str`

Translate a prompt from one model to another.

**Parameters:**
- `prompt`: The original prompt text
- `source_model`: The model the prompt was originally written for
- `target_model`: The model to translate the prompt for
- `preserve_style`: Whether to maintain the original writing style

**Returns:**
- Translated prompt optimized for the target model

**Example:**
```python
translated = translator.translate_prompt(
    prompt="system: You are a helpful assistant.\nuser: Hello!",
    source_model=ModelType.GPT4,
    target_model=ModelType.CLAUDE
)
```

#### `compare_models(prompt: str, models: List[ModelType]) -> Dict[ModelType, Dict]`

Compare how a prompt would perform across different models.

**Parameters:**
- `prompt`: The prompt to compare
- `models`: List of models to compare against

**Returns:**
- Dictionary with model-specific metrics

**Example:**
```python
results = translator.compare_models(
    prompt="Your prompt here",
    models=[ModelType.GPT4, ModelType.CLAUDE]
)
```

#### `get_model_specifics(model: ModelType) -> ModelConfig`

Get configuration details for a specific model.

**Parameters:**
- `model`: The model to get details for

**Returns:**
- Model configuration object

**Example:**
```python
config = translator.get_model_specifics(ModelType.GPT4)
print(f"Max tokens: {config.max_tokens}")
print(f"Cost per 1K tokens: ${config.cost_per_1k_tokens}")
```

## REST API

### POST /api/v1/translate

Translate a prompt from one model to another.

**Request:**
```json
{
  "prompt": "Your prompt here",
  "source_model": "gpt-4",
  "target_model": "claude-3",
  "preserve_style": true
}
```

**Response:**
```json
{
  "translated_prompt": "Translated prompt",
  "original_tokens": 100,
  "translated_tokens": 90,
  "estimated_cost": 0.0015,
  "style_compatibility": 0.95,
  "format_compatibility": 0.98
}
```

### POST /api/v1/compare

Compare prompt performance across models.

**Request:**
```json
{
  "prompt": "Your prompt here",
  "models": ["gpt-4", "claude-3"]
}
```

**Response:**
```json
{
  "results": {
    "gpt-4": {
      "estimated_tokens": 100,
      "estimated_cost": 0.003,
      "style_compatibility": 0.95,
      "format_compatibility": 0.98
    },
    "claude-3": {
      "estimated_tokens": 90,
      "estimated_cost": 0.0015,
      "style_compatibility": 0.92,
      "format_compatibility": 0.95
    }
  }
}
```

### GET /api/v1/models

List all supported models and their configurations.

**Response:**
```json
{
  "models": {
    "gpt-4": {
      "max_tokens": 8192,
      "cost_per_1k_tokens": 0.03,
      "preferred_style": "concise",
      "temperature_range": [0.0, 2.0],
      "stop_sequences": ["\n\n", "###"],
      "special_tokens": {
        "system": "system",
        "user": "user",
        "assistant": "assistant"
      }
    },
    "claude-3": {
      "max_tokens": 100000,
      "cost_per_1k_tokens": 0.015,
      "preferred_style": "detailed",
      "temperature_range": [0.0, 1.0],
      "stop_sequences": ["\n\nHuman:", "\n\nAssistant:"],
      "special_tokens": {
        "human": "Human:",
        "assistant": "Assistant:"
      }
    }
  }
}
```

## Best Practices

1. **Style Preservation**
   - Use `preserve_style=True` when maintaining consistent tone
   - Use `preserve_style=False` for model-specific optimization

2. **Token Optimization**
   - Monitor token usage across models
   - Use model comparison to find cost-effective options

3. **Format Adaptation**
   - Be aware of model-specific formatting requirements
   - Test translated prompts before deployment

4. **Model Selection**
   - Compare models for your specific use case
   - Consider cost, latency, and quality requirements

## Troubleshooting

### Common Issues

1. **Style Inconsistency**
   - Check model-specific style preferences
   - Adjust `preserve_style` parameter
   - Review style patterns

2. **Format Errors**
   - Verify model-specific formatting
   - Check special tokens
   - Test with sample prompts

3. **Token Limit Exceeded**
   - Use token optimization
   - Compare token usage across models
   - Adjust prompt length

### Getting Help

- Check the [API Documentation](../api.md)
- Visit our [GitHub Issues](https://github.com/yourorg/prompt-efficiency-suite/issues)
- Contact support at support@prompt-efficiency-suite.com 