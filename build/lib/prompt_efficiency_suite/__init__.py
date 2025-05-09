"""
Prompt Efficiency Suite - A comprehensive toolkit for optimizing and managing prompts.
"""

from .batch_optimizer import BatchOptimizer
from .multimodal_compressor import MultimodalCompressor
from .prompt_optimizer import PromptOptimizer
from .token_counter import TokenCounter
from .quality_analyzer import QualityAnalyzer
from .cost_estimator import CostEstimator

__version__ = "1.0.0"
__author__ = "Prompt Efficiency Suite Team"
__email__ = "support@promptefficiencysuite.com"

__all__ = [
    "BatchOptimizer",
    "MultimodalCompressor",
    "PromptOptimizer",
    "TokenCounter",
    "QualityAnalyzer",
    "CostEstimator"
] 