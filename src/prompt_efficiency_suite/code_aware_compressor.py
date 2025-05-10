"""
Code-Aware Compressor module for compressing prompts while preserving code structure.
"""

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

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


class CodeAwareCompressor:
    """A class for compressing text while preserving code structure."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the CodeAwareCompressor.

        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.code_patterns = self._load_code_patterns()
        self.compression_history: List[CompressionResult] = []

    def compress(self, text: str, compression_params: Optional[Dict[str, Any]] = None) -> CompressionResult:
        """Compress text while preserving code structure.

        Args:
            text (str): Text to compress.
            compression_params (Optional[Dict[str, Any]]): Additional compression parameters.

        Returns:
            CompressionResult: Result of compression.
        """
        params = compression_params or {}

        # Extract code blocks
        code_blocks = self._extract_code_blocks(text)

        # Replace code blocks with placeholders
        text_with_placeholders = text
        for i, block in enumerate(code_blocks):
            placeholder = f"CODE_BLOCK_{i}"
            text_with_placeholders = text_with_placeholders.replace(block, placeholder)

        # Compress non-code text
        compressed_text = self._compress_text(text_with_placeholders)

        # Restore code blocks
        for i, block in enumerate(code_blocks):
            placeholder = f"CODE_BLOCK_{i}"
            compressed_text = compressed_text.replace(placeholder, block)

        # Calculate metrics
        compression_ratio = len(compressed_text) / len(text)
        removed_tokens = self._get_removed_tokens(text, compressed_text)

        result = CompressionResult(
            original_text=text,
            compressed_text=compressed_text,
            compression_ratio=compression_ratio,
            preserved_code_blocks=code_blocks,
            removed_tokens=removed_tokens,
            metadata={"compression_params": params, "code_blocks_count": len(code_blocks)},
        )

        self.compression_history.append(result)
        return result

    def get_compression_stats(self) -> Dict[str, Any]:
        """Get statistics about compressions.

        Returns:
            Dict[str, Any]: Compression statistics.
        """
        if not self.compression_history:
            return {}

        total_compressions = len(self.compression_history)
        avg_ratio = sum(r.compression_ratio for r in self.compression_history) / total_compressions

        return {
            "total_compressions": total_compressions,
            "average_compression_ratio": avg_ratio,
            "preserved_code_blocks": sum(len(r.preserved_code_blocks) for r in self.compression_history),
        }

    def _load_code_patterns(self) -> Dict[str, Any]:
        """Load code pattern configurations."""
        return {
            "block": {"pattern": r"```[\s\S]*?```", "description": "Code block with language marker"},
            "inline": {"pattern": r"`[^`]+`", "description": "Inline code"},
            "indented": {"pattern": r"(?m)^( {4}|\t).*$", "description": "Indented code block"},
        }

    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code blocks from text."""
        code_blocks = []

        # Extract code blocks in order of appearance
        for pattern_info in self.code_patterns.values():
            matches = re.finditer(pattern_info["pattern"], text)
            for match in matches:
                code_blocks.append(match.group())

        return code_blocks

    def _compress_text(self, text: str) -> str:
        """Compress non-code text."""
        # Remove redundant whitespace
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        # Remove common filler words
        filler_words = [r"\bvery\b", r"\breally\b", r"\bquite\b", r"\bjust\b", r"\bsimply\b", r"\bbasically\b"]
        for word in filler_words:
            text = re.sub(word, "", text, flags=re.IGNORECASE)

        # Remove redundant punctuation
        text = re.sub(r"([.!?])\1+", r"\1", text)

        # Clean up whitespace again
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        return text

    def _get_removed_tokens(self, original: str, compressed: str) -> List[str]:
        """Get list of removed tokens."""
        original_tokens = set(original.split())
        compressed_tokens = set(compressed.split())
        return list(original_tokens - compressed_tokens)

    def export_compression_history(self, output_path: Path) -> None:
        """Export compression history to a file.

        Args:
            output_path (Path): Path to save history.
        """
        history_data = {
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
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2)
