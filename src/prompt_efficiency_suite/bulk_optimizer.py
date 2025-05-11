import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Union

from .analyzer import PromptAnalysis, PromptAnalyzer
from .base_compressor import BaseCompressor, CompressionResult
from .metrics import EfficiencyMetrics, MetricsTracker


class BulkOptimizer:
    """Optimizes multiple prompts in bulk with parallel processing."""

    def __init__(
        self,
        compressor: BaseCompressor,
        analyzer: PromptAnalyzer,
        metrics_tracker: MetricsTracker,
        max_workers: int = 4,
    ):
        """Initialize the bulk optimizer.

        Args:
            compressor: The compressor to use for optimization
            analyzer: The analyzer to use for quality assessment
            metrics_tracker: The metrics tracker to use
            max_workers: Maximum number of parallel workers
        """
        self.compressor = compressor
        self.analyzer = analyzer
        self.metrics_tracker = metrics_tracker
        self.max_workers = max_workers
        self.executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=max_workers)

    async def optimize_batch(
        self,
        prompts: List[str],
        target_ratio: Optional[float] = None,
        min_quality_score: float = 0.7,
    ) -> List[Dict[str, Union[CompressionResult, PromptAnalysis]]]:
        """Optimize a batch of prompts.

        Args:
            prompts: List of prompts to optimize
            target_ratio: Optional target compression ratio
            min_quality_score: Minimum quality score to accept

        Returns:
            List of dictionaries containing compression and analysis results
        """
        # Process prompts in parallel
        tasks: List[asyncio.Task] = []
        for prompt in prompts:
            task = asyncio.create_task(
                self._optimize_single(prompt, target_ratio, min_quality_score)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

    async def _optimize_single(
        self, prompt: str, target_ratio: Optional[float], min_quality_score: float
    ) -> Optional[Dict[str, Union[CompressionResult, PromptAnalysis]]]:
        """Optimize a single prompt.

        Args:
            prompt: The prompt to optimize
            target_ratio: Optional target compression ratio
            min_quality_score: Minimum quality score to accept

        Returns:
            Dictionary containing compression and analysis results, or None if optimization failed
        """
        try:
            # Compress the prompt
            compression_result = await self.compressor.compress(prompt, target_ratio)

            # Analyze the compressed result
            analysis = self.analyzer.analyze(compression_result.compressed_text)

            # Track metrics
            metrics = EfficiencyMetrics(
                prompt_id=hash(prompt),
                token_count=compression_result.compressed_tokens,
                cost=compression_result.compressed_tokens
                * 0.0001,  # Example cost calculation
                latency=0.0,  # Would be measured in real implementation
                success_rate=(
                    1.0 if analysis.quality_score >= min_quality_score else 0.0
                ),
                quality_score=analysis.quality_score,
            )
            self.metrics_tracker.add_metrics(metrics)

            # Return results if quality threshold is met
            if analysis.quality_score >= min_quality_score:
                return {
                    "compression": compression_result,
                    "analysis": analysis,
                    "metrics": metrics,
                }
            return None

        except Exception as e:
            print(f"Error optimizing prompt: {str(e)}")
            return None

    def get_optimization_stats(self) -> Dict[str, Union[float, int]]:
        """Get statistics about the optimization process.

        Returns:
            Dictionary containing optimization statistics
        """
        return self.metrics_tracker.get_metrics_summary()
