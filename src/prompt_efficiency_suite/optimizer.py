"""
Core optimizer module for prompt optimization.
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
import re
import json
from pathlib import Path
import logging
from collections import defaultdict

from .analyzer import PromptAnalyzer
from .code_aware_compressor import CodeAwareCompressor
from .macro_suggester import MacroSuggester

logger = logging.getLogger(__name__)

@dataclass
class OptimizationConfig:
    """Configuration for prompt optimization."""
    max_length: int = 4096
    min_clarity: float = 0.8
    min_completeness: float = 0.8
    min_consistency: float = 0.8
    min_efficiency: float = 0.8
    preserve_code: bool = True
    preserve_examples: bool = True
    preserve_context: bool = True
    metadata: Dict[str, any] = field(default_factory=dict)

@dataclass
class OptimizationResult:
    """Result of prompt optimization."""
    original_prompt: str
    optimized_prompt: str
    clarity_score: float
    completeness_score: float
    consistency_score: float
    efficiency_score: float
    length_reduction: float
    optimization_time: float
    metadata: Dict[str, any] = field(default_factory=dict)

class PromptOptimizer:
    """Class for optimizing prompts."""

    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the optimizer.
        
        Args:
            config (Optional[OptimizationConfig]): Configuration for optimization.
        """
        self.config = config or OptimizationConfig()
        self.optimization_history: List[OptimizationResult] = []
        self._load_optimization_patterns()

    def optimize(
        self,
        prompt: str,
        optimization_params: Optional[Dict[str, any]] = None
    ) -> OptimizationResult:
        """Optimize a prompt.
        
        Args:
            prompt (str): Prompt to optimize.
            optimization_params (Optional[Dict[str, any]]): Additional optimization parameters.
            
        Returns:
            OptimizationResult: Result of optimization.
        """
        params = optimization_params or {}
        config = OptimizationConfig(**{**self.config.__dict__, **params})

        # Analyze prompt
        clarity = self._calculate_clarity(prompt)
        completeness = self._calculate_completeness(prompt)
        consistency = self._calculate_consistency(prompt)
        efficiency = self._calculate_efficiency(prompt)

        # Apply optimizations
        optimized = self._optimize_prompt(prompt, config)

        # Calculate metrics
        result = OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=optimized,
            clarity_score=clarity,
            completeness_score=completeness,
            consistency_score=consistency,
            efficiency_score=efficiency,
            length_reduction=1 - (len(optimized) / len(prompt)),
            optimization_time=0.0,  # TODO: Add timing
            metadata={}
        )

        self.optimization_history.append(result)
        return result

    def get_optimization_stats(self) -> Dict[str, any]:
        """Get statistics about optimizations.
        
        Returns:
            Dict[str, any]: Optimization statistics.
        """
        if not self.optimization_history:
            return {}

        return {
            "total_optimizations": len(self.optimization_history),
            "avg_length_reduction": sum(r.length_reduction for r in self.optimization_history) / len(self.optimization_history),
            "avg_clarity": sum(r.clarity_score for r in self.optimization_history) / len(self.optimization_history),
            "avg_completeness": sum(r.completeness_score for r in self.optimization_history) / len(self.optimization_history),
            "avg_consistency": sum(r.consistency_score for r in self.optimization_history) / len(self.optimization_history),
            "avg_efficiency": sum(r.efficiency_score for r in self.optimization_history) / len(self.optimization_history),
        }

    def _load_optimization_patterns(self) -> None:
        """Load optimization patterns."""
        self.patterns = {
            "redundant_phrases": [
                r"\bas (you |we )?mentioned( earlier| before| previously)?\b",
                r"\blike I said( earlier| before| previously)?\b",
                r"\bas (I |we )?discussed( earlier| before| previously)?\b",
                r"\bin other words\b",
                r"\bbasically\b",
                r"\bessentially\b",
            ],
            "filler_words": [
                r"\bvery\b",
                r"\breally\b",
                r"\bquite\b",
                r"\bjust\b",
                r"\bsimply\b",
                r"\bactually\b",
            ],
            "code_blocks": [
                r"```[\s\S]*?```",
                r"`[^`]+`",
            ],
            "examples": [
                r"Example:[\s\S]*?(?=\n\n|\Z)",
                r"For example:[\s\S]*?(?=\n\n|\Z)",
            ],
        }

    def _calculate_clarity(self, prompt: str) -> float:
        """Calculate clarity score."""
        # TODO: Implement more sophisticated clarity calculation
        return 0.9

    def _calculate_completeness(self, prompt: str) -> float:
        """Calculate completeness score."""
        # TODO: Implement more sophisticated completeness calculation
        return 0.9

    def _calculate_consistency(self, prompt: str) -> float:
        """Calculate consistency score."""
        # TODO: Implement more sophisticated consistency calculation
        return 0.9

    def _calculate_efficiency(self, prompt: str) -> float:
        """Calculate efficiency score."""
        # TODO: Implement more sophisticated efficiency calculation
        return 0.9

    def _optimize_prompt(self, prompt: str, config: OptimizationConfig) -> str:
        """Optimize a prompt."""
        optimized = prompt

        # Preserve code blocks and examples if configured
        preserved_sections = []
        if config.preserve_code:
            preserved_sections.extend(self.patterns["code_blocks"])
        if config.preserve_examples:
            preserved_sections.extend(self.patterns["examples"])

        # Extract preserved sections
        preserved = {}
        for i, pattern in enumerate(preserved_sections):
            for match in re.finditer(pattern, optimized):
                key = f"PRESERVED_{i}_{len(preserved)}"
                preserved[key] = match.group(0)
                optimized = optimized.replace(match.group(0), key)

        # Remove redundant phrases
        for pattern in self.patterns["redundant_phrases"]:
            optimized = re.sub(pattern, "", optimized)

        # Remove filler words
        for pattern in self.patterns["filler_words"]:
            optimized = re.sub(pattern, "", optimized)

        # Clean up whitespace
        optimized = re.sub(r"\s+", " ", optimized)
        optimized = re.sub(r"\n\s*\n\s*\n", "\n\n", optimized)
        optimized = optimized.strip()

        # Restore preserved sections
        for key, value in preserved.items():
            optimized = optimized.replace(key, value)

        return optimized

class Optimizer:
    """A class for optimizing prompts."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Optimizer.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.analyzer = PromptAnalyzer(config)
        self.compressor = CodeAwareCompressor(config)
        self.macro_suggester = MacroSuggester(config)
        self.optimization_history: List[OptimizationResult] = []
        
    def optimize(
        self,
        prompt: str,
        optimization_params: Optional[Dict[str, Any]] = None
    ) -> OptimizationResult:
        """Optimize a prompt.
        
        Args:
            prompt (str): Prompt to optimize.
            optimization_params (Optional[Dict[str, Any]]): Optimization parameters.
            
        Returns:
            OptimizationResult: Optimization result.
        """
        params = optimization_params or {}
        
        # Analyze prompt
        analysis_result = self.analyzer.analyze(prompt)
        
        # Compress prompt
        compression_result = self.compressor.compress(prompt)
        
        # Suggest macros
        macro_result = self.macro_suggester.suggest_macros(prompt)
        
        # Combine optimizations
        optimized_prompt = self._combine_optimizations(
            prompt,
            analysis_result,
            compression_result,
            macro_result,
            params
        )
        
        # Calculate optimization stats
        stats = self._calculate_optimization_stats(
            prompt,
            optimized_prompt,
            analysis_result,
            compression_result,
            macro_result
        )
        
        # Create result
        result = OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=optimized_prompt,
            clarity_score=stats['improvements']['clarity'],
            completeness_score=stats['improvements']['completeness'],
            consistency_score=stats['improvements']['consistency'],
            efficiency_score=stats['improvements']['efficiency'],
            length_reduction=stats['length_reduction'],
            optimization_time=0.0,  # TODO: Add timing
            metadata={
                'optimization_params': params,
                'analysis_metrics': analysis_result.metrics.__dict__,
                'compression_ratio': compression_result.compression_ratio,
                'suggested_macros': [
                    macro.__dict__ for macro in macro_result.suggested_macros
                ]
            }
        )
        
        self.optimization_history.append(result)
        return result
        
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get statistics about optimizations.
        
        Returns:
            Dict[str, Any]: Optimization statistics.
        """
        if not self.optimization_history:
            return {}
            
        # Calculate average improvements
        total_improvements = defaultdict(float)
        for result in self.optimization_history:
            stats = result.optimization_stats
            for metric, value in stats['improvements'].items():
                total_improvements[metric] += value
                
        avg_improvements = {
            metric: value / len(self.optimization_history)
            for metric, value in total_improvements.items()
        }
        
        return {
            'total_optimizations': len(self.optimization_history),
            'average_improvements': avg_improvements,
            'optimization_types': self._get_optimization_type_stats()
        }
        
    def export_results(self, output_path: Path) -> None:
        """Export optimization results to a file.
        
        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            'statistics': self.get_optimization_stats(),
            'results': [
                {
                    'original_prompt': result.original_prompt,
                    'optimized_prompt': result.optimized_prompt,
                    'optimization_stats': result.optimization_stats,
                    'metadata': result.metadata
                }
                for result in self.optimization_history
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2)
            
    def _combine_optimizations(
        self,
        prompt: str,
        analysis_result: Any,
        compression_result: Any,
        macro_result: Any,
        params: Dict[str, Any]
    ) -> str:
        """Combine different optimizations.
        
        Args:
            prompt (str): Original prompt.
            analysis_result (Any): Analysis result.
            compression_result (Any): Compression result.
            macro_result (Any): Macro suggestion result.
            params (Dict[str, Any]): Optimization parameters.
            
        Returns:
            str: Optimized prompt.
        """
        # Start with compressed prompt
        optimized = compression_result.compressed_prompt
        
        # Apply macro suggestions if enabled
        if params.get('apply_macros', True):
            for macro in macro_result.suggested_macros:
                optimized = self._apply_macro(optimized, macro)
                
        # Apply analysis-based improvements
        if params.get('apply_analysis', True):
            optimized = self._apply_analysis_improvements(
                optimized,
                analysis_result.metrics
            )
            
        return optimized
        
    def _apply_macro(self, prompt: str, macro: Any) -> str:
        """Apply a macro to the prompt.
        
        Args:
            prompt (str): Prompt to modify.
            macro (Any): Macro to apply.
            
        Returns:
            str: Modified prompt.
        """
        # This is a placeholder implementation
        # In a real implementation, this would:
        # 1. Find instances of the pattern
        # 2. Replace them with the macro
        # 3. Handle any necessary context
        return prompt
        
    def _apply_analysis_improvements(
        self,
        prompt: str,
        metrics: Any
    ) -> str:
        """Apply improvements based on analysis metrics.
        
        Args:
            prompt (str): Prompt to improve.
            metrics (Any): Analysis metrics.
            
        Returns:
            str: Improved prompt.
        """
        # This is a placeholder implementation
        # In a real implementation, this would:
        # 1. Check metrics for areas of improvement
        # 2. Apply specific improvements based on metrics
        # 3. Maintain prompt coherence
        return prompt
        
    def _calculate_optimization_stats(
        self,
        original_prompt: str,
        optimized_prompt: str,
        analysis_result: Any,
        compression_result: Any,
        macro_result: Any
    ) -> Dict[str, Any]:
        """Calculate optimization statistics.
        
        Args:
            original_prompt (str): Original prompt.
            optimized_prompt (str): Optimized prompt.
            analysis_result (Any): Analysis result.
            compression_result (Any): Compression result.
            macro_result (Any): Macro suggestion result.
            
        Returns:
            Dict[str, Any]: Optimization statistics.
        """
        # Calculate basic stats
        original_length = len(original_prompt)
        optimized_length = len(optimized_prompt)
        length_reduction = 1 - (optimized_length / original_length)
        
        # Calculate improvements
        improvements = {
            'length': length_reduction,
            'clarity': analysis_result.metrics.clarity_score,
            'completeness': analysis_result.metrics.completeness_score,
            'consistency': analysis_result.metrics.consistency_score,
            'efficiency': analysis_result.metrics.efficiency_score
        }
        
        return {
            'original_length': original_length,
            'optimized_length': optimized_length,
            'length_reduction': length_reduction,
            'improvements': improvements,
            'applied_macros': len(macro_result.suggested_macros)
        }
        
    def _get_optimization_type_stats(self) -> Dict[str, int]:
        """Get statistics about optimization types.
        
        Returns:
            Dict[str, int]: Optimization type statistics.
        """
        stats = defaultdict(int)
        
        for result in self.optimization_history:
            # Count applied optimizations
            if result.metadata.get('analysis_metrics'):
                stats['analysis'] += 1
            if result.metadata.get('compression_ratio'):
                stats['compression'] += 1
            if result.metadata.get('suggested_macros'):
                stats['macros'] += 1
                
        return dict(stats)

class BatchOptimizer:
    """Class for optimizing multiple prompts in batch."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the batch optimizer.
        
        Args:
            config (Optional[OptimizationConfig]): Configuration for optimization.
        """
        self.config = config or OptimizationConfig()
        self.optimizer = PromptOptimizer(config)
        self.batch_history: List[List[OptimizationResult]] = []
        
    def optimize_batch(
        self,
        prompts: List[str],
        optimization_params: Optional[Dict[str, Any]] = None
    ) -> List[OptimizationResult]:
        """Optimize a batch of prompts.
        
        Args:
            prompts (List[str]): List of prompts to optimize.
            optimization_params (Optional[Dict[str, Any]]): Additional optimization parameters.
            
        Returns:
            List[OptimizationResult]: List of optimization results.
        """
        results = []
        for prompt in prompts:
            result = self.optimizer.optimize(prompt, optimization_params)
            results.append(result)
            
        self.batch_history.append(results)
        return results
        
    def get_batch_stats(self) -> Dict[str, Any]:
        """Get statistics about batch optimizations.
        
        Returns:
            Dict[str, Any]: Batch optimization statistics.
        """
        if not self.batch_history:
            return {}
            
        total_batches = len(self.batch_history)
        total_prompts = sum(len(batch) for batch in self.batch_history)
        avg_batch_size = total_prompts / total_batches
        
        all_results = [result for batch in self.batch_history for result in batch]
        avg_length_reduction = sum(r.length_reduction for r in all_results) / len(all_results)
        avg_clarity = sum(r.clarity_score for r in all_results) / len(all_results)
        avg_completeness = sum(r.completeness_score for r in all_results) / len(all_results)
        avg_consistency = sum(r.consistency_score for r in all_results) / len(all_results)
        avg_efficiency = sum(r.efficiency_score for r in all_results) / len(all_results)
        
        return {
            "total_batches": total_batches,
            "total_prompts": total_prompts,
            "avg_batch_size": avg_batch_size,
            "avg_length_reduction": avg_length_reduction,
            "avg_clarity": avg_clarity,
            "avg_completeness": avg_completeness,
            "avg_consistency": avg_consistency,
            "avg_efficiency": avg_efficiency
        }
        
    def export_batch_results(self, output_path: Path) -> None:
        """Export batch optimization results to a file.
        
        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            "batch_history": [
                [
                    {
                        "original_prompt": r.original_prompt,
                        "optimized_prompt": r.optimized_prompt,
                        "clarity_score": r.clarity_score,
                        "completeness_score": r.completeness_score,
                        "consistency_score": r.consistency_score,
                        "efficiency_score": r.efficiency_score,
                        "length_reduction": r.length_reduction,
                        "optimization_time": r.optimization_time,
                        "metadata": r.metadata
                    }
                    for r in batch
                ]
                for batch in self.batch_history
            ],
            "stats": self.get_batch_stats()
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2) 