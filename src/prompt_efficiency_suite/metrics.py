from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

class EfficiencyMetrics(BaseModel):
    """Model for storing efficiency metrics."""
    prompt_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    token_count: int
    cost: float
    latency: float
    success_rate: float
    quality_score: float
    metadata: Dict[str, Union[str, int, float]] = Field(default_factory=dict)

class MetricsTracker:
    """Tracks and stores efficiency metrics for prompts."""
    
    def __init__(self):
        """Initialize the metrics tracker."""
        self.metrics_history: List[EfficiencyMetrics] = []
    
    def add_metrics(self, metrics: EfficiencyMetrics) -> None:
        """Add new metrics to the history.
        
        Args:
            metrics: The efficiency metrics to add
        """
        self.metrics_history.append(metrics)
    
    def get_metrics_by_id(self, prompt_id: str) -> List[EfficiencyMetrics]:
        """Get all metrics for a specific prompt ID.
        
        Args:
            prompt_id: The ID of the prompt to get metrics for
            
        Returns:
            List of EfficiencyMetrics for the specified prompt
        """
        return [m for m in self.metrics_history if m.prompt_id == prompt_id]
    
    def get_average_metrics(self) -> Dict[str, float]:
        """Calculate average metrics across all recorded data.
        
        Returns:
            Dictionary containing average values for each metric
        """
        if not self.metrics_history:
            return {}
        
        total_metrics = len(self.metrics_history)
        return {
            "avg_token_count": sum(m.token_count for m in self.metrics_history) / total_metrics,
            "avg_cost": sum(m.cost for m in self.metrics_history) / total_metrics,
            "avg_latency": sum(m.latency for m in self.metrics_history) / total_metrics,
            "avg_success_rate": sum(m.success_rate for m in self.metrics_history) / total_metrics,
            "avg_quality_score": sum(m.quality_score for m in self.metrics_history) / total_metrics
        }
    
    def get_metrics_summary(self) -> Dict[str, Union[float, int]]:
        """Get a summary of all metrics.
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.metrics_history:
            return {}
        
        return {
            "total_prompts": len(self.metrics_history),
            "total_tokens": sum(m.token_count for m in self.metrics_history),
            "total_cost": sum(m.cost for m in self.metrics_history),
            "min_latency": min(m.latency for m in self.metrics_history),
            "max_latency": max(m.latency for m in self.metrics_history),
            "avg_success_rate": sum(m.success_rate for m in self.metrics_history) / len(self.metrics_history)
        } 