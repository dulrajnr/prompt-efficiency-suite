"""
Orchestrator - A module for coordinating prompt optimization components.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .analyzer import PromptAnalyzer
from .optimizer import PromptOptimizer
from .model_translator import ModelTranslator, ModelType
from .code_aware_compressor import CodeAwareCompressor
from .macro_suggester import MacroSuggester

@dataclass
class ModelPerformance:
    """Performance metrics for a model."""
    model_type: ModelType
    response_time: float
    token_count: int
    cost: float
    success_rate: float
    metadata: Dict[str, any] = field(default_factory=dict)

@dataclass
class PerformanceMetrics:
    """Performance metrics for prompt optimization."""
    clarity_improvement: float
    completeness_improvement: float
    consistency_improvement: float
    efficiency_improvement: float
    length_reduction: float
    execution_time: float
    metadata: Dict[str, any] = field(default_factory=dict)

@dataclass
class OrchestrationResult:
    """Result of orchestrated optimization."""
    original_prompt: str
    optimized_prompt: str
    analysis_result: Dict[str, any]
    optimization_result: Dict[str, any]
    translation_result: Optional[Dict[str, any]]
    performance_metrics: PerformanceMetrics
    metadata: Dict[str, any] = field(default_factory=dict)

class PromptOrchestrator:
    """Class for orchestrating prompt optimization."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.analyzer = PromptAnalyzer()
        self.optimizer = PromptOptimizer()
        self.translator = ModelTranslator()
        self.compressor = CodeAwareCompressor()
        self.macro_suggester = MacroSuggester()
        self.optimization_history: List[OrchestrationResult] = []

    def optimize_prompt(
        self,
        prompt: str,
        target_model: Optional[Union[str, ModelType]] = None,
        optimization_params: Optional[Dict[str, any]] = None
    ) -> OrchestrationResult:
        """Optimize a prompt.
        
        Args:
            prompt (str): Prompt to optimize.
            target_model (Optional[Union[str, ModelType]]): Target model for optimization.
            optimization_params (Optional[Dict[str, any]]): Additional optimization parameters.
            
        Returns:
            OrchestrationResult: Result of optimization.
        """
        params = optimization_params or {}

        # Run analysis and optimization in parallel
        with ThreadPoolExecutor() as executor:
            analysis_future = executor.submit(self.analyzer.analyze, prompt)
            optimization_future = executor.submit(self.optimizer.optimize, prompt, params)

            analysis_result = analysis_future.result()
            optimization_result = optimization_future.result()

        # Translate if target model is specified
        translation_result = None
        if target_model:
            translation_result = self.translator.translate(
                optimization_result.optimized_prompt,
                source_format=ModelType.OPENAI,  # Assuming OpenAI format by default
                target_format=target_model
            )

        # Calculate performance metrics
        metrics = PerformanceMetrics(
            clarity_improvement=optimization_result.clarity_score - 0.5,  # Assuming baseline of 0.5
            completeness_improvement=optimization_result.completeness_score - 0.5,
            consistency_improvement=optimization_result.consistency_score - 0.5,
            efficiency_improvement=optimization_result.efficiency_score - 0.5,
            length_reduction=optimization_result.length_reduction,
            execution_time=optimization_result.optimization_time,
            metadata={}
        )

        result = OrchestrationResult(
            original_prompt=prompt,
            optimized_prompt=optimization_result.optimized_prompt,
            analysis_result=analysis_result.__dict__,
            optimization_result=optimization_result.__dict__,
            translation_result=translation_result.__dict__ if translation_result else None,
            performance_metrics=metrics,
            metadata={"optimization_params": params}
        )

        self.optimization_history.append(result)
        return result

    def optimize_batch(
        self,
        prompts: List[str],
        target_model: Optional[Union[str, ModelType]] = None,
        optimization_params: Optional[Dict[str, any]] = None,
        max_workers: int = 4
    ) -> List[OrchestrationResult]:
        """Optimize a batch of prompts.
        
        Args:
            prompts (List[str]): Prompts to optimize.
            target_model (Optional[Union[str, ModelType]]): Target model for optimization.
            optimization_params (Optional[Dict[str, any]]): Additional optimization parameters.
            max_workers (int): Maximum number of worker threads.
            
        Returns:
            List[OrchestrationResult]: Results of optimization.
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    self.optimize_prompt,
                    prompt,
                    target_model,
                    optimization_params
                )
                for prompt in prompts
            ]
            return [future.result() for future in futures]

    def get_optimization_stats(self) -> Dict[str, any]:
        """Get statistics about optimizations.
        
        Returns:
            Dict[str, any]: Optimization statistics.
        """
        if not self.optimization_history:
            return {}

        return {
            "total_optimizations": len(self.optimization_history),
            "avg_clarity_improvement": sum(r.performance_metrics.clarity_improvement for r in self.optimization_history) / len(self.optimization_history),
            "avg_completeness_improvement": sum(r.performance_metrics.completeness_improvement for r in self.optimization_history) / len(self.optimization_history),
            "avg_consistency_improvement": sum(r.performance_metrics.consistency_improvement for r in self.optimization_history) / len(self.optimization_history),
            "avg_efficiency_improvement": sum(r.performance_metrics.efficiency_improvement for r in self.optimization_history) / len(self.optimization_history),
            "avg_length_reduction": sum(r.performance_metrics.length_reduction for r in self.optimization_history) / len(self.optimization_history),
            "avg_execution_time": sum(r.performance_metrics.execution_time for r in self.optimization_history) / len(self.optimization_history)
        }

    def clear_history(self) -> None:
        """Clear optimization history."""
        self.optimization_history.clear()
        self.analyzer.analysis_history.clear()
        self.optimizer.optimization_history.clear()
        self.translator.translation_history.clear()
        self.macro_suggester.suggestion_history.clear()

    def export_results(self, output_path: Path) -> None:
        """Export optimization results to a file.
        
        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            'statistics': self.get_optimization_stats(),
            'results': [
                {
                    'prompt': result.original_prompt,
                    'optimized_prompt': result.optimized_prompt,
                    'analysis_metrics': result.analysis_result,
                    'optimization_stats': result.optimization_result,
                    'translation_info': (
                        {
                            'source_format': result.translation_result['source_format'],
                            'target_format': result.translation_result['target_format']
                        }
                        if result.translation_result
                        else None
                    ),
                    'performance_metrics': result.performance_metrics.__dict__,
                    'metadata': result.metadata
                }
                for result in self.optimization_history
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2) 