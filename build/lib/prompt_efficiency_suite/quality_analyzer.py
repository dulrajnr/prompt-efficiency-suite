"""
Quality Analyzer module for analyzing prompt quality.
"""

import spacy
from typing import List, Dict, Any, Union
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class QualityAnalyzer:
    """A class for analyzing the quality of prompts."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the QualityAnalyzer.
        
        Args:
            model_name (str): The name of the spaCy model to use.
        """
        self.nlp = spacy.load(model_name)
        
    def analyze(self, prompt: str) -> float:
        """Analyze the quality of a single prompt.
        
        Args:
            prompt (str): Prompt to analyze.
            
        Returns:
            float: Quality score between 0 and 1.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        return self.analyze_quality(prompt)
        
    def analyze_quality(self, prompt: str) -> float:
        """Analyze the quality of a single prompt.
        
        Args:
            prompt (str): Prompt to analyze.
            
        Returns:
            float: Quality score between 0 and 1.
        """
        doc = self.nlp(prompt)
        
        # Calculate various quality metrics
        metrics = {
            'length': self._analyze_length(doc),
            'complexity': self._analyze_complexity(doc),
            'clarity': self._analyze_clarity(doc),
            'specificity': self._analyze_specificity(doc)
        }
        
        # Calculate weighted average
        weights = {
            'length': 0.25,
            'complexity': 0.25,
            'clarity': 0.25,
            'specificity': 0.25
        }
        
        quality_score = sum(metrics[k] * weights[k] for k in metrics)
        return quality_score
    
    def analyze_batch_quality(self, prompts: List[str]) -> List[float]:
        """Analyze the quality of a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to analyze.
            
        Returns:
            List[float]: List of quality scores.
        """
        with ThreadPoolExecutor() as executor:
            scores = list(executor.map(self.analyze_quality, prompts))
        return scores
    
    def _analyze_length(self, doc) -> float:
        """Analyze the length of a prompt.
        
        Args:
            doc: spaCy document.
            
        Returns:
            float: Length score between 0 and 1.
        """
        # Count non-punctuation tokens
        word_count = len([token for token in doc if not token.is_punct])
        
        # Score based on word count (optimal range: 10-50 words)
        if word_count < 10:
            return word_count / 10
        elif word_count > 50:
            return max(0, 1 - (word_count - 50) / 50)
        else:
            return 1.0
    
    def _analyze_complexity(self, doc) -> float:
        """Analyze the complexity of a prompt.
        
        Args:
            doc: spaCy document.
            
        Returns:
            float: Complexity score between 0 and 1.
        """
        # Calculate average word length
        word_lengths = [len(token.text) for token in doc if not token.is_punct]
        avg_length = np.mean(word_lengths) if word_lengths else 0
        
        # Score based on average word length (optimal range: 4-8 characters)
        if avg_length < 4:
            return avg_length / 4
        elif avg_length > 8:
            return max(0, 1 - (avg_length - 8) / 8)
        else:
            return 1.0
    
    def _analyze_clarity(self, doc) -> float:
        """Analyze the clarity of a prompt.
        
        Args:
            doc: spaCy document.
            
        Returns:
            float: Clarity score between 0 and 1.
        """
        # Calculate stop word ratio
        stop_words = len([token for token in doc if token.is_stop])
        total_words = len([token for token in doc if not token.is_punct])
        stop_word_ratio = stop_words / total_words if total_words > 0 else 0
        
        # Score based on stop word ratio (optimal range: 0.2-0.4)
        if stop_word_ratio < 0.2:
            return stop_word_ratio / 0.2
        elif stop_word_ratio > 0.4:
            return max(0, 1 - (stop_word_ratio - 0.4) / 0.4)
        else:
            return 1.0
    
    def _analyze_specificity(self, doc) -> float:
        """Analyze the specificity of a prompt.
        
        Args:
            doc: spaCy document.
            
        Returns:
            float: Specificity score between 0 and 1.
        """
        # Count named entities and noun phrases
        entities = len(doc.ents)
        noun_phrases = len([chunk for chunk in doc.noun_chunks])
        
        # Score based on number of specific elements
        specificity_score = min(1.0, (entities + noun_phrases) / 5)
        return specificity_score 