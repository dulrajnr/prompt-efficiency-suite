"""
Prompt Analyzer module for analyzing prompts and their components.
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import spacy
from pydantic import BaseModel


@dataclass
class AnalysisMetrics:
    """Metrics for prompt analysis."""

    clarity_score: float
    completeness_score: float
    consistency_score: float
    efficiency_score: float
    complexity_score: float
    metadata: Dict[str, Any]


@dataclass
class AnalysisResult:
    """Result of prompt analysis."""

    prompt: str
    metrics: AnalysisMetrics
    suggestions: List[str]
    metadata: Dict[str, Any]


class PromptAnalysis(BaseModel):
    """Model for storing prompt analysis results."""

    token_count: int
    word_count: int
    sentence_count: int
    readability_score: float
    complexity_score: float
    redundancy_score: float
    key_phrases: List[str]
    metadata: Dict[str, Union[str, int, float]]


class PromptAnalyzer:
    """Analyzes prompts for efficiency and quality metrics."""

    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the analyzer with a specific spaCy model."""
        self.nlp = spacy.load(model_name)

    def analyze(self, text: str) -> PromptAnalysis:
        """Analyze a single prompt.

        Args:
            text: The prompt text to analyze

        Returns:
            PromptAnalysis containing various metrics and insights
        """
        doc = self.nlp(text)

        # Basic metrics
        token_count = len(doc)
        word_count = len([token for token in doc if not token.is_punct])
        sentence_count = len(list(doc.sents))

        # Calculate readability score (simplified Flesch-Kincaid)
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            readability_score = 206.835 - (1.015 * avg_sentence_length)
        else:
            readability_score = 0.0

        # Calculate complexity score
        complex_words = len([token for token in doc if len(token.text) > 6])
        complexity_score = complex_words / word_count if word_count > 0 else 0.0

        # Calculate redundancy score (simplified)
        unique_words = len(set(token.text.lower() for token in doc if not token.is_punct))
        redundancy_score = 1 - (unique_words / word_count) if word_count > 0 else 0.0

        # Extract key phrases (noun chunks)
        key_phrases = [chunk.text for chunk in doc.noun_chunks]

        return PromptAnalysis(
            token_count=token_count,
            word_count=word_count,
            sentence_count=sentence_count,
            readability_score=readability_score,
            complexity_score=complexity_score,
            redundancy_score=redundancy_score,
            key_phrases=key_phrases,
            metadata={
                "avg_word_length": sum(len(token.text) for token in doc) / token_count if token_count > 0 else 0,
                "unique_word_ratio": unique_words / word_count if word_count > 0 else 0,
            },
        )

    def batch_analyze(self, texts: List[str]) -> List[PromptAnalysis]:
        """Analyze multiple prompts in batch.

        Args:
            texts: List of prompt texts to analyze

        Returns:
            List of PromptAnalysis objects
        """
        return [self.analyze(text) for text in texts]

    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get statistics about analysis results.

        Returns:
            Dict[str, Any]: Analysis statistics.
        """
        if not self.analysis_history:
            return {}

        total_analyses = len(self.analysis_history)

        # Calculate average scores
        avg_scores = {
            "clarity": sum(r.metrics.clarity_score for r in self.analysis_history) / total_analyses,
            "completeness": sum(r.metrics.completeness_score for r in self.analysis_history) / total_analyses,
            "consistency": sum(r.metrics.consistency_score for r in self.analysis_history) / total_analyses,
            "efficiency": sum(r.metrics.efficiency_score for r in self.analysis_history) / total_analyses,
            "complexity": sum(r.metrics.complexity_score for r in self.analysis_history) / total_analyses,
        }

        return {
            "total_analyses": total_analyses,
            "average_scores": avg_scores,
            "suggestion_frequency": self._calculate_suggestion_frequency(),
        }

    def export_results(self, output_path: Path) -> None:
        """Export analysis results to a file.

        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            "statistics": self.get_analysis_stats(),
            "results": [
                {
                    "prompt": result.prompt,
                    "metrics": {
                        "clarity_score": result.metrics.clarity_score,
                        "completeness_score": result.metrics.completeness_score,
                        "consistency_score": result.metrics.consistency_score,
                        "efficiency_score": result.metrics.efficiency_score,
                        "complexity_score": result.metrics.complexity_score,
                        "metadata": result.metrics.metadata,
                    },
                    "suggestions": result.suggestions,
                    "metadata": result.metadata,
                }
                for result in self.analysis_history
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2)

    def _load_analysis_patterns(self) -> Dict[str, re.Pattern]:
        """Load analysis patterns."""
        return {
            "ambiguity": re.compile(r"\b(may|might|could|possibly|maybe)\b"),
            "redundancy": re.compile(r"\b(\w+)(\s+\1)+\b"),
            "complexity": re.compile(r"[^.!?]+[.!?]"),
            "formatting": re.compile(r"[*_`].*?[*_`]"),
            "instructions": re.compile(r"\b(please|kindly|should|must|need to)\b"),
            "examples": re.compile(r"\b(example|instance|case|sample)\b"),
            "context": re.compile(r"\b(context|background|scenario|situation)\b"),
        }

    def _calculate_metrics(self, prompt: str, params: Dict[str, Any]) -> AnalysisMetrics:
        """Calculate analysis metrics.

        Args:
            prompt (str): Prompt to analyze.
            params (Dict[str, Any]): Analysis parameters.

        Returns:
            AnalysisMetrics: Analysis metrics.
        """
        # Calculate base scores
        clarity_score = self._calculate_clarity_score(prompt)
        completeness_score = self._calculate_completeness_score(prompt)
        consistency_score = self._calculate_consistency_score(prompt)
        efficiency_score = self._calculate_efficiency_score(prompt)
        complexity_score = self._calculate_complexity_score(prompt)

        return AnalysisMetrics(
            clarity_score=clarity_score,
            completeness_score=completeness_score,
            consistency_score=consistency_score,
            efficiency_score=efficiency_score,
            complexity_score=complexity_score,
            metadata={"analysis_params": params, "prompt_length": len(prompt), "word_count": len(prompt.split())},
        )

    def _calculate_clarity_score(self, prompt: str) -> float:
        """Calculate clarity score.

        Args:
            prompt (str): Prompt to analyze.

        Returns:
            float: Clarity score between 0 and 1.
        """
        # Count ambiguous terms
        ambiguous_terms = len(self.analysis_patterns["ambiguity"].findall(prompt))

        # Count redundant phrases
        redundant_phrases = len(self.analysis_patterns["redundancy"].findall(prompt))

        # Calculate base score
        base_score = 1.0
        if len(prompt.split()) > 0:
            base_score -= (ambiguous_terms + redundant_phrases) / len(prompt.split())

        return max(0.0, min(1.0, base_score))

    def _calculate_completeness_score(self, prompt: str) -> float:
        """Calculate completeness score.

        Args:
            prompt (str): Prompt to analyze.

        Returns:
            float: Completeness score between 0 and 1.
        """
        # Count key components
        has_instructions = bool(self.analysis_patterns["instructions"].search(prompt))
        has_examples = bool(self.analysis_patterns["examples"].search(prompt))
        has_context = bool(self.analysis_patterns["context"].search(prompt))

        # Calculate score based on presence of components
        score = 0.0
        if has_instructions:
            score += 0.4
        if has_examples:
            score += 0.3
        if has_context:
            score += 0.3

        return score

    def _calculate_consistency_score(self, prompt: str) -> float:
        """Calculate consistency score.

        Args:
            prompt (str): Prompt to analyze.

        Returns:
            float: Consistency score between 0 and 1.
        """
        # This is a placeholder implementation
        # In a real implementation, this would check for:
        # - Consistent terminology
        # - Consistent formatting
        # - Consistent tone
        return 0.9

    def _calculate_efficiency_score(self, prompt: str) -> float:
        """Calculate efficiency score.

        Args:
            prompt (str): Prompt to analyze.

        Returns:
            float: Efficiency score between 0 and 1.
        """
        # Count formatting markers
        formatting_markers = len(self.analysis_patterns["formatting"].findall(prompt))

        # Calculate words per sentence
        sentences = self.analysis_patterns["complexity"].findall(prompt)
        if not sentences:
            return 0.0

        avg_words_per_sentence = sum(len(s.split()) for s in sentences) / len(sentences)

        # Penalize very long sentences and excessive formatting
        base_score = 1.0
        if avg_words_per_sentence > 20:  # Arbitrary threshold
            base_score -= (avg_words_per_sentence - 20) / 100

        base_score -= formatting_markers / 50  # Arbitrary scaling

        return max(0.0, min(1.0, base_score))

    def _calculate_complexity_score(self, prompt: str) -> float:
        """Calculate complexity score.

        Args:
            prompt (str): Prompt to analyze.

        Returns:
            float: Complexity score between 0 and 1.
        """
        # Count sentences
        sentences = self.analysis_patterns["complexity"].findall(prompt)
        if not sentences:
            return 0.0

        # Calculate average sentence length
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)

        # Calculate score (higher score means more complex)
        score = min(1.0, avg_sentence_length / 30)  # Arbitrary threshold

        return score

    def _generate_suggestions(self, prompt: str, metrics: AnalysisMetrics) -> List[str]:
        """Generate suggestions for improving the prompt.

        Args:
            prompt (str): Prompt to analyze.
            metrics (AnalysisMetrics): Analysis metrics.

        Returns:
            List[str]: List of suggestions.
        """
        suggestions = []

        # Check clarity
        if metrics.clarity_score < 0.7:
            suggestions.append("Consider removing ambiguous terms and redundant phrases")

        # Check completeness
        if metrics.completeness_score < 0.7:
            suggestions.append("Add more context, examples, or specific instructions")

        # Check efficiency
        if metrics.efficiency_score < 0.7:
            suggestions.append("Consider simplifying sentence structure and reducing formatting")

        # Check complexity
        if metrics.complexity_score > 0.8:
            suggestions.append("Consider breaking down complex sentences into simpler ones")

        return suggestions

    def _calculate_suggestion_frequency(self) -> Dict[str, int]:
        """Calculate frequency of suggestions across all analyses.

        Returns:
            Dict[str, int]: Suggestion frequency.
        """
        frequency = defaultdict(int)

        for result in self.analysis_history:
            for suggestion in result.suggestions:
                frequency[suggestion] += 1

        return dict(frequency)

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()
