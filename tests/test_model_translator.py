import json
from pathlib import Path

import pytest

from prompt_efficiency_suite.model_translator import (
    ModelConfig,
    ModelTranslator,
    ModelType,
    TranslationResult,
)


@pytest.fixture
def translator():
    return ModelTranslator()


def test_model_configs_loaded(translator):
    """Test that model configurations are properly loaded."""
    assert ModelType.OPENAI in translator.model_configs
    assert ModelType.ANTHROPIC in translator.model_configs

    openai_config = translator.model_configs[ModelType.OPENAI]
    assert isinstance(openai_config, ModelConfig)
    assert openai_config.max_tokens > 0


def test_style_patterns_loaded(translator):
    """Test that style patterns are properly loaded."""
    assert "concise" in translator.style_patterns
    assert "detailed" in translator.style_patterns

    concise_patterns = translator.style_patterns["concise"]
    assert "remove_redundant" in concise_patterns
    assert "simplify_phrases" in concise_patterns
    assert "replace_with" in concise_patterns


def test_translate_prompt_basic(translator):
    """Test basic prompt translation."""
    prompt = "System: You are a helpful assistant.\nUser: This is a test prompt."
    result = translator.translate(
        prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC
    )

    assert isinstance(result, TranslationResult)
    assert len(result.translated_prompt) > 0
    assert "Human:" in result.translated_prompt


def test_translate_prompt_style_adaptation(translator):
    """Test prompt translation with style adaptation."""
    prompt = "System: You are a helpful assistant.\nUser: This is a really very extremely important test."
    result = translator.translate(
        prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC
    )

    # Check if redundant words were removed
    translated = result.translated_prompt.lower()
    assert "really" not in translated
    assert "very" not in translated
    assert "extremely" not in translated


def test_translate_prompt_format_adaptation(translator):
    """Test prompt translation with format adaptation."""
    prompt = "System: You are a helpful assistant.\nUser: Hello!"
    result = translator.translate(
        prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC
    )

    # Check if format was adapted for Anthropic
    assert "Human:" in result.translated_prompt
    assert "Assistant:" in result.translated_prompt


def test_get_translation_stats(translator):
    """Test getting translation statistics."""
    prompt = "System: You are a helpful assistant.\nUser: This is a test prompt."
    translator.translate(
        prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC
    )

    stats = translator.get_translation_stats()

    assert isinstance(stats, dict)
    assert "total_translations" in stats
    assert stats["total_translations"] > 0


def test_invalid_model_type(translator):
    """Test handling of invalid model types."""
    with pytest.raises(ValueError):
        translator.translate(
            prompt="Test", source_format="invalid_model", target_format=ModelType.OPENAI
        )


def test_export_templates(translator, tmp_path):
    """Test exporting format templates."""
    prompt = "System: You are a helpful assistant.\nUser: This is a test prompt."
    translator.translate(
        prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC
    )

    output_path = tmp_path / "templates.json"
    translator.export_templates(output_path)

    assert output_path.exists()
    with open(output_path) as f:
        templates = json.load(f)
        assert "templates" in templates


def test_translator_initialization() -> None:
    """Test translator initialization."""
    translator = ModelTranslator()
    assert translator is not None


def test_translate_prompt() -> None:
    """Test translating a prompt between models."""
    translator = ModelTranslator()
    prompt = "This is a test prompt"
    result = translator.translate(prompt, ModelType.GPT4, ModelType.GPT35)
    assert isinstance(result, str)
    assert len(result) > 0
    assert result != prompt  # Should be different after translation


def test_translate_with_config() -> None:
    """Test translating a prompt with custom configuration."""
    translator = ModelTranslator()
    prompt = "This is a test prompt"
    config = {
        "preserve_formatting": True,
        "maintain_context": True,
        "optimize_for_target": True,
    }
    result = translator.translate(prompt, ModelType.GPT4, ModelType.GPT35, config)
    assert isinstance(result, str)
    assert len(result) > 0
    assert result != prompt


def test_translate_empty_prompt() -> None:
    """Test translating an empty prompt."""
    translator = ModelTranslator()
    prompt = ""
    result = translator.translate(prompt, ModelType.GPT4, ModelType.GPT35)
    assert isinstance(result, str)
    assert result == prompt  # Empty prompt should remain empty


def test_translate_prompt_with_special_chars() -> None:
    """Test translating a prompt with special characters."""
    translator = ModelTranslator()
    prompt = "Hello! How are you? I'm fine, thanks."
    result = translator.translate(prompt, ModelType.GPT4, ModelType.GPT35)
    assert isinstance(result, str)
    assert len(result) > 0
    assert result != prompt


def test_get_model_capabilities() -> None:
    """Test getting model capabilities."""
    translator = ModelTranslator()
    capabilities = translator.get_model_capabilities(ModelType.GPT4)
    assert isinstance(capabilities, dict)
    assert "max_tokens" in capabilities
    assert "supports_functions" in capabilities
    assert "supports_streaming" in capabilities
