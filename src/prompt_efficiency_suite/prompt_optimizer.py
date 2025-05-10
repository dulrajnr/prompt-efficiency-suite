"""
Prompt Optimizer module for optimizing individual prompts.
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class OptimizationResult:
    original_prompt: str
    optimized_prompt: str
    improvement_metrics: Dict[str, float]
    token_reduction: int
    execution_time: float
    metadata: Dict[str, Any]


class PromptOptimizer:
    """A class for optimizing individual prompts."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the PromptOptimizer.

        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.optimization_history: List[OptimizationResult] = []
        self.patterns = self._load_optimization_patterns()

    def optimize(self, prompt: str, optimization_params: Optional[Dict[str, Any]] = None) -> OptimizationResult:
        """Optimize a single prompt.

        Args:
            prompt (str): Prompt to optimize.
            optimization_params (Optional[Dict[str, Any]]): Optimization parameters.

        Returns:
            OptimizationResult: Optimization result.
        """
        params = optimization_params or {}

        # Apply optimization techniques
        optimized = self._apply_optimization_techniques(prompt, params)

        # Calculate metrics
        original_tokens = len(prompt.strip().split())
        optimized_tokens = len(optimized.strip().split())
        token_reduction = original_tokens - optimized_tokens
        improvement_metrics = self._calculate_improvement_metrics(prompt, optimized)

        # Create result
        result = OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=optimized,
            improvement_metrics=improvement_metrics,
            token_reduction=token_reduction,
            execution_time=1.0,  # Placeholder value
            metadata={"optimization_params": params, "techniques_applied": list(self.patterns.keys())},
        )

        self.optimization_history.append(result)
        return result

    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get statistics about optimization results.

        Returns:
            Dict[str, Any]: Optimization statistics.
        """
        if not self.optimization_history:
            return {}

        total_prompts = len(self.optimization_history)
        total_reduction = sum(r.token_reduction for r in self.optimization_history)
        total_time = sum(r.execution_time for r in self.optimization_history)

        improvement_metrics = defaultdict(float)
        for result in self.optimization_history:
            for metric, value in result.improvement_metrics.items():
                improvement_metrics[metric] += value

        return {
            "total_prompts": total_prompts,
            "average_token_reduction": total_reduction / total_prompts,
            "average_execution_time": total_time / total_prompts,
            "average_improvements": {metric: total / total_prompts for metric, total in improvement_metrics.items()},
        }

    def export_results(self, output_path: Path) -> None:
        """Export optimization results to a file.

        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            "statistics": self.get_optimization_stats(),
            "results": [
                {
                    "original_prompt": result.original_prompt,
                    "optimized_prompt": result.optimized_prompt,
                    "improvement_metrics": result.improvement_metrics,
                    "token_reduction": result.token_reduction,
                    "execution_time": result.execution_time,
                    "metadata": result.metadata,
                }
                for result in self.optimization_history
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2)

    def _load_optimization_patterns(self) -> Dict[str, re.Pattern]:
        """Load optimization patterns."""
        return {
            "remove_redundant_whitespace": re.compile(r"\s+"),
            "remove_empty_lines": re.compile(r"\n\s*\n"),
            "remove_trailing_whitespace": re.compile(r"[ \t]+$", re.MULTILINE),
            "remove_leading_whitespace": re.compile(r"^[ \t]+", re.MULTILINE),
        }

    def _apply_optimization_techniques(self, prompt: str, params: Dict[str, Any]) -> str:
        """Apply optimization techniques to the prompt.

        Args:
            prompt (str): Prompt to optimize.
            params (Dict[str, Any]): Optimization parameters.

        Returns:
            str: Optimized prompt.
        """
        optimized = prompt

        # Apply each optimization technique
        for name, pattern in self.patterns.items():
            if params.get(f"apply_{name}", True):
                if name == "remove_redundant_whitespace":
                    optimized = pattern.sub(" ", optimized)
                elif name == "remove_empty_lines":
                    optimized = pattern.sub("\n", optimized)
                elif name == "remove_trailing_whitespace":
                    optimized = pattern.sub("", optimized)
                elif name == "remove_leading_whitespace":
                    optimized = pattern.sub("", optimized)

        return optimized.strip()

    def _calculate_improvement_metrics(self, original: str, optimized: str) -> Dict[str, float]:
        """Calculate improvement metrics.

        Args:
            original (str): Original prompt.
            optimized (str): Optimized prompt.

        Returns:
            Dict[str, float]: Improvement metrics.
        """
        original_tokens = len(original.strip().split())
        optimized_tokens = len(optimized.strip().split())

        return {
            "token_reduction_ratio": (original_tokens - optimized_tokens) / original_tokens
            if original_tokens > 0
            else 0.0,
            "length_reduction_ratio": (len(original) - len(optimized)) / len(original) if len(original) > 0 else 0.0,
            "clarity_score": 0.8,  # Placeholder value
            "efficiency_score": 0.9,  # Placeholder value
        }
