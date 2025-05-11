"""Utils - A module for utility functions used across the prompt efficiency suite."""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration
    """
    with open(config_path, "r") as f:
        return json.load(f)


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to a file.

    Args:
        config: Configuration to save
        config_path: Path to save configuration to
    """
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def format_timestamp(timestamp: datetime) -> str:
    """Format a timestamp.

    Args:
        timestamp: Timestamp to format

    Returns:
        Formatted timestamp string
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to be safe for all operating systems.

    Args:
        filename: The filename to sanitize

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")
    # Ensure the filename is not empty
    if not sanitized:
        sanitized = "unnamed_file"
    return sanitized


def format_size(size_bytes: int) -> str:
    """Format a size in bytes to a human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human-readable size string
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def calculate_token_estimate(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Estimate the number of tokens in a text.

    Args:
        text: The text to estimate tokens for
        model_name: The model to estimate for

    Returns:
        Estimated number of tokens
    """
    # Simple estimation: 1 token ≈ 4 characters for English text
    # This is a rough estimate and may vary based on the model
    return len(text) // 4


def validate_prompt(prompt: str) -> bool:
    """Check if a prompt is valid.

    Args:
        prompt: The prompt to validate

    Returns:
        True if the prompt is valid, False otherwise
    """
    # This would be implemented to validate prompts
    return True


def extract_parameters(text: str) -> List[str]:
    """Extract parameter names from a text.

    Args:
        text: The text to extract parameters from

    Returns:
        List of parameter names
    """
    # Find all parameter-like patterns
    patterns: List[str] = [
        r"\{([^}]+)\}",  # {param}
        r"\[([^\]]+)\]",  # [param]
        r"<([^>]+)>",  # <param>
        r"\$([a-zA-Z_][a-zA-Z0-9_]*)",  # $param
    ]

    parameters = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        parameters.extend(match.group(1) for match in matches)

    return list(set(parameters))


def merge_configs(
    base_config: Dict[str, Any], override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge two configuration dictionaries.

    Args:
        base_config: Base configuration
        override_config: Configuration to override with

    Returns:
        Merged configuration
    """
    result = base_config.copy()

    for key, value in override_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result
