"""
Quality Analyzer module for analyzing prompt quality.
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
import re
import json
from pathlib import Path
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """Quality metrics for a prompt."""
    clarity_score: float
    completeness_score: float
    consistency_score: float
    relevance_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class QualityAnalyzer:
    """A class for analyzing prompt quality."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the QualityAnalyzer.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.analysis_history: List[QualityMetrics] = []
        
    def analyze(self, prompt: str) -> float:
        """Analyze prompt quality.
        
        Args:
            prompt (str): Prompt to analyze.
            
        Returns:
            float: Overall quality score.
        """
        # Calculate individual metrics
        clarity = self._calculate_clarity(prompt)
        completeness = self._calculate_completeness(prompt)
        consistency = self._calculate_consistency(prompt)
        relevance = self._calculate_relevance(prompt)
        
        # Calculate overall score
        overall_score = (clarity + completeness + consistency + relevance) / 4
        
        # Create metrics
        metrics = QualityMetrics(
            clarity_score=clarity,
            completeness_score=completeness,
            consistency_score=consistency,
            relevance_score=relevance,
            metadata={
                'prompt_length': len(prompt),
                'timestamp': self._get_timestamp()
            }
        )
        
        self.analysis_history.append(metrics)
        return overall_score
        
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get statistics about quality analyses.
        
        Returns:
            Dict[str, Any]: Analysis statistics.
        """
        if not self.analysis_history:
            return {}
            
        total_analyses = len(self.analysis_history)
        
        # Calculate average scores
        avg_clarity = sum(r.clarity_score for r in self.analysis_history) / total_analyses
        avg_completeness = sum(r.completeness_score for r in self.analysis_history) / total_analyses
        avg_consistency = sum(r.consistency_score for r in self.analysis_history) / total_analyses
        avg_relevance = sum(r.relevance_score for r in self.analysis_history) / total_analyses
        
        return {
            'total_analyses': total_analyses,
            'average_scores': {
                'clarity': avg_clarity,
                'completeness': avg_completeness,
                'consistency': avg_consistency,
                'relevance': avg_relevance,
                'overall': (avg_clarity + avg_completeness + avg_consistency + avg_relevance) / 4
            }
        }
        
    def export_analysis_history(self, output_path: Path) -> None:
        """Export analysis history to a file.
        
        Args:
            output_path (Path): Path to save history.
        """
        history_data = {
            'statistics': self.get_analysis_stats(),
            'analyses': [
                {
                    'clarity_score': result.clarity_score,
                    'completeness_score': result.completeness_score,
                    'consistency_score': result.consistency_score,
                    'relevance_score': result.relevance_score,
                    'metadata': result.metadata
                }
                for result in self.analysis_history
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2)
            
    def _calculate_clarity(self, prompt: str) -> float:
        """Calculate clarity score."""
        # Simple clarity calculation based on average word length
        words = prompt.split()
        if not words:
            return 0.0
            
        avg_word_length = sum(len(word) for word in words) / len(words)
        clarity_score = min(1.0, max(0.0, 1.0 - (avg_word_length - 5) / 10))
        
        return clarity_score
        
    def _calculate_completeness(self, prompt: str) -> float:
        """Calculate completeness score."""
        # Simple completeness calculation based on prompt length
        min_length = self.config.get('min_prompt_length', 10)
        max_length = self.config.get('max_prompt_length', 1000)
        
        length = len(prompt.split())
        if length < min_length:
            return length / min_length
        elif length > max_length:
            return max(0.0, 1.0 - (length - max_length) / max_length)
        else:
            return 1.0
            
    def _calculate_consistency(self, prompt: str) -> float:
        """Calculate consistency score."""
        # Simple consistency calculation based on repeated words
        words = prompt.lower().split()
        if not words:
            return 0.0
            
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1
            
        max_repetition = max(word_freq.values())
        consistency_score = 1.0 - (max_repetition - 1) / len(words)
        
        return max(0.0, min(1.0, consistency_score))
        
    def _calculate_relevance(self, prompt: str) -> float:
        """Calculate relevance score."""
        # Simple relevance calculation based on keyword presence
        keywords = self.config.get('relevant_keywords', [])
        if not keywords:
            return 0.9  # Default score if no keywords defined
            
        prompt_lower = prompt.lower()
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in prompt_lower)
        relevance_score = keyword_matches / len(keywords)
        
        return max(0.0, min(1.0, relevance_score))
        
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat() 