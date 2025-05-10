import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict:
    """Load configuration from a file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration
    """
    try:
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            if config_path.suffix == ".json":
                return json.load(f)
            elif config_path.suffix in [".yaml", ".yml"]:
                return yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported config file format: {config_path.suffix}")
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return {}


def save_config(config: Dict, config_path: str) -> bool:
    """Save configuration to a file.

    Args:
        config: Configuration dictionary to save
        config_path: Path to save the configuration file

    Returns:
        True if successful, False otherwise
    """
    try:
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            if config_path.suffix == ".json":
                json.dump(config, f, indent=2)
            elif config_path.suffix in [".yaml", ".yml"]:
                yaml.dump(config, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported config file format: {config_path.suffix}")
        return True
    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")
        return False


def format_timestamp(timestamp: datetime) -> str:
    """Format a timestamp for display.

    Args:
        timestamp: The timestamp to format

    Returns:
        Formatted timestamp string
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


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
    """Validate a prompt for basic requirements.

    Args:
        prompt: The prompt to validate

    Returns:
        True if valid, False otherwise
    """
    if not prompt or not isinstance(prompt, str):
        return False

    # Check minimum length
    if len(prompt) < 10:
        return False

    # Check for common issues
    if prompt.isspace():
        return False

    # Check for balanced quotes
    if prompt.count('"') % 2 != 0 or prompt.count("'") % 2 != 0:
        return False

    return True


def extract_parameters(text: str) -> List[str]:
    """Extract parameter names from a text.

    Args:
        text: The text to extract parameters from

    Returns:
        List of parameter names
    """
    # Find all parameter-like patterns
    patterns = [
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


def merge_configs(base_config: Dict, override_config: Dict) -> Dict:
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
