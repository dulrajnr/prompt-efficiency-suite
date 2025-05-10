"""
Model translator for converting prompts between different model formats.
"""

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Supported model types."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    CUSTOM = "custom"


@dataclass
class ModelConfig:
    """Configuration for a specific model."""

    model_type: ModelType
    system_prefix: str = ""
    user_prefix: str = ""
    assistant_prefix: str = ""
    system_suffix: str = ""
    user_suffix: str = ""
    assistant_suffix: str = ""
    max_tokens: int = 4096
    preferred_style: str = "balanced"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    """Result of prompt translation."""

    original_prompt: str
    translated_prompt: str
    source_format: ModelType
    target_format: ModelType
    metadata: Dict[str, Any]


class ModelTranslator:
    """A class for translating prompts between different model formats."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the ModelTranslator.

        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.translation_history: List[TranslationResult] = []
        self.format_templates = self._load_format_templates()
        self.model_configs = self._load_model_configs()
        self.style_patterns = self._load_style_patterns()

    def _load_model_configs(self) -> Dict[ModelType, ModelConfig]:
        """Load model configurations.

        Returns:
            Dict[ModelType, ModelConfig]: Model configurations.
        """
        return {
            ModelType.OPENAI: ModelConfig(model_type=ModelType.OPENAI, max_tokens=4096, preferred_style="balanced"),
            ModelType.ANTHROPIC: ModelConfig(
                model_type=ModelType.ANTHROPIC, max_tokens=8192, preferred_style="concise"
            ),
            ModelType.COHERE: ModelConfig(model_type=ModelType.COHERE, max_tokens=2048, preferred_style="concise"),
            ModelType.CUSTOM: ModelConfig(model_type=ModelType.CUSTOM, max_tokens=4096, preferred_style="balanced"),
        }

    def _load_style_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load style patterns.

        Returns:
            Dict[str, Dict[str, Any]]: Style patterns.
        """
        return {
            "concise": {
                "remove_redundant": True,
                "simplify_phrases": True,
                "replace_with": {
                    r"really\s+very\s+extremely": "",
                    r"really\s+very": "",
                    r"really": "",
                    r"very": "",
                    r"extremely": "",
                    r"basically": "",
                    r"actually": "",
                },
            },
            "detailed": {
                "remove_redundant": False,
                "simplify_phrases": False,
                "add_context": True,
                "expand_acronyms": True,
            },
            "balanced": {"remove_redundant": True, "simplify_phrases": False, "preserve_context": True},
        }

    def translate(
        self,
        prompt: str,
        source_format: Union[str, ModelType],
        target_format: Union[str, ModelType],
        translation_params: Optional[Dict[str, Any]] = None,
    ) -> TranslationResult:
        """Translate a prompt between formats.

        Args:
            prompt (str): Prompt to translate.
            source_format (Union[str, ModelType]): Source format.
            target_format (Union[str, ModelType]): Target format.
            translation_params (Optional[Dict[str, Any]]): Translation parameters.

        Returns:
            TranslationResult: Translation result.
        """
        # Convert string formats to enum
        if isinstance(source_format, str):
            source_format = ModelType(source_format.lower())
        if isinstance(target_format, str):
            target_format = ModelType(target_format.lower())

        params = translation_params or {}

        # Get format templates
        source_template = self.format_templates[source_format]
        target_template = self.format_templates[target_format]

        # Parse source prompt
        parsed_prompt = self._parse_prompt(prompt, source_template)

        # Apply style adaptation
        adapted_prompt = self._adapt_style(parsed_prompt, target_format)

        # Generate target prompt
        translated_prompt = self._generate_prompt(adapted_prompt, target_template)

        # Create result
        result = TranslationResult(
            original_prompt=prompt,
            translated_prompt=translated_prompt,
            source_format=source_format,
            target_format=target_format,
            metadata={"translation_params": params, "parsed_elements": parsed_prompt},
        )

        self.translation_history.append(result)
        return result

    def get_translation_stats(self) -> Dict[str, Any]:
        """Get statistics about translations.

        Returns:
            Dict[str, Any]: Translation statistics.
        """
        if not self.translation_history:
            return {}

        # Count format conversions
        format_conversions = defaultdict(int)
        for result in self.translation_history:
            key = f"{result.source_format.value}->{result.target_format.value}"
            format_conversions[key] += 1

        return {"total_translations": len(self.translation_history), "format_conversions": dict(format_conversions)}

    def export_templates(self, output_path: Path) -> None:
        """Export format templates to a file.

        Args:
            output_path (Path): Path to save templates.
        """
        templates_data = {"templates": {format.value: template for format, template in self.format_templates.items()}}

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(templates_data, f, indent=2)

    def _load_format_templates(self) -> Dict[ModelType, Dict[str, Any]]:
        """Load format templates.

        Returns:
            Dict[ModelType, Dict[str, Any]]: Format templates.
        """
        return {
            ModelType.OPENAI: {
                "system": "system",
                "user": "user",
                "assistant": "assistant",
                "format": {
                    "system": "System: {content}",
                    "user": "User: {content}",
                    "assistant": "Assistant: {content}",
                },
            },
            ModelType.ANTHROPIC: {
                "system": "system",
                "user": "human",
                "assistant": "assistant",
                "format": {
                    "system": "{content}",
                    "user": "\n\nHuman: {content}",
                    "assistant": "\n\nAssistant: {content}",
                },
            },
            ModelType.COHERE: {
                "system": "system",
                "user": "user",
                "assistant": "assistant",
                "format": {"system": "{content}", "user": "User: {content}", "assistant": "Assistant: {content}"},
            },
            ModelType.CUSTOM: {
                "system": "system",
                "user": "user",
                "assistant": "assistant",
                "format": {"system": "{content}", "user": "{content}", "assistant": "{content}"},
            },
        }

    def _parse_prompt(self, prompt: str, template: Dict[str, Any]) -> Dict[str, List[str]]:
        """Parse prompt into components.

        Args:
            prompt (str): Prompt to parse.
            template (Dict[str, Any]): Format template.

        Returns:
            Dict[str, List[str]]: Parsed prompt components.
        """
        components = {"system": [], "user": [], "assistant": []}

        # Split prompt into lines
        lines = prompt.split("\n")
        current_role = None
        current_content = []

        for line in lines:
            # Check for role markers
            if line.startswith("System:"):
                if current_role:
                    components[current_role].append("\n".join(current_content))
                current_role = "system"
                current_content = [line[7:].strip()]
            elif line.startswith("User:"):
                if current_role:
                    components[current_role].append("\n".join(current_content))
                current_role = "user"
                current_content = [line[5:].strip()]
            elif line.startswith("Assistant:"):
                if current_role:
                    components[current_role].append("\n".join(current_content))
                current_role = "assistant"
                current_content = [line[10:].strip()]
            else:
                if current_role:
                    current_content.append(line)

        # Add last component
        if current_role and current_content:
            components[current_role].append("\n".join(current_content))

        return components

    def _adapt_style(self, components: Dict[str, List[str]], target_format: ModelType) -> Dict[str, List[str]]:
        """Adapt prompt style.

        Args:
            components (Dict[str, List[str]]): Prompt components.
            target_format (ModelType): Target format.

        Returns:
            Dict[str, List[str]]: Adapted prompt components.
        """
        target_config = self.model_configs[target_format]
        style_patterns = self.style_patterns[target_config.preferred_style]

        adapted_components = {"system": [], "user": [], "assistant": []}

        for role, messages in components.items():
            for message in messages:
                adapted_message = message

                if style_patterns.get("remove_redundant", False):
                    # Remove redundant words and phrases
                    for pattern, replacement in style_patterns.get("replace_with", {}).items():
                        adapted_message = re.sub(pattern, replacement, adapted_message, flags=re.IGNORECASE)

                adapted_components[role].append(adapted_message)

        return adapted_components

    def _generate_prompt(self, components: Dict[str, List[str]], template: Dict[str, Any]) -> str:
        """Generate prompt from components.

        Args:
            components (Dict[str, List[str]]): Prompt components.
            template (Dict[str, Any]): Format template.

        Returns:
            str: Generated prompt.
        """
        parts = []

        # Add system message if present
        if components["system"]:
            system_content = " ".join(components["system"])
            parts.append(template["format"]["system"].format(content=system_content))

        # Add user and assistant messages
        for role in ["user", "assistant"]:
            for content in components[role]:
                parts.append(template["format"][role].format(content=content))

        # Add default assistant response if none exists
        if not components["assistant"]:
            parts.append(template["format"]["assistant"].format(content=""))

        return "\n".join(parts)
