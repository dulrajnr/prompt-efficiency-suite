"""
Macro Suggester - A module for suggesting macros for common prompt patterns.
"""

from typing import Dict, Any, Optional, List, Set, Union
from dataclasses import dataclass, field
import re
import json
from pathlib import Path
import logging
from collections import defaultdict
from .macro_manager import MacroManager, MacroDefinition
from pydantic import BaseModel

logger = logging.getLogger(__name__)

@dataclass
class Suggestion:
    """A suggestion for a macro."""
    pattern: str
    replacement: str
    description: str
    example: str
    confidence: float
    metadata: Dict[str, any] = field(default_factory=dict)

@dataclass
class SuggestionResult:
    """Result of macro suggestions."""
    prompt: str
    suggestions: List[Suggestion]
    matched_patterns: List[str]
    metadata: Dict[str, any] = field(default_factory=dict)

class PatternMatch(BaseModel):
    """Model for storing pattern match results."""
    pattern: str
    frequency: int
    examples: List[str]
    suggested_macro: Optional[MacroDefinition] = None

class MacroSuggester:
    """Suggests macros based on prompt patterns."""
    
    def __init__(self, macro_manager: MacroManager):
        """Initialize the macro suggester.
        
        Args:
            macro_manager: The macro manager to use
        """
        self.macro_manager = macro_manager
        self.pattern_matches: Dict[str, PatternMatch] = {}
        self.min_pattern_length = 10
        self.min_frequency = 2
    
    def analyze_prompts(self, prompts: List[str]) -> List[PatternMatch]:
        """Analyze a list of prompts to find common patterns.
        
        Args:
            prompts: List of prompts to analyze
            
        Returns:
            List of pattern matches found
        """
        # Reset pattern matches
        self.pattern_matches.clear()
        
        # Find common patterns
        for prompt in prompts:
            self._find_patterns(prompt)
        
        # Filter and sort patterns
        valid_patterns = [
            match for match in self.pattern_matches.values()
            if len(match.pattern) >= self.min_pattern_length
            and match.frequency >= self.min_frequency
        ]
        
        return sorted(valid_patterns, key=lambda x: x.frequency, reverse=True)
    
    def _find_patterns(self, prompt: str) -> None:
        """Find patterns in a single prompt.
        
        Args:
            prompt: The prompt to analyze
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
                            pattern=pattern,
                            frequency=1,
                            examples=[chunk]
                        )
                    else:
                        match = self.pattern_matches[pattern]
                        match.frequency += 1
                        if chunk not in match.examples:
                            match.examples.append(chunk)
    
    def _split_into_chunks(self, text: str) -> List[str]:
        """Split text into logical chunks.
        
        Args:
            text: The text to split
            
        Returns:
            List of text chunks
        """
        # Split by sentences, bullet points, or other logical boundaries
        chunks = re.split(r'[.!?]|\n|\*', text)
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def _is_similar(self, chunk1: str, chunk2: str) -> bool:
        """Check if two chunks are similar enough to be considered the same pattern.
        
        Args:
            chunk1: First text chunk
            chunk2: Second text chunk
            
        Returns:
            True if chunks are similar, False otherwise
        """
        # Simple similarity check - can be improved with more sophisticated methods
        chunk1_words = set(chunk1.lower().split())
        chunk2_words = set(chunk2.lower().split())
        
        # Calculate Jaccard similarity
        intersection = len(chunk1_words & chunk2_words)
        union = len(chunk1_words | chunk2_words)
        
        return intersection / union > 0.7 if union > 0 else False
    
    def _normalize_pattern(self, pattern: str) -> str:
        """Normalize a pattern for comparison.
        
        Args:
            pattern: The pattern to normalize
            
        Returns:
            Normalized pattern
        """
        # Convert to lowercase and remove extra whitespace
        normalized = ' '.join(pattern.lower().split())
        
        # Replace specific values with placeholders
        normalized = re.sub(r'\d+', '{number}', normalized)
        normalized = re.sub(r'"[^"]*"', '{string}', normalized)
        
        return normalized
    
    def suggest_macros(self, patterns: List[PatternMatch]) -> List[MacroDefinition]:
        """Suggest macros based on found patterns.
        
        Args:
            patterns: List of pattern matches to analyze
            
        Returns:
            List of suggested macro definitions
        """
        suggested_macros = []
        
        for pattern in patterns:
            if pattern.frequency >= self.min_frequency:
                # Create a macro definition
                macro = MacroDefinition(
                    name=f"macro_{len(suggested_macros) + 1}",
                    template=pattern.pattern,
                    description=f"Macro for common pattern: {pattern.pattern[:50]}...",
                    parameters=self._extract_parameters(pattern.pattern)
                )
                
                pattern.suggested_macro = macro
                suggested_macros.append(macro)
        
        return suggested_macros
    
    def _extract_parameters(self, pattern: str) -> List[str]:
        """Extract parameters from a pattern.
        
        Args:
            pattern: The pattern to extract parameters from
            
        Returns:
            List of parameter names
        """
        # Find all placeholders in the pattern
        placeholders = re.findall(r'\{([^}]+)\}', pattern)
        return list(set(placeholders))

    def get_suggestion_stats(self) -> Dict[str, any]:
        """Get statistics about suggestions.
        
        Returns:
            Dict[str, any]: Suggestion statistics.
        """
        if not self.pattern_matches:
            return {}

        pattern_counts = {}
        for match in self.pattern_matches.values():
            pattern_counts[match.pattern] = match.frequency

        return {
            "total_suggestions": len(self.pattern_matches),
            "avg_suggestions_per_prompt": sum(match.frequency for match in self.pattern_matches.values()) / len(self.pattern_matches),
            "pattern_frequency": pattern_counts
        }

    def _load_macro_patterns(self) -> None:
        """Load macro patterns."""
        self.patterns = {
            "function_definition": {
                "pattern": r"def\s+\w+\s*\([^)]*\)\s*:",
                "replacement": "${function_name}(${params})",
                "description": "Function definition pattern",
                "example": "def process_data(data: List[str]) -> Dict[str, int]:",
                "confidence": 0.9
            },
            "class_definition": {
                "pattern": r"class\s+\w+(\s*\([^)]*\))?:",
                "replacement": "${class_name}",
                "description": "Class definition pattern",
                "example": "class DataProcessor:",
                "confidence": 0.9
            },
            "import_statement": {
                "pattern": r"(from\s+[\w.]+\s+)?import\s+[\w.]+(\s+as\s+\w+)?",
                "replacement": "${import_statement}",
                "description": "Import statement pattern",
                "example": "from typing import List, Dict",
                "confidence": 0.9
            },
            "docstring": {
                "pattern": r'"""[^"]*"""',
                "replacement": "${docstring}",
                "description": "Docstring pattern",
                "example": '"""Process the input data."""',
                "confidence": 0.8
            },
            "type_hint": {
                "pattern": r":\s*[\w\[\],\s]+",
                "replacement": "${type_hint}",
                "description": "Type hint pattern",
                "example": ": List[str]",
                "confidence": 0.8
            },
            "error_handling": {
                "pattern": r"try:.*?except\s+\w+(\s+as\s+\w+)?:",
                "replacement": "${error_handling}",
                "description": "Error handling pattern",
                "example": "try: ... except ValueError as e:",
                "confidence": 0.8
            },
            "logging_statement": {
                "pattern": r"logger\.\w+\([^)]+\)",
                "replacement": "${logging_statement}",
                "description": "Logging statement pattern",
                "example": 'logger.info("Processing data")',
                "confidence": 0.8
            },
            "configuration_dict": {
                "pattern": r"\{[^}]+\}",
                "replacement": "${config}",
                "description": "Configuration dictionary pattern",
                "example": '{"model": "gpt-4", "max_tokens": 100}',
                "confidence": 0.7
            }
        }

    def export_patterns(self, output_path: Path) -> None:
        """Export macro patterns to a file.
        
        Args:
            output_path (Path): Path to save patterns.
        """
        patterns_data = {
            'patterns': [
                {
                    'name': pattern.name,
                    'pattern': pattern.pattern,
                    'description': pattern.description,
                    'example': pattern.example,
                    'metadata': pattern.metadata
                }
                for pattern in self.patterns.values()
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(patterns_data, f, indent=2)
            
    def _find_matching_patterns(self, prompt: str) -> List[Dict[str, Any]]:
        """Find patterns that match the prompt.
        
        Args:
            prompt (str): Prompt to analyze.
            
        Returns:
            List[Dict[str, Any]]: List of matched patterns.
        """
        matches = []
        
        for pattern in self.patterns.values():
            if re.search(pattern['pattern'], prompt, re.MULTILINE | re.DOTALL):
                matches.append({
                    'name': pattern['name'],
                    'pattern': pattern['pattern'],
                    'description': pattern['description'],
                    'example': pattern['example'],
                    'metadata': pattern['metadata']
                })
                
        return matches
        
    def _generate_macro_suggestions(
        self,
        prompt: str,
        matched_patterns: List[Dict[str, Any]],
        params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate macro suggestions based on matched patterns.
        
        Args:
            prompt (str): Original prompt.
            matched_patterns (List[Dict[str, Any]]): Matched patterns.
            params (Dict[str, Any]]): Suggestion parameters.
            
        Returns:
            List[Dict[str, Any]]: List of suggested macros.
        """
        suggestions = []
        used_patterns: Set[str] = set()
        
        # Sort patterns by frequency in the prompt
        pattern_frequency = defaultdict(int)
        for pattern in matched_patterns:
            matches = re.findall(pattern['pattern'], prompt, re.MULTILINE | re.DOTALL)
            pattern_frequency[pattern['name']] = len(matches)
            
        # Sort patterns by frequency
        sorted_patterns = sorted(
            matched_patterns,
            key=lambda p: pattern_frequency[p['name']],
            reverse=True
        )
        
        # Generate suggestions
        for pattern in sorted_patterns:
            if pattern['name'] in used_patterns:
                continue
                
            # Check if pattern is frequent enough
            if pattern_frequency[pattern['name']] >= params.get('min_frequency', 2):
                suggestions.append(pattern)
                used_patterns.add(pattern['name'])
                
        return suggestions 