from pathlib import Path

import pytest

from prompt_efficiency_suite.config import get_default_config, load_config, save_config


def test_load_config() -> None:
    """Test loading configuration from a file."""
    config = load_config()
    assert isinstance(config, dict)
    assert "model" in config
    assert "max_tokens" in config
    assert "temperature" in config


def test_save_config() -> None:
    """Test saving configuration to a file."""
    config = {"model": "gpt-4", "max_tokens": 1000, "temperature": 0.7}
    output_path = Path("test_config.json")
    save_config(config, output_path)
    assert output_path.exists()
    output_path.unlink()  # Clean up


def test_get_default_config() -> None:
    """Test getting default configuration."""
    config = get_default_config()
    assert isinstance(config, dict)
    assert "model" in config
    assert "max_tokens" in config
    assert "temperature" in config
    assert config["model"] == "gpt-4"
    assert isinstance(config["max_tokens"], int)
    assert isinstance(config["temperature"], float)


def test_load_config_with_custom_path() -> None:
    """Test loading configuration from a custom path."""
    config = {"model": "gpt-4", "max_tokens": 1000, "temperature": 0.7}
    config_path = Path("test_config.json")
    save_config(config, config_path)

    loaded_config = load_config(config_path)
    assert loaded_config == config
    config_path.unlink()  # Clean up


def test_save_config_with_custom_path() -> None:
    """Test saving configuration to a custom path."""
    config = {"model": "gpt-4", "max_tokens": 1000, "temperature": 0.7}
    output_path = Path("custom_config.json")
    save_config(config, output_path)
    assert output_path.exists()
    output_path.unlink()  # Clean up
