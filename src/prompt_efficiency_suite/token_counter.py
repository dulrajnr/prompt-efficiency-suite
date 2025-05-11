"""Token Counter - A module for counting tokens in prompts."""

import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TokenCount:
    """Result of token counting."""

    text: str
    total_tokens: int
    token_distribution: Dict[str, int]
    metadata: Dict[str, Any] = field(default_factory=dict)


class TokenCounter:
    """A class for counting tokens in prompts."""

    def __init__(self):
        """Initialize the token counter."""
        self.logger = logging.getLogger(__name__)

    def count(self, prompt: str) -> int:
        """Count tokens in a prompt.

        Args:
            prompt: The prompt to count tokens in

        Returns:
            Number of tokens
        """
        # TODO: Implement token counting
        return len(prompt.split())

    def count_with_model(self, prompt: str, model: str = "gpt-4") -> Dict[str, Any]:
        """Count tokens in a prompt using a specific model.

        Args:
            prompt: The prompt to count tokens in
            model: The model to use for token counting

        Returns:
            Dictionary containing token count and model info
        """
        # TODO: Implement model-specific token counting
        return {
            "token_count": self.count(prompt),
            "model": model,
            "encoding": "cl100k_base",
            "max_tokens": 8192,
        }

    def count_tokens(self, text: str) -> int:
        """Count tokens in text.

        Args:
            text (str): Text to count tokens in.

        Returns:
            int: Number of tokens.
        """
        # Simple whitespace-based tokenization
        tokens = text.split()
        token_count = len(tokens)

        # Calculate token distribution
        distribution: Dict[str, int] = defaultdict(int)
        for token in tokens:
            distribution[token] += 1

        result = TokenCount(
            text=text,
            total_tokens=token_count,
            token_distribution=dict(distribution),
            metadata={
                "tokenization_method": "whitespace",
                "timestamp": self._get_timestamp(),
            },
        )

        self.count_history.append(result)
        return token_count

    def get_count_stats(self) -> Dict[str, Any]:
        """Get statistics about token counts.

        Returns:
            Dict[str, Any]: Token count statistics.
        """
        if not self.count_history:
            return {}

        total_counts = len(self.count_history)
        avg_tokens = sum(r.total_tokens for r in self.count_history) / total_counts

        # Calculate token frequency distribution
        token_freq: Dict[str, int] = defaultdict(int)
        for result in self.count_history:
            for token, count in result.token_distribution.items():
                token_freq[token] += count

        return {
            "total_counts": total_counts,
            "average_tokens": avg_tokens,
            "unique_tokens": len(token_freq),
            "most_common_tokens": sorted(
                token_freq.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }

    def export_count_history(self, output_path: Path) -> None:
        """Export count history to a file.

        Args:
            output_path (Path): Path to save history.
        """
        history_data = {
            "statistics": self.get_count_stats(),
            "counts": [
                {
                    "text_length": len(result.text),
                    "total_tokens": result.total_tokens,
                    "token_distribution": result.token_distribution,
                    "metadata": result.metadata,
                }
                for result in self.count_history
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2)

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            str: ISO format timestamp.
        """
        return datetime.now().isoformat()
