"""
Token Counter module for counting tokens in prompts.
"""

import tiktoken
from typing import List, Dict, Any, Union
from concurrent.futures import ThreadPoolExecutor

class TokenCounter:
    """A class for counting tokens in prompts."""
    
    def __init__(self, model_name: str = "cl100k_base"):
        """Initialize the TokenCounter.
        
        Args:
            model_name (str): The name of the tokenizer model to use.
        """
        self.encoding = tiktoken.get_encoding(model_name)
        
    def count_tokens(self, prompt: str) -> int:
        """Count tokens in a single prompt.
        
        Args:
            prompt (str): Prompt to count tokens for.
            
        Returns:
            int: Number of tokens.
        """
        return len(self.encoding.encode(prompt))
    
    def count_batch_tokens(self, prompts: List[str]) -> List[int]:
        """Count tokens in a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to count tokens for.
            
        Returns:
            List[int]: List of token counts.
        """
        with ThreadPoolExecutor() as executor:
            counts = list(executor.map(self.count_tokens, prompts))
        return counts
    
    def get_token_chunks(self, prompt: str, max_tokens: int = 4096) -> List[str]:
        """Split a prompt into chunks of maximum token size.
        
        Args:
            prompt (str): Prompt to split.
            max_tokens (int): Maximum number of tokens per chunk.
            
        Returns:
            List[str]: List of prompt chunks.
        """
        tokens = self.encoding.encode(prompt)
        chunks = []
        
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i + max_tokens]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
        return chunks
    
    def estimate_cost(self, prompt: str, cost_per_1k_tokens: float = 0.002) -> float:
        """Estimate the cost of a prompt based on token count.
        
        Args:
            prompt (str): Prompt to estimate cost for.
            cost_per_1k_tokens (float): Cost per 1000 tokens.
            
        Returns:
            float: Estimated cost.
        """
        token_count = self.count_tokens(prompt)
        return (token_count / 1000) * cost_per_1k_tokens
    
    def estimate_batch_cost(self, prompts: List[str], cost_per_1k_tokens: float = 0.002) -> List[float]:
        """Estimate the cost of a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to estimate cost for.
            cost_per_1k_tokens (float): Cost per 1000 tokens.
            
        Returns:
            List[float]: List of estimated costs.
        """
        with ThreadPoolExecutor() as executor:
            costs = list(executor.map(
                lambda p: self.estimate_cost(p, cost_per_1k_tokens),
                prompts
            ))
        return costs 