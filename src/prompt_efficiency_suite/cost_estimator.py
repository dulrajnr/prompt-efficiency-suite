"""Cost Estimator - A module for estimating prompt costs."""

import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class CostEstimate:
    """Cost estimate for a prompt."""

    token_count: int
    cost_per_token: float
    total_cost: float
    model_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class CostEstimator:
    """A class for estimating prompt costs."""

    def __init__(self):
        """Initialize the cost estimator."""
        self.logger = logging.getLogger(__name__)
        self.estimation_history: List[CostEstimate] = []
        self.model_rates = self._load_model_rates()

    def estimate(self, prompt: str, model: str = "gpt-4") -> Dict[str, Any]:
        """Estimate the cost of a prompt.

        Args:
            prompt: The prompt to estimate
            model: The model to use for estimation

        Returns:
            Dictionary containing cost estimation
        """
        # Count tokens
        token_count = self._count_tokens(prompt)

        # Get model rates
        rates = self._get_model_rates(model)

        # Calculate cost
        cost = token_count * rates["price_per_token"]

        return {
            "token_count": token_count,
            "model": model,
            "cost": cost,
            "rates": rates,
        }

    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in text.

        Args:
            text: The text to count tokens in

        Returns:
            Number of tokens
        """
        # TODO: Implement proper token counting
        return len(text.split())

    def _get_model_rates(self, model: str) -> Dict[str, float]:
        """Get the rates for a model.

        Args:
            model: The model to get rates for

        Returns:
            Dictionary containing model rates
        """
        rates = {
            "gpt-4": {"price_per_token": 0.03, "max_tokens": 8192, "min_tokens": 1},
            "gpt-3.5-turbo": {
                "price_per_token": 0.002,
                "max_tokens": 4096,
                "min_tokens": 1,
            },
        }

        return rates.get(model, rates["gpt-4"])

    def estimate_cost(self, prompt: str, model_name: str = "gpt-3.5-turbo") -> float:
        """Estimate cost for a prompt.

        Args:
            prompt (str): Prompt to estimate cost for.
            model_name (str): Name of the model to use.

        Returns:
            float: Estimated cost in USD.
        """
        # Get token count (simple estimation)
        token_count = len(prompt.split()) * 1.3  # Rough approximation

        # Get cost per token
        cost_per_token = self.model_rates.get(model_name, 0.0)

        # Calculate total cost
        total_cost = token_count * cost_per_token

        # Create estimate
        estimate = CostEstimate(
            token_count=int(token_count),
            cost_per_token=cost_per_token,
            total_cost=total_cost,
            model_name=model_name,
            metadata={"prompt_length": len(prompt), "timestamp": self._get_timestamp()},
        )

        self.estimation_history.append(estimate)
        return total_cost

    def get_estimation_stats(self) -> Dict[str, Any]:
        """Get statistics about cost estimations.

        Returns:
            Dict[str, Any]: Estimation statistics.
        """
        if not self.estimation_history:
            return {}

        total_estimations = len(self.estimation_history)
        total_cost = sum(e.total_cost for e in self.estimation_history)
        total_tokens = sum(e.token_count for e in self.estimation_history)

        # Calculate model usage distribution
        model_usage: Dict[str, int] = defaultdict(int)
        for estimate in self.estimation_history:
            model_usage[estimate.model_name] += 1

        return {
            "total_estimations": total_estimations,
            "total_cost": total_cost,
            "average_cost": total_cost / total_estimations,
            "total_tokens": total_tokens,
            "average_tokens": total_tokens / total_estimations,
            "model_usage": dict(model_usage),
        }

    def export_estimation_history(self, output_path: Path) -> None:
        """Export estimation history to a file.

        Args:
            output_path (Path): Path to save history.
        """
        history_data = {
            "statistics": self.get_estimation_stats(),
            "estimations": [
                {
                    "token_count": estimate.token_count,
                    "cost_per_token": estimate.cost_per_token,
                    "total_cost": estimate.total_cost,
                    "model_name": estimate.model_name,
                    "metadata": estimate.metadata,
                }
                for estimate in self.estimation_history
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2)

    def _load_model_rates(self) -> Dict[str, float]:
        """Load model rate configurations."""
        return {
            "gpt-4": 0.03,  # $0.03 per 1K tokens
            "gpt-4-32k": 0.06,  # $0.06 per 1K tokens
            "gpt-3.5-turbo": 0.002,  # $0.002 per 1K tokens
            "gpt-3.5-turbo-16k": 0.004,  # $0.004 per 1K tokens
            "text-davinci-003": 0.02,  # $0.02 per 1K tokens
            "text-curie-001": 0.002,  # $0.002 per 1K tokens
            "text-babbage-001": 0.0005,  # $0.0005 per 1K tokens
            "text-ada-001": 0.0004,  # $0.0004 per 1K tokens
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().isoformat()
