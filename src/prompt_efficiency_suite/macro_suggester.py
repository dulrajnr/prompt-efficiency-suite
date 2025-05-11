"""Macro Suggester - A module for suggesting macros for prompts."""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Pattern, Set, TypedDict, Union

from pydantic import BaseModel

from .macro_manager import MacroDefinition, MacroManager


@dataclass
class Suggestion:
    """A suggestion for a macro."""

    pattern: str
    replacement: str
    description: str
    example: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SuggestionResult:
    """Result of macro suggestions."""

    prompt: str
    suggestions: List[Suggestion]
    matched_patterns: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class PatternMatch(BaseModel):
    """Model for storing pattern match results."""

    pattern: str
    frequency: int
    examples: List[str]
    suggested_macro: Optional[MacroDefinition] = None


class MacroSuggester:
    """A class for suggesting macros for prompts."""

    def __init__(self, min_pattern_length: int = 3, min_frequency: int = 2) -> None:
        """Initialize the macro suggester."""
        self.min_pattern_length = min_pattern_length
        self.min_frequency = min_frequency
        self.pattern_matches: Dict[str, List[str]] = {}
        self.logger = logging.getLogger(__name__)

    def suggest(self, prompt: str) -> List[Dict[str, Any]]:
        """Suggest macros for a prompt.

        Args:
            prompt: The prompt to suggest macros for

        Returns:
            List of suggested macros
        """
        # Get patterns
        patterns = self._get_patterns()

        # Find matching patterns
        matches = []
        for pattern in patterns:
            if pattern["regex"].search(prompt):
                matches.append(pattern)

        return matches

    def _get_patterns(self) -> List[Dict[str, Any]]:
        """Get a list of patterns.

        Args:
            None

        Returns:
            List of patterns
        """
        # TODO: Implement pattern loading
        return []

    def analyze_prompts(self, prompts: List[str]) -> List[PatternMatch]:
        """Analyze a list of prompts to find common patterns.

        Args:
            prompts (List[str]): List of prompts to analyze.

        Returns:
            List[PatternMatch]: List of pattern matches found.
        """
        # Reset pattern matches
        self.pattern_matches.clear()

        # Find common patterns
        for prompt in prompts:
            self._find_patterns(prompt)

        # Filter and sort patterns
        valid_patterns = [
            match
            for match in self.pattern_matches.values()
            if len(match.pattern) >= self.min_pattern_length
            and match.frequency >= self.min_frequency
        ]

        return sorted(valid_patterns, key=lambda x: x.frequency, reverse=True)

    def _find_patterns(self, prompt: str) -> None:
        """Find patterns in a single prompt.

        Args:
            prompt (str): The prompt to analyze.
        """
        # Split into sentences or logical chunks
        chunks = self._split_into_chunks(prompt)

        # Find repeated patterns
        for i, chunk in enumerate(chunks):
            if len(chunk) < self.min_pattern_length:
                continue

            # Look for this chunk in other positions
            for j, other_chunk in enumerate(chunks):
                if i != j and self._is_similar(chunk, other_chunk):
                    pattern = self._normalize_pattern(chunk)
                    if pattern not in self.pattern_matches:
                        self.pattern_matches[pattern] = PatternMatch(
                            pattern=pattern, frequency=1, examples=[chunk]
                        )
                    else:
                        match = self.pattern_matches[pattern]
                        match.frequency += 1
                        if chunk not in match.examples:
                            match.examples.append(chunk)

    def _split_into_chunks(self, text: str) -> List[str]:
        """Split text into logical chunks.

        Args:
            text (str): The text to split.

        Returns:
            List[str]: List of text chunks.
        """
        # Split by sentences, bullet points, or other logical boundaries
        chunks: List[str] = re.split(r"[.!?]|\n|\*", text)
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def _is_similar(self, chunk1: str, chunk2: str) -> bool:
        """Check if two chunks are similar enough to be considered the same pattern.

        Args:
            chunk1 (str): First text chunk.
            chunk2 (str): Second text chunk.

        Returns:
            bool: True if chunks are similar, False otherwise.
        """
        # Simple similarity check - can be improved with more sophisticated methods
        chunk1_words: Set[str] = set(chunk1.lower().split())
        chunk2_words: Set[str] = set(chunk2.lower().split())

        # Calculate Jaccard similarity
        intersection: int = len(chunk1_words & chunk2_words)
        union: int = len(chunk1_words | chunk2_words)

        return intersection / union > 0.7 if union > 0 else False

    def _normalize_pattern(self, pattern: str) -> str:
        """Normalize a pattern for comparison.

        Args:
            pattern (str): The pattern to normalize.

        Returns:
            str: Normalized pattern.
        """
        # Convert to lowercase and remove extra whitespace
        normalized: str = " ".join(pattern.lower().split())

        # Replace specific values with placeholders
        normalized = re.sub(r"\d+", "{number}", normalized)
        normalized = re.sub(r'"[^"]*"', "{string}", normalized)

        return normalized

    def suggest_macros(self, patterns: List[PatternMatch]) -> List[MacroDefinition]:
        """Suggest macros based on found patterns.

        Args:
            patterns (List[PatternMatch]): List of pattern matches to analyze.

        Returns:
            List[MacroDefinition]: List of suggested macro definitions.
        """
        suggested_macros: List[MacroDefinition] = []

        for pattern in patterns:
            if pattern.frequency >= self.min_frequency:
                # Create a macro definition
                macro = MacroDefinition(
                    name=f"macro_{len(suggested_macros) + 1}",
                    template=pattern.pattern,
                    description=f"Macro for common pattern: {pattern.pattern[:50]}...",
                    parameters=self._extract_parameters(pattern.pattern),
                )

                pattern.suggested_macro = macro
                suggested_macros.append(macro)

        return suggested_macros

    def _extract_parameters(self, pattern: str) -> List[str]:
        """Extract parameters from a pattern.

        Args:
            pattern (str): The pattern to extract parameters from.

        Returns:
            List[str]: List of parameter names.
        """
        # Find all placeholders in the pattern
        params: List[str] = []
        for match in re.finditer(r"{(\w+)}", pattern):
            param = match.group(1)
            if param not in params:
                params.append(param)
        return params

    def get_suggestion_stats(self) -> Dict[str, Any]:
        """Get statistics about suggestions.

        Returns:
            Dict[str, Any]: Suggestion statistics.
        """
        if not self.pattern_matches:
            return {}

        total_patterns = len(self.pattern_matches)
        total_frequency = sum(
            match.frequency for match in self.pattern_matches.values()
        )
        avg_frequency = total_frequency / total_patterns if total_patterns > 0 else 0

        return {
            "total_patterns": total_patterns,
            "total_frequency": total_frequency,
            "avg_frequency": avg_frequency,
            "pattern_lengths": {
                match.pattern: len(match.pattern)
                for match in self.pattern_matches.values()
            },
            "metadata": {"timestamp": self._get_timestamp()},
        }

    def _load_macro_patterns(self) -> None:
        """Load macro patterns from configuration."""
        pattern_strings: Dict[str, List[str]] = {
            "code_blocks": [
                r"```[\s\S]*?```",
                r"`[^`]+`",
            ],
            "examples": [
                r"Example:[\s\S]*?(?=\n\n|\Z)",
                r"For example:[\s\S]*?(?=\n\n|\Z)",
            ],
            "instructions": [
                r"Please[\s\S]*?(?=\n\n|\Z)",
                r"Instructions:[\s\S]*?(?=\n\n|\Z)",
            ],
        }

        self.patterns = {
            category: [re.compile(pattern) for pattern in patterns]
            for category, patterns in pattern_strings.items()
        }

    def export_patterns(self, output_path: Path) -> None:
        """Export pattern matches to a file.

        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            "statistics": self.get_suggestion_stats(),
            "patterns": [
                {
                    "pattern": match.pattern,
                    "frequency": match.frequency,
                    "examples": match.examples,
                    "suggested_macro": (
                        match.suggested_macro.dict() if match.suggested_macro else None
                    ),
                }
                for match in self.pattern_matches.values()
            ],
            "metadata": {"timestamp": self._get_timestamp()},
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2)

    def _find_matching_patterns(self, prompt: str) -> List[Dict[str, Any]]:
        """Find patterns that match the prompt.

        Args:
            prompt (str): The prompt to analyze.

        Returns:
            List[Dict[str, Any]]: List of matching patterns.
        """
        matches: List[Dict[str, Any]] = []

        for category, patterns in self.patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(prompt):
                    matches.append(
                        {
                            "category": category,
                            "pattern": pattern.pattern,
                            "match": match.group(0),
                            "start": match.start(),
                            "end": match.end(),
                        }
                    )

        return matches

    def _generate_macro_suggestions(
        self,
        prompt: str,
        matched_patterns: List[Dict[str, Any]],
        params: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Generate macro suggestions based on matched patterns.

        Args:
            prompt (str): The prompt to analyze.
            matched_patterns (List[Dict[str, Any]]): List of matched patterns.
            params (Dict[str, Any]): Additional parameters.

        Returns:
            List[Dict[str, Any]]: List of macro suggestions.
        """
        suggestions: List[Dict[str, Any]] = []

        for match in matched_patterns:
            if match["category"] in params.get("enabled_categories", []):
                suggestion = {
                    "pattern": match["pattern"],
                    "replacement": f"{{macro_{match['category']}}}",
                    "description": f"Replace {match['category']} pattern with macro",
                    "example": match["match"],
                    "confidence": 0.8,  # TODO: Implement confidence calculation
                    "metadata": {
                        "category": match["category"],
                        "position": {"start": match["start"], "end": match["end"]},
                    },
                }
                suggestions.append(suggestion)

        return suggestions

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            str: ISO format timestamp.
        """
        return datetime.now().isoformat()

    def analyze_prompt(self, prompt: str) -> List[MacroDefinition]:
        """Analyze a prompt and suggest macros."""
        patterns = self._find_patterns(prompt)
        return self._generate_macro_definitions(patterns)

    def _find_patterns(self, prompt: str) -> Dict[str, int]:
        """Find repeated patterns in the prompt."""
        patterns: Dict[str, int] = {}
        words = prompt.split()

        for i in range(len(words) - self.min_pattern_length + 1):
            pattern = " ".join(words[i : i + self.min_pattern_length])
            patterns[pattern] = patterns.get(pattern, 0) + 1

        return {p: f for p, f in patterns.items() if f >= self.min_frequency}

    def _generate_macro_definitions(
        self, patterns: Dict[str, int]
    ) -> List[MacroDefinition]:
        """Generate macro definitions from patterns."""
        macros: List[MacroDefinition] = []

        for pattern, frequency in patterns.items():
            if frequency >= self.min_frequency:
                macro = MacroDefinition(
                    name=f"MACRO_{len(macros) + 1}",
                    pattern=pattern,
                    parameters=[],
                    description=f"Replaces '{pattern}'",
                )
                macros.append(macro)

        return macros

    def get_pattern_matches(self) -> Dict[str, List[str]]:
        """Get all pattern matches found during analysis."""
        return self.pattern_matches
