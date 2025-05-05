"""
Batch Optimizer module for processing multiple prompts efficiently.
"""

import spacy
from typing import List, Dict, Any, Union
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import tiktoken

class BatchOptimizer:
    """A class for optimizing and processing multiple prompts in batch."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the BatchOptimizer.
        
        Args:
            model_name (str): The name of the spaCy model to use.
        """
        self.nlp = spacy.load(model_name)
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def process_batch(self, prompts: List[str]) -> List[str]:
        """Process a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to process.
            
        Returns:
            List[str]: Processed prompts.
        """
        with ThreadPoolExecutor() as executor:
            processed = list(executor.map(self._process_single, prompts))
        return processed
    
    def optimize_batch(self, prompts: List[str]) -> List[str]:
        """Optimize a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to optimize.
            
        Returns:
            List[str]: Optimized prompts.
        """
        with ThreadPoolExecutor() as executor:
            optimized = list(executor.map(self._optimize_single, prompts))
        return optimized
    
    def validate_batch(self, prompts: List[str]) -> List[bool]:
        """Validate a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to validate.
            
        Returns:
            List[bool]: Validation results.
        """
        with ThreadPoolExecutor() as executor:
            validation_results = list(executor.map(self._validate_single, prompts))
        return validation_results
    
    def _process_single(self, prompt: str) -> str:
        """Process a single prompt.
        
        Args:
            prompt (str): Prompt to process.
            
        Returns:
            str: Processed prompt.
        """
        doc = self.nlp(prompt)
        # Basic processing: remove extra whitespace and normalize
        processed = " ".join(token.text for token in doc)
        return processed.strip()
    
    def _optimize_single(self, prompt: str) -> str:
        """Optimize a single prompt.
        
        Args:
            prompt (str): Prompt to optimize.
            
        Returns:
            str: Optimized prompt.
        """
        doc = self.nlp(prompt)
        # Basic optimization: remove stop words and lemmatize
        optimized = " ".join(token.lemma_ for token in doc if not token.is_stop)
        return optimized.strip()
    
    def _validate_single(self, prompt: str) -> bool:
        """Validate a single prompt.
        
        Args:
            prompt (str): Prompt to validate.
            
        Returns:
            bool: True if prompt is valid, False otherwise.
        """
        # Basic validation: check if prompt is not empty and has reasonable length
        if not prompt or len(prompt.strip()) == 0:
            return False
        
        # Check token count
        tokens = self.encoding.encode(prompt)
        if len(tokens) > 4096:  # Maximum token limit
            return False
            
        return True 