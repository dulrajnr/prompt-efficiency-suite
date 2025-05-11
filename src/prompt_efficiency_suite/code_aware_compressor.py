"""Code Aware Compressor - A module for compressing prompts while preserving code blocks."""

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple, TypedDict

logger = logging.getLogger(__name__)


@dataclass
class CompressionResult:
    """Result of code-aware compression."""

    original_text: str
    compressed_text: str
    compression_ratio: float
    preserved_code_blocks: List[str]
    removed_tokens: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class CodePattern(TypedDict):
    """Configuration for a code pattern."""

    pattern: str
    description: str


class CodeAwareCompressor:
    """A class for compressing prompts while preserving code blocks."""

    def __init__(self):
        """Initialize the compressor."""
        self.logger = logging.getLogger(__name__)

    def compress(self, prompt: str) -> str:
        """Compress a prompt while preserving code blocks.

        Args:
            prompt: The prompt to compress

        Returns:
            The compressed prompt
        """
        # Split into sections
        sections = self._split_sections(prompt)

        # Process each section
        compressed_sections = []
        for section_type, content in sections:
            if section_type == "code":
                compressed_sections.append(content)
            else:
                compressed_sections.append(self._compress_text(content))

        return "".join(compressed_sections)

    def _split_sections(self, prompt: str) -> List[Tuple[str, str]]:
        """Split a prompt into code and non-code sections.

        Args:
            prompt: The prompt to split

        Returns:
            List of (section_type, content) tuples
        """
        sections = []
        current_pos = 0

        # Find code blocks
        for match in re.finditer(r"```.*?```", prompt, re.DOTALL):
            # Add text before code block
            if match.start() > current_pos:
                sections.append(("text", prompt[current_pos : match.start()]))

            # Add code block
            sections.append(("code", match.group(0)))
            current_pos = match.end()

        # Add remaining text
        if current_pos < len(prompt):
            sections.append(("text", prompt[current_pos:]))

        return sections

    def _compress_text(self, text: str) -> str:
        """Compress text while preserving meaning.

        Args:
            text: The text to compress

        Returns:
            The compressed text
        """
        # Remove redundant whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove redundant punctuation
        text = re.sub(r"[.,;:!?]{2,}", lambda m: m.group(0)[0], text)

        # Remove redundant words
        text = self._remove_redundant_words(text)

        return text.strip()

    def _remove_redundant_words(self, text: str) -> str:
        """Remove redundant words from text.

        Args:
            text: The text to process

        Returns:
            The text with redundant words removed
        """
        # TODO: Implement word redundancy detection
        return text

    def get_compression_stats(self) -> Dict[str, Any]:
        """Get statistics about compressions.

        Returns:
            Dict[str, Any]: Compression statistics.
        """
        if not self.compression_history:
            return {}

        total_compressions: int = len(self.compression_history)
        avg_ratio: float = (
            sum(r.compression_ratio for r in self.compression_history)
            / total_compressions
        )

        return {
            "total_compressions": total_compressions,
            "average_compression_ratio": avg_ratio,
            "preserved_code_blocks": sum(
                len(r.preserved_code_blocks) for r in self.compression_history
            ),
            "metadata": {"timestamp": self._get_timestamp()},
        }

    def _load_code_patterns(self) -> Dict[str, CodePattern]:
        """Load code pattern configurations.

        Returns:
            Dict[str, CodePattern]: Dictionary of code patterns.
        """
        return {
            "block": {
                "pattern": r"```[\s\S]*?```",
                "description": "Code block with language marker",
            },
            "inline": {"pattern": r"`[^`]+`", "description": "Inline code"},
            "indented": {
                "pattern": r"(?m)^( {4}|\t).*$",
                "description": "Indented code block",
            },
        }

    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code blocks from text.

        Args:
            text (str): Text to extract code blocks from.

        Returns:
            List[str]: List of extracted code blocks.
        """
        code_blocks: List[str] = []

        # Extract code blocks in order of appearance
        for pattern_info in self.code_patterns.values():
            pattern: Pattern[str] = re.compile(pattern_info["pattern"])
            matches = pattern.finditer(text)
            for match in matches:
                code_blocks.append(match.group())

        return code_blocks

    def _get_removed_tokens(self, original: str, compressed: str) -> List[str]:
        """Get list of removed tokens.

        Args:
            original (str): Original text.
            compressed (str): Compressed text.

        Returns:
            List[str]: List of removed tokens.
        """
        original_tokens: Set[str] = set(original.split())
        compressed_tokens: Set[str] = set(compressed.split())
        return list(original_tokens - compressed_tokens)

    def export_compression_history(self, output_path: Path) -> None:
        """Export compression history to a file.

        Args:
            output_path (Path): Path to save history.
        """
        history_data: Dict[str, Any] = {
            "statistics": self.get_compression_stats(),
            "compressions": [
                {
                    "original_length": len(result.original_text),
                    "compressed_length": len(result.compressed_text),
                    "compression_ratio": result.compression_ratio,
                    "code_blocks_count": len(result.preserved_code_blocks),
                    "removed_tokens": result.removed_tokens,
                    "metadata": result.metadata,
                }
                for result in self.compression_history
            ],
            "metadata": {"timestamp": self._get_timestamp()},
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2)

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            str: ISO format timestamp.
        """
        return datetime.now().isoformat()
