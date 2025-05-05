"""
Cost Estimator module for estimating prompt costs.
"""

import tiktoken
from typing import List, Dict, Any, Union
from concurrent.futures import ThreadPoolExecutor

class CostEstimator:
    """A class for estimating costs of prompts."""
    
    def __init__(self, model_name: str = "cl100k_base"):
        """Initialize the CostEstimator.
        
        Args:
            model_name (str): The name of the tokenizer model to use.
        """
        self.encoding = tiktoken.get_encoding(model_name)
        
    def estimate_cost(self, prompt: str, cost_per_1k_tokens: float = 0.002) -> float:
        """Estimate the cost of a single prompt.
        
        Args:
            prompt (str): Prompt to estimate cost for.
            cost_per_1k_tokens (float): Cost per 1000 tokens.
            
        Returns:
            float: Estimated cost.
        """
        token_count = len(self.encoding.encode(prompt))
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
    
    def get_token_count(self, prompt: str) -> int:
        """Get the token count of a prompt.
        
        Args:
            prompt (str): Prompt to count tokens for.
            
        Returns:
            int: Number of tokens.
        """
        return len(self.encoding.encode(prompt))
    
    def get_batch_token_counts(self, prompts: List[str]) -> List[int]:
        """Get token counts for a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to count tokens for.
            
        Returns:
            List[int]: List of token counts.
        """
        with ThreadPoolExecutor() as executor:
            counts = list(executor.map(self.get_token_count, prompts))
        return counts
    
    def estimate_total_cost(self, prompts: List[str], cost_per_1k_tokens: float = 0.002) -> float:
        """Estimate the total cost of a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to estimate cost for.
            cost_per_1k_tokens (float): Cost per 1000 tokens.
            
        Returns:
            float: Total estimated cost.
        """
        costs = self.estimate_batch_cost(prompts, cost_per_1k_tokens)
        return sum(costs)
    
    def get_cost_breakdown(self, prompts: List[str], cost_per_1k_tokens: float = 0.002) -> Dict[str, Any]:
        """Get a detailed cost breakdown for a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to analyze.
            cost_per_1k_tokens (float): Cost per 1000 tokens.
            
        Returns:
            Dict[str, Any]: Cost breakdown including total cost, average cost, and individual costs.
        """
        costs = self.estimate_batch_cost(prompts, cost_per_1k_tokens)
        token_counts = self.get_batch_token_counts(prompts)
        
        return {
            'total_cost': sum(costs),
            'average_cost': sum(costs) / len(costs) if costs else 0,
            'total_tokens': sum(token_counts),
            'average_tokens': sum(token_counts) / len(token_counts) if token_counts else 0,
            'individual_costs': list(zip(prompts, costs, token_counts))
        } 