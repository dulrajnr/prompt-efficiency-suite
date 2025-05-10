"""
Adaptive Budgeting module for dynamically adjusting token budgets based on context and requirements.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from .metrics import EfficiencyMetrics


@dataclass
class BudgetAlert:
    """Alert for budget-related issues."""

    alert_type: str
    severity: str
    message: str
    component: str
    threshold: float
    current_value: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BudgetMetrics:
    """Metrics for budget usage and efficiency."""

    total_tokens_allocated: int
    total_tokens_used: int
    system_efficiency: float
    context_efficiency: float
    instruction_efficiency: float
    response_efficiency: float
    cost_efficiency: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BudgetAllocation:
    """Data class for storing budget allocation information."""

    total_budget: int
    used_budget: int
    remaining_budget: int
    allocation_period: timedelta
    start_time: datetime
    end_time: datetime
    metadata: Dict[str, Union[str, int, float]] = None


class AdaptiveBudgetManager:
    """Manages adaptive token budgets based on usage patterns."""

    def __init__(
        self,
        initial_budget: int,
        allocation_period: timedelta = timedelta(days=1),
        min_budget: int = 1000,
        max_budget: int = 1000000,
    ):
        """Initialize the budget manager.

        Args:
            initial_budget: Initial token budget
            allocation_period: Time period for budget allocation
            min_budget: Minimum allowed budget
            max_budget: Maximum allowed budget
        """
        self.initial_budget = initial_budget
        self.allocation_period = allocation_period
        self.min_budget = min_budget
        self.max_budget = max_budget
        self.current_allocation = None
        self.usage_history: List[EfficiencyMetrics] = []
        self._initialize_allocation()

    def _initialize_allocation(self) -> None:
        """Initialize the current budget allocation."""
        now = datetime.utcnow()
        self.current_allocation = BudgetAllocation(
            total_budget=self.initial_budget,
            used_budget=0,
            remaining_budget=self.initial_budget,
            allocation_period=self.allocation_period,
            start_time=now,
            end_time=now + self.allocation_period,
            metadata={"allocation_type": "initial"},
        )

    def record_usage(self, metrics: EfficiencyMetrics) -> None:
        """Record token usage.

        Args:
            metrics: The efficiency metrics to record
        """
        self.usage_history.append(metrics)
        if self.current_allocation:
            self.current_allocation.used_budget += metrics.token_count
            self.current_allocation.remaining_budget = max(
                0,
                self.current_allocation.total_budget - self.current_allocation.used_budget,
            )

    def get_remaining_budget(self) -> int:
        """Get the remaining budget.

        Returns:
            Remaining token budget
        """
        if not self.current_allocation:
            return 0
        return self.current_allocation.remaining_budget

    def can_allocate(self, required_tokens: int) -> bool:
        """Check if there's enough budget for the required tokens.

        Args:
            required_tokens: Number of tokens required

        Returns:
            True if there's enough budget, False otherwise
        """
        if not self.current_allocation:
            return False
        return self.current_allocation.remaining_budget >= required_tokens

    def adjust_budget(self) -> None:
        """Adjust the budget based on usage patterns."""
        if not self.usage_history:
            return

        # Calculate usage statistics
        recent_usage = [m for m in self.usage_history if m.timestamp > datetime.utcnow() - self.allocation_period]

        if not recent_usage:
            return

        # Calculate average daily usage
        daily_usage = np.mean([m.token_count for m in recent_usage])

        # Calculate success rate
        success_rate = np.mean([m.success_rate for m in recent_usage])

        # Adjust budget based on usage and success
        if success_rate > 0.9:  # High success rate
            new_budget = int(daily_usage * 1.2)  # Increase by 20%
        elif success_rate > 0.7:  # Good success rate
            new_budget = int(daily_usage * 1.1)  # Increase by 10%
        elif success_rate < 0.5:  # Low success rate
            new_budget = int(daily_usage * 0.8)  # Decrease by 20%
        else:
            new_budget = int(daily_usage)  # Keep the same

        # Ensure budget stays within limits
        new_budget = max(self.min_budget, min(self.max_budget, new_budget))

        # Create new allocation
        now = datetime.utcnow()
        self.current_allocation = BudgetAllocation(
            total_budget=new_budget,
            used_budget=0,
            remaining_budget=new_budget,
            allocation_period=self.allocation_period,
            start_time=now,
            end_time=now + self.allocation_period,
            metadata={
                "previous_budget": self.current_allocation.total_budget if self.current_allocation else 0,
                "adjustment_factor": new_budget
                / (self.current_allocation.total_budget if self.current_allocation else 1),
                "success_rate": success_rate,
                "daily_usage": daily_usage,
            },
        )

    def get_budget_stats(self) -> Dict[str, Union[int, float]]:
        """Get statistics about budget usage.

        Returns:
            Dictionary containing budget statistics
        """
        if not self.current_allocation:
            return {}

        recent_usage = [m for m in self.usage_history if m.timestamp > datetime.utcnow() - self.allocation_period]

        if not recent_usage:
            return {
                "total_budget": self.current_allocation.total_budget,
                "used_budget": self.current_allocation.used_budget,
                "remaining_budget": self.current_allocation.remaining_budget,
                "allocation_period_days": self.allocation_period.days,
            }

        return {
            "total_budget": self.current_allocation.total_budget,
            "used_budget": self.current_allocation.used_budget,
            "remaining_budget": self.current_allocation.remaining_budget,
            "allocation_period_days": self.allocation_period.days,
            "avg_daily_usage": np.mean([m.token_count for m in recent_usage]),
            "success_rate": np.mean([m.success_rate for m in recent_usage]),
            "total_requests": len(recent_usage),
        }


class AdaptiveBudgeting:
    """A class for managing and adjusting token budgets adaptively."""

    def __init__(self):
        """Initialize the AdaptiveBudgeting system."""
        self.model_configs: Dict[str, Dict[str, Any]] = {}
        self.usage_history: List[Dict[str, Any]] = []
        self.adjustment_factors: Dict[str, float] = {}

    def load_model_config(self, model_name: str, config_path: Path) -> None:
        """Load configuration for a specific model.

        Args:
            model_name (str): Name of the model.
            config_path (Path): Path to the configuration file.
        """
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.model_configs[model_name] = {
            "max_tokens": config.get("max_tokens", 2048),
            "token_cost": config.get("token_cost", 0.0),
            "context_ratio": config.get("context_ratio", 0.7),
            "system_ratio": config.get("system_ratio", 0.1),
            "instruction_ratio": config.get("instruction_ratio", 0.1),
            "response_ratio": config.get("response_ratio", 0.1),
        }

    def calculate_budget(
        self,
        model_name: str,
        task_type: str,
        context_length: Optional[int] = None,
        requirements: Optional[Dict[str, Any]] = None,
    ) -> BudgetAllocation:
        """Calculate token budget allocation based on model and task requirements.

        Args:
            model_name (str): Name of the model to use.
            task_type (str): Type of task (e.g., 'summarization', 'qa', 'chat').
            context_length (Optional[int]): Length of the context in tokens.
            requirements (Optional[Dict[str, Any]]): Additional requirements.

        Returns:
            BudgetAllocation: Calculated budget allocation.
        """
        if model_name not in self.model_configs:
            raise ValueError(f"Model '{model_name}' not configured")

        config = self.model_configs[model_name]
        max_tokens = config["max_tokens"]

        # Adjust ratios based on task type and requirements
        ratios = self._adjust_ratios(
            task_type,
            config["context_ratio"],
            config["system_ratio"],
            config["instruction_ratio"],
            config["response_ratio"],
            requirements,
        )

        # Calculate token allocations
        total_tokens = min(max_tokens, context_length or max_tokens)
        allocation = {
            "system_tokens": int(total_tokens * ratios["system"]),
            "context_tokens": int(total_tokens * ratios["context"]),
            "instruction_tokens": int(total_tokens * ratios["instruction"]),
            "response_tokens": int(total_tokens * ratios["response"]),
        }

        # Add metadata
        metadata = {
            "model_name": model_name,
            "task_type": task_type,
            "original_context_length": context_length,
            "adjusted_ratios": ratios,
            "cost_estimate": self._estimate_cost(total_tokens, config["token_cost"]),
        }

        return BudgetAllocation(
            total_budget=total_tokens,
            used_budget=0,
            remaining_budget=total_tokens,
            allocation_period=timedelta(days=1),
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(days=1),
            metadata=metadata,
        )

    def update_usage(self, allocation: BudgetAllocation, actual_usage: Dict[str, int]) -> None:
        """Update usage history with actual token usage.

        Args:
            allocation (BudgetAllocation): Original budget allocation.
            actual_usage (Dict[str, int]): Actual token usage.
        """
        usage_data = {
            "allocated": {
                "total": allocation.total_budget,
                "system": allocation.system_tokens,
                "context": allocation.context_tokens,
                "instruction": allocation.instruction_tokens,
                "response": allocation.response_tokens,
            },
            "actual": actual_usage,
            "metadata": allocation.metadata,
        }

        self.usage_history.append(usage_data)
        self._update_adjustment_factors()

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get statistics about token usage.

        Returns:
            Dict[str, Any]: Usage statistics.
        """
        if not self.usage_history:
            return {}

        stats = {
            "total_requests": len(self.usage_history),
            "average_usage": self._calculate_average_usage(),
            "efficiency_metrics": self._calculate_efficiency_metrics(),
            "adjustment_factors": self.adjustment_factors.copy(),
        }

        return stats

    def _adjust_ratios(
        self,
        task_type: str,
        context_ratio: float,
        system_ratio: float,
        instruction_ratio: float,
        response_ratio: float,
        requirements: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, float]:
        """Adjust token ratios based on task type and requirements."""
        # Apply task-specific adjustments
        task_adjustments = {
            "summarization": {"context": 1.2, "response": 0.8},
            "qa": {"context": 0.9, "instruction": 1.1},
            "chat": {"system": 0.8, "response": 1.2},
        }

        adjustments = task_adjustments.get(task_type, {})

        # Apply requirement-specific adjustments
        if requirements:
            if requirements.get("detailed_response", False):
                adjustments["response"] = adjustments.get("response", 1.0) * 1.2
            if requirements.get("minimal_context", False):
                adjustments["context"] = adjustments.get("context", 1.0) * 0.8

        # Apply historical adjustment factors
        for component, factor in self.adjustment_factors.items():
            adjustments[component] = adjustments.get(component, 1.0) * factor

        # Calculate adjusted ratios
        ratios = {
            "context": context_ratio * adjustments.get("context", 1.0),
            "system": system_ratio * adjustments.get("system", 1.0),
            "instruction": instruction_ratio * adjustments.get("instruction", 1.0),
            "response": response_ratio * adjustments.get("response", 1.0),
        }

        # Normalize ratios to sum to 1.0
        total = sum(ratios.values())
        return {k: v / total for k, v in ratios.items()}

    def _update_adjustment_factors(self) -> None:
        """Update adjustment factors based on usage history."""
        if len(self.usage_history) < 5:
            return

        recent_history = self.usage_history[-5:]
        component_usage = defaultdict(list)

        for entry in recent_history:
            allocated = entry["allocated"]
            actual = entry["actual"]

            for component in ["system", "context", "instruction", "response"]:
                if component in allocated and component in actual:
                    ratio = actual[component] / allocated[component]
                    component_usage[component].append(ratio)

        # Calculate new adjustment factors
        for component, ratios in component_usage.items():
            avg_ratio = np.mean(ratios)
            # Smooth the adjustment to avoid sudden changes
            current = self.adjustment_factors.get(component, 1.0)
            self.adjustment_factors[component] = 0.8 * current + 0.2 * avg_ratio

    def _calculate_average_usage(self) -> Dict[str, float]:
        """Calculate average token usage across components."""
        if not self.usage_history:
            return {}

        totals = defaultdict(int)
        counts = defaultdict(int)

        for entry in self.usage_history:
            actual = entry["actual"]
            for component, tokens in actual.items():
                totals[component] += tokens
                counts[component] += 1

        return {component: totals[component] / counts[component] for component in totals}

    def _calculate_efficiency_metrics(self) -> Dict[str, float]:
        """Calculate efficiency metrics based on usage history."""
        if not self.usage_history:
            return {}

        allocation_ratios = []
        for entry in self.usage_history:
            allocated = entry["allocated"]
            actual = entry["actual"]

            if "total" in allocated and "total" in actual:
                ratio = actual["total"] / allocated["total"]
                allocation_ratios.append(ratio)

        return {
            "average_efficiency": np.mean(allocation_ratios),
            "efficiency_std": np.std(allocation_ratios),
            "min_efficiency": min(allocation_ratios),
            "max_efficiency": max(allocation_ratios),
        }

    def _estimate_cost(self, total_tokens: int, token_cost: float) -> float:
        """Estimate the cost for the token usage."""
        return total_tokens * token_cost
