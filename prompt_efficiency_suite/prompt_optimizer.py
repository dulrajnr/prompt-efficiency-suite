"""
Prompt Optimizer module for optimizing individual prompts.
"""

import spacy
from typing import List, Dict, Any, Union
import tiktoken
from concurrent.futures import ThreadPoolExecutor

class PromptOptimizer:
    """A class for optimizing individual prompts."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the PromptOptimizer.
        
        Args:
            model_name (str): The name of the spaCy model to use.
        """
        self.nlp = spacy.load(model_name)
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def optimize(self, prompt: str) -> str:
        """Optimize a single prompt.
        
        Args:
            prompt (str): Prompt to optimize.
            
        Returns:
            str: Optimized prompt.
        """
        doc = self.nlp(prompt)
        
        # Remove stop words
        tokens = [token for token in doc if not token.is_stop]
        
        # Lemmatize
        lemmatized = [token.lemma_ for token in tokens]
        
        # Remove extra whitespace
        optimized = " ".join(lemmatized)
        optimized = " ".join(optimized.split())
        
        return optimized.strip()
    
    def optimize_batch(self, prompts: List[str]) -> List[str]:
        """Optimize a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to optimize.
            
        Returns:
            List[str]: Optimized prompts.
        """
        with ThreadPoolExecutor() as executor:
            optimized = list(executor.map(self.optimize, prompts))
        return optimized
    
    def analyze_quality(self, prompt: str) -> float:
        """Analyze the quality of a prompt.
        
        Args:
            prompt (str): Prompt to analyze.
            
        Returns:
            float: Quality score between 0 and 1.
        """
        doc = self.nlp(prompt)
        
        # Calculate various quality metrics
        token_count = len(doc)
        word_count = len([token for token in doc if not token.is_punct])
        stop_word_ratio = len([token for token in doc if token.is_stop]) / token_count if token_count > 0 else 0
        
        # Normalize metrics
        token_score = min(token_count / 100, 1.0)  # Cap at 100 tokens
        word_score = min(word_count / 50, 1.0)  # Cap at 50 words
        stop_word_score = 1 - stop_word_ratio  # Lower stop word ratio is better
        
        # Calculate final score
        quality_score = (token_score + word_score + stop_word_score) / 3
        
        return quality_score
    
    def get_token_count(self, prompt: str) -> int:
        """Get the token count of a prompt.
        
        Args:
            prompt (str): Prompt to count tokens for.
            
        Returns:
            int: Number of tokens.
        """
        return len(self.encoding.encode(prompt))
    
    def get_word_count(self, prompt: str) -> int:
        """Get the word count of a prompt.
        
        Args:
            prompt (str): Prompt to count words for.
            
        Returns:
            int: Number of words.
        """
        doc = self.nlp(prompt)
        return len([token for token in doc if not token.is_punct])
    
    def get_stop_word_count(self, prompt: str) -> int:
        """Get the stop word count of a prompt.
        
        Args:
            prompt (str): Prompt to count stop words for.
            
        Returns:
            int: Number of stop words.
        """
        doc = self.nlp(prompt)
        return len([token for token in doc if token.is_stop]) 