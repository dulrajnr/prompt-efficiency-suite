# Cross-Model Prompt Translator

The Cross-Model Prompt Translator is a powerful tool that enables seamless translation of prompts between different LLM models while maintaining effectiveness and optimizing for model-specific requirements.

## Features

### Core Translation
- Translates prompts between different LLM models (GPT-4, GPT-3.5, Claude, PaLM, LLaMA, Mistral)
- Preserves prompt structure and intent
- Adapts formatting and style to target model conventions
- Handles system messages, instructions, examples, and context

### Validation
- Validates prompts before translation
- Checks model-specific requirements (e.g., system message requirements)
- Validates token limits
- Verifies markdown support
- Provides detailed validation results with errors and warnings

### Optimization
- Optimizes prompts for better performance
- Removes redundant phrases and words
- Adapts style based on model preferences
- Limits example count for optimal results
- Estimates token savings and costs

## Usage

### Basic Translation

```python
from prompt_efficiency_suite.translator import PromptTranslator
from prompt_efficiency_suite.translator.model_types import ModelType

# Create translator instance
translator = PromptTranslator()

# Translate a string prompt
result = translator.translate(
    prompt="Your prompt here",
    source_model=ModelType.GPT4,
    target_model=ModelType.CLAUDE,
    optimize=True
)

# Access translation results
print(result.translated_prompt)
print(result.validation_result.is_valid)
print(result.optimization_result.improvements)
print(result.estimated_cost)
```

### Using PromptComponents

```python
from prompt_efficiency_suite.translator import PromptComponents

# Create structured prompt
components = PromptComponents(
    system_message="You are a helpful assistant",
    instruction="Write a story",
    examples=["Example 1", "Example 2"],
    context="This is a test",
    constraints="Keep it short",
    output_format="Markdown"
)

# Translate components
result = translator.translate(
    prompt=components,
    source_model=ModelType.CLAUDE,
    target_model=ModelType.GPT35,
    optimize=True
)
```

## Model Support

The translator supports the following models:

| Model | Token Limit | System Message Required | Markdown Support |
|-------|-------------|------------------------|-----------------|
| GPT-4 | 8192 | Yes | Yes |
| GPT-3.5 | 4096 | Yes | Yes |
| Claude | 100000 | No | Yes |
| Claude Instant | 100000 | No | Yes |
| PaLM | 8192 | No | No |
| LLaMA | 4096 | No | No |
| Mistral | 8192 | No | Yes |

## Validation Rules

The validator checks for:

1. Required Components
   - System message (if required by model)
   - Instruction (always required)

2. Token Limits
   - Ensures prompt fits within model's token limit
   - Estimates tokens based on character count

3. Formatting
   - Checks markdown support
   - Validates example count (warns if > 3)
   - Validates context length (warns if > 100 words)

## Optimization Strategies

The optimizer applies the following strategies:

1. Style Adaptation
   - Concise: Removes redundant words and phrases
   - Clear: Adds clarifying phrases and breaks long sentences
   - Detailed: Preserves information while maintaining clarity

2. Component Optimization
   - System Message: Removes redundant AI assistant references
   - Instruction: Removes unnecessary politeness markers
   - Examples: Limits to 3 most relevant examples
   - Context: Removes redundant context markers
   - Constraints: Simplifies constraint statements

3. Token Optimization
   - Removes redundant phrases
   - Simplifies complex sentences
   - Estimates token savings

## Best Practices

1. Prompt Structure
   - Always include a clear instruction
   - Use system messages when required by the model
   - Keep examples relevant and concise
   - Provide context only when necessary

2. Optimization
   - Enable optimization for better performance
   - Review optimization suggestions
   - Consider token savings vs. clarity

3. Validation
   - Always check validation results
   - Address validation errors before translation
   - Consider validation warnings for improvements

## Error Handling

The translator provides detailed error information through the `TranslationResult`:

```python
result = translator.translate(prompt, source_model, target_model)

if not result.validation_result.is_valid:
    print("Validation Errors:")
    for error in result.validation_result.errors:
        print(f"- {error}")

if result.validation_result.warnings:
    print("Warnings:")
    for warning in result.validation_result.warnings:
        print(f"- {warning}")
```

## Cost Estimation

The translator provides cost estimates based on:
- Token count
- Model-specific pricing
- Optimization savings

```python
result = translator.translate(prompt, source_model, target_model)
print(f"Estimated cost: ${result.estimated_cost:.4f}")
```

## Contributing

To contribute to the translator:
1. Add new model support in `model_types.py`
2. Implement model-specific style profiles
3. Add new validation rules
4. Develop additional optimization strategies

## License

This project is licensed under the MIT License - see the LICENSE file for details.
