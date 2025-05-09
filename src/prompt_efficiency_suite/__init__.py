"""
Prompt Efficiency Suite - A toolkit for optimizing and managing prompts.
"""

from .base_compressor import BaseCompressor, CompressionResult
from .analyzer import PromptAnalyzer, PromptAnalysis
from .metrics import MetricsTracker, EfficiencyMetrics
from .bulk_optimizer import BulkOptimizer
from .macro_manager import MacroManager, MacroDefinition
from .macro_suggester import MacroSuggester
from .repository_scanner import RepositoryScanner, PromptLocation
from .adaptive_budgeting import AdaptiveBudgetManager, BudgetAllocation
from .utils import (
    load_config,
    save_config,
    format_timestamp,
    sanitize_filename,
    format_size,
    calculate_token_estimate,
    validate_prompt,
    extract_parameters,
    merge_configs
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
    "__version__"
] 