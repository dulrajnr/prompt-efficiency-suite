import json
from pathlib import Path

import pytest

from prompt_efficiency_suite.model_translator import ModelConfig, ModelTranslator, ModelType, TranslationResult


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
    result = translator.translate(prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC)

    assert isinstance(result, TranslationResult)
    assert len(result.translated_prompt) > 0
    assert "Human:" in result.translated_prompt


def test_translate_prompt_style_adaptation(translator):
    """Test prompt translation with style adaptation."""
    prompt = "System: You are a helpful assistant.\nUser: This is a really very extremely important test."
    result = translator.translate(prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC)

    # Check if redundant words were removed
    translated = result.translated_prompt.lower()
    assert "really" not in translated
    assert "very" not in translated
    assert "extremely" not in translated


def test_translate_prompt_format_adaptation(translator):
    """Test prompt translation with format adaptation."""
    prompt = "System: You are a helpful assistant.\nUser: Hello!"
    result = translator.translate(prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC)

    # Check if format was adapted for Anthropic
    assert "Human:" in result.translated_prompt
    assert "Assistant:" in result.translated_prompt


def test_get_translation_stats(translator):
    """Test getting translation statistics."""
    prompt = "System: You are a helpful assistant.\nUser: This is a test prompt."
    translator.translate(prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC)

    stats = translator.get_translation_stats()

    assert isinstance(stats, dict)
    assert "total_translations" in stats
    assert stats["total_translations"] > 0


def test_invalid_model_type(translator):
    """Test handling of invalid model types."""
    with pytest.raises(ValueError):
        translator.translate(prompt="Test", source_format="invalid_model", target_format=ModelType.OPENAI)


def test_export_templates(translator, tmp_path):
    """Test exporting format templates."""
    prompt = "System: You are a helpful assistant.\nUser: This is a test prompt."
    translator.translate(prompt=prompt, source_format=ModelType.OPENAI, target_format=ModelType.ANTHROPIC)

    output_path = tmp_path / "templates.json"
    translator.export_templates(output_path)

    assert output_path.exists()
    with open(output_path) as f:
        templates = json.load(f)
        assert "templates" in templates
