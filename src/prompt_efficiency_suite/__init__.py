"""
Prompt Efficiency Suite - A toolkit for optimizing and managing prompts.
"""

from .adaptive_budgeting import AdaptiveBudgetManager, BudgetAllocation
from .analyzer import PromptAnalysis, PromptAnalyzer
from .base_compressor import BaseCompressor, CompressionResult
from .bulk_optimizer import BulkOptimizer
from .macro_manager import MacroDefinition, MacroManager
from .macro_suggester import MacroSuggester
from .metrics import EfficiencyMetrics, MetricsTracker
from .repository_scanner import PromptLocation, RepositoryScanner
from .utils import (
    calculate_token_estimate,
    extract_parameters,
    format_size,
    format_timestamp,
    load_config,
    merge_configs,
    sanitize_filename,
    save_config,
    validate_prompt,
)

__version__ = "0.1.0"

__all__ = [
    # Core components
    "BaseCompressor",
    "CompressionResult",
    "PromptAnalyzer",
    "PromptAnalysis",
    "MetricsTracker",
    "EfficiencyMetrics",
    "BulkOptimizer",
    "MacroManager",
    "MacroDefinition",
    "MacroSuggester",
    "RepositoryScanner",
    "PromptLocation",
    "AdaptiveBudgetManager",
    "BudgetAllocation",
    # Utility functions
    "load_config",
    "save_config",
    "format_timestamp",
    "sanitize_filename",
    "format_size",
    "calculate_token_estimate",
    "validate_prompt",
    "extract_parameters",
    "merge_configs",
    # Version
    "__version__",
]
