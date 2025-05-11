"""
Adaptive Budgeting module for dynamically adjusting token budgets based on context and requirements.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

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
    metadata: Dict[str, Union[str, int, float]] = field(default_factory=dict)


class ModelConfig(TypedDict):
    """Configuration for a model."""

    max_tokens: int
    token_cost: float
    context_ratio: float
    system_ratio: float
    instruction_ratio: float
    response_ratio: float


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
            initial_budget (int): Initial token budget.
            allocation_period (timedelta): Time period for budget allocation.
            min_budget (int): Minimum allowed budget.
            max_budget (int): Maximum allowed budget.
        """
        self.initial_budget: int = initial_budget
        self.allocation_period: timedelta = allocation_period
        self.min_budget: int = min_budget
        self.max_budget: int = max_budget
        self.current_allocation: Optional[BudgetAllocation] = None
        self.usage_history: List[EfficiencyMetrics] = []
        self._initialize_allocation()

    def _initialize_allocation(self) -> None:
        """Initialize the current budget allocation."""
        now: datetime = datetime.utcnow()
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
            metrics (EfficiencyMetrics): The efficiency metrics to record.
        """
        self.usage_history.append(metrics)
        if self.current_allocation:
            self.current_allocation.used_budget += metrics.token_count
            self.current_allocation.remaining_budget = max(
                0,
                self.current_allocation.total_budget
                - self.current_allocation.used_budget,
            )

    def get_remaining_budget(self) -> int:
        """Get the remaining budget.

        Returns:
            int: Remaining token budget.
        """
        if not self.current_allocation:
            return 0
        return self.current_allocation.remaining_budget

    def can_allocate(self, required_tokens: int) -> bool:
        """Check if there's enough budget for the required tokens.

        Args:
            required_tokens (int): Number of tokens required.

        Returns:
            bool: True if there's enough budget, False otherwise.
        """
        if not self.current_allocation:
            return False
        return self.current_allocation.remaining_budget >= required_tokens

    def adjust_budget(self) -> None:
        """Adjust the budget based on usage patterns."""
        if not self.usage_history:
            return

        # Calculate usage statistics
        recent_usage: List[EfficiencyMetrics] = [
            m
            for m in self.usage_history
            if m.timestamp > datetime.utcnow() - self.allocation_period
        ]

        if not recent_usage:
            return

        # Calculate average daily usage
        daily_usage: float = np.mean([m.token_count for m in recent_usage])

        # Calculate success rate
        success_rate: float = np.mean([m.success_rate for m in recent_usage])

        # Adjust budget based on usage and success
        if success_rate > 0.9:  # High success rate
            new_budget: int = int(daily_usage * 1.2)  # Increase by 20%
        elif success_rate > 0.7:  # Good success rate
            new_budget = int(daily_usage * 1.1)  # Increase by 10%
        elif success_rate < 0.5:  # Low success rate
            new_budget = int(daily_usage * 0.8)  # Decrease by 20%
        else:
            new_budget = int(daily_usage)  # Keep the same

        # Ensure budget stays within limits
        new_budget = max(self.min_budget, min(self.max_budget, new_budget))

        # Create new allocation
        now: datetime = datetime.utcnow()
        self.current_allocation = BudgetAllocation(
            total_budget=new_budget,
            used_budget=0,
            remaining_budget=new_budget,
            allocation_period=self.allocation_period,
            start_time=now,
            end_time=now + self.allocation_period,
            metadata={
                "previous_budget": (
                    self.current_allocation.total_budget
                    if self.current_allocation
                    else 0
                ),
                "adjustment_factor": new_budget
                / (
                    self.current_allocation.total_budget
                    if self.current_allocation
                    else 1
                ),
                "success_rate": success_rate,
                "daily_usage": daily_usage,
            },
        )

    def get_budget_stats(self) -> Dict[str, Union[int, float]]:
        """Get statistics about budget usage.

        Returns:
            Dict[str, Union[int, float]]: Dictionary containing budget statistics.
        """
        if not self.current_allocation:
            return {}

        return {
            "total_budget": self.current_allocation.total_budget,
            "used_budget": self.current_allocation.used_budget,
            "remaining_budget": self.current_allocation.remaining_budget,
            "usage_percentage": (
                self.current_allocation.used_budget
                / self.current_allocation.total_budget
                * 100
            ),
            "allocation_period_days": self.allocation_period.days,
            "time_remaining": (
                self.current_allocation.end_time - datetime.utcnow()
            ).total_seconds()
            / 86400,  # Convert to days
        }


class AdaptiveBudgeting:
    """Class for adaptive token budgeting."""

    def __init__(self, initial_budget: float = 100.0) -> None:
        self.initial_budget = initial_budget
        self.current_budget = initial_budget
        self.usage_history: List[Dict[str, Any]] = []

    def allocate_budget(
        self, prompt: str, options: Optional[Dict[str, Any]] = None
    ) -> float:
        """Allocate budget for a prompt based on its characteristics."""
        options = options or {}
        # Placeholder implementation
        return min(self.current_budget, 10.0)

    def update_budget(self, usage: Dict[str, Any]) -> None:
        """Update the budget based on usage data."""
        self.usage_history.append(usage)
        # Placeholder implementation

    def get_budget_stats(self) -> Dict[str, Union[str, int, float, Dict[str, Any]]]:
        """Get statistics about budget usage."""
        return {
            "initial_budget": self.initial_budget,
            "current_budget": self.current_budget,
            "total_usage": len(self.usage_history),
            "usage_by_type": {},
        }

    def load_model_config(self, model_name: str, config_path: Path) -> None:
        """Load model configuration from a file.

        Args:
            model_name (str): Name of the model.
            config_path (Path): Path to the configuration file.
        """
        with open(config_path, "r", encoding="utf-8") as f:
            config_data: Dict[str, Any] = json.load(f)

        self.model_configs[model_name] = {
            "max_tokens": config_data["max_tokens"],
            "token_cost": config_data["token_cost"],
            "context_ratio": config_data["context_ratio"],
            "system_ratio": config_data["system_ratio"],
            "instruction_ratio": config_data["instruction_ratio"],
            "response_ratio": config_data["response_ratio"],
        }

    def calculate_budget(
        self,
        model_name: str,
        task_type: str,
        context_length: Optional[int] = None,
        requirements: Optional[Dict[str, Any]] = None,
    ) -> BudgetAllocation:
        """Calculate token budget for a task.

        Args:
            model_name (str): Name of the model to use.
            task_type (str): Type of task being performed.
            context_length (Optional[int]): Length of the context.
            requirements (Optional[Dict[str, Any]]): Additional requirements.

        Returns:
            BudgetAllocation: Calculated budget allocation.
        """
        if model_name not in self.model_configs:
            raise ValueError(f"Model {model_name} not configured")

        config: ModelConfig = self.model_configs[model_name]
        requirements = requirements or {}

        # Calculate base ratios
        context_ratio: float = config["context_ratio"]
        system_ratio: float = config["system_ratio"]
        instruction_ratio: float = config["instruction_ratio"]
        response_ratio: float = config["response_ratio"]

        # Adjust ratios based on task type and requirements
        adjusted_ratios: Dict[str, float] = self._adjust_ratios(
            task_type,
            context_ratio,
            system_ratio,
            instruction_ratio,
            response_ratio,
            requirements,
        )

        # Calculate total budget
        total_budget: int = config["max_tokens"]
        if context_length:
            total_budget = min(
                total_budget,
                int(context_length / adjusted_ratios["context"]),
            )

        # Calculate component budgets
        context_budget: int = int(total_budget * adjusted_ratios["context"])
        system_budget: int = int(total_budget * adjusted_ratios["system"])
        instruction_budget: int = int(total_budget * adjusted_ratios["instruction"])
        response_budget: int = int(total_budget * adjusted_ratios["response"])

        # Create allocation
        now: datetime = datetime.utcnow()
        allocation: BudgetAllocation = BudgetAllocation(
            total_budget=total_budget,
            used_budget=0,
            remaining_budget=total_budget,
            allocation_period=timedelta(hours=1),
            start_time=now,
            end_time=now + timedelta(hours=1),
            metadata={
                "model": model_name,
                "task_type": task_type,
                "component_budgets": {
                    "context": context_budget,
                    "system": system_budget,
                    "instruction": instruction_budget,
                    "response": response_budget,
                },
                "adjusted_ratios": adjusted_ratios,
                "estimated_cost": self._estimate_cost(
                    total_budget, config["token_cost"]
                ),
            },
        )

        return allocation

    def update_usage(
        self, allocation: BudgetAllocation, actual_usage: Dict[str, int]
    ) -> None:
        """Update usage statistics.

        Args:
            allocation (BudgetAllocation): The budget allocation.
            actual_usage (Dict[str, int]): Actual token usage by component.
        """
        usage_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow(),
            "allocation": allocation.__dict__,
            "actual_usage": actual_usage,
            "efficiency": self._calculate_efficiency_metrics(),
        }

        self.usage_history.append(usage_data)
        self._update_adjustment_factors()

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics.

        Returns:
            Dict[str, Any]: Usage statistics.
        """
        if not self.usage_history:
            return {}

        return {
            "total_usage": len(self.usage_history),
            "average_usage": self._calculate_average_usage(),
            "efficiency_metrics": self._calculate_efficiency_metrics(),
            "adjustment_factors": self.adjustment_factors,
            "metadata": {"timestamp": datetime.utcnow().isoformat()},
        }

    def _adjust_ratios(
        self,
        task_type: str,
        context_ratio: float,
        system_ratio: float,
        instruction_ratio: float,
        response_ratio: float,
        requirements: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, float]:
        """Adjust budget ratios based on task type and requirements.

        Args:
            task_type (str): Type of task.
            context_ratio (float): Base context ratio.
            system_ratio (float): Base system ratio.
            instruction_ratio (float): Base instruction ratio.
            response_ratio (float): Base response ratio.
            requirements (Optional[Dict[str, Any]]): Additional requirements.

        Returns:
            Dict[str, float]: Adjusted ratios.
        """
        requirements = requirements or {}
        adjusted: Dict[str, float] = {
            "context": context_ratio * self.adjustment_factors["context"],
            "system": system_ratio * self.adjustment_factors["system"],
            "instruction": instruction_ratio * self.adjustment_factors["instruction"],
            "response": response_ratio * self.adjustment_factors["response"],
        }

        # Adjust based on task type
        if task_type == "code_generation":
            adjusted["context"] *= 1.2
            adjusted["instruction"] *= 0.8
        elif task_type == "text_generation":
            adjusted["context"] *= 0.8
            adjusted["response"] *= 1.2
        elif task_type == "analysis":
            adjusted["context"] *= 1.5
            adjusted["response"] *= 0.7

        # Adjust based on requirements
        if requirements.get("high_precision"):
            adjusted["context"] *= 1.2
            adjusted["instruction"] *= 1.2
        if requirements.get("fast_response"):
            adjusted["response"] *= 1.2
            adjusted["context"] *= 0.8

        # Normalize ratios
        total: float = sum(adjusted.values())
        return {k: v / total for k, v in adjusted.items()}

    def _update_adjustment_factors(self) -> None:
        """Update adjustment factors based on usage history."""
        if not self.usage_history:
            return

        recent_usage: List[Dict[str, Any]] = [
            u for u in self.usage_history[-10:] if "efficiency" in u
        ]

        if not recent_usage:
            return

        # Calculate average efficiency for each component
        avg_efficiency: Dict[str, float] = {
            component: np.mean([u["efficiency"][component] for u in recent_usage])
            for component in ["context", "system", "instruction", "response"]
        }

        # Update adjustment factors
        for component, efficiency in avg_efficiency.items():
            if efficiency < 0.7:  # Low efficiency
                self.adjustment_factors[component] *= 0.9
            elif efficiency > 0.9:  # High efficiency
                self.adjustment_factors[component] *= 1.1

    def _calculate_average_usage(self) -> Dict[str, float]:
        """Calculate average usage by component.

        Returns:
            Dict[str, float]: Average usage statistics.
        """
        if not self.usage_history:
            return {}

        components: List[str] = ["context", "system", "instruction", "response"]
        return {
            component: np.mean(
                [
                    u["actual_usage"].get(component, 0)
                    for u in self.usage_history
                    if "actual_usage" in u
                ]
            )
            for component in components
        }

    def _calculate_efficiency_metrics(self) -> Dict[str, float]:
        """Calculate efficiency metrics.

        Returns:
            Dict[str, float]: Efficiency metrics.
        """
        if not self.usage_history:
            return {}

        recent_usage: List[Dict[str, Any]] = [
            u for u in self.usage_history[-10:] if "actual_usage" in u
        ]

        if not recent_usage:
            return {}

        components: List[str] = ["context", "system", "instruction", "response"]
        return {
            component: np.mean(
                [
                    u["actual_usage"].get(component, 0)
                    / u["allocation"]["metadata"]["component_budgets"].get(component, 1)
                    for u in recent_usage
                ]
            )
            for component in components
        }

    def _estimate_cost(self, total_tokens: int, token_cost: float) -> float:
        """Estimate cost for token usage.

        Args:
            total_tokens (int): Total number of tokens.
            token_cost (float): Cost per token.

        Returns:
            float: Estimated cost.
        """
        return total_tokens * token_cost
