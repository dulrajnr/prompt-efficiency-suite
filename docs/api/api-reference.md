# API Reference

This document provides detailed API reference for the Prompt Efficiency Suite.

## Core Classes

### BaseCompressor

```python
class BaseCompressor:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize the compressor.

        Args:
            model_name: The model to use for token counting
        """
        pass

    async def compress(
        self,
        text: str,
        target_ratio: Optional[float] = None
    ) -> CompressionResult:
        """Compress the input text.

        Args:
            text: The text to compress
            target_ratio: Optional target compression ratio (0.0 to 1.0)

        Returns:
            CompressionResult containing compression metrics and results
        """
        pass

    async def batch_compress(
        self,
        texts: List[str],
        target_ratio: Optional[float] = None
    ) -> List[CompressionResult]:
        """Compress multiple texts in batch.

        Args:
            texts: List of texts to compress
            target_ratio: Optional target compression ratio (0.0 to 1.0)

        Returns:
            List of CompressionResult objects
        """
        pass
```

### PromptAnalyzer

```python
class PromptAnalyzer:
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the analyzer.

        Args:
            model_name: The spaCy model to use for analysis
        """
        pass

    def analyze(self, text: str) -> PromptAnalysis:
        """Analyze a single prompt.

        Args:
            text: The prompt text to analyze

        Returns:
            PromptAnalysis containing various metrics and insights
        """
        pass

    def batch_analyze(self, texts: List[str]) -> List[PromptAnalysis]:
        """Analyze multiple prompts in batch.

        Args:
            texts: List of prompt texts to analyze

        Returns:
            List of PromptAnalysis objects
        """
        pass
```

### MetricsTracker

```python
class MetricsTracker:
    def __init__(self):
        """Initialize the metrics tracker."""
        pass

    def add_metrics(self, metrics: EfficiencyMetrics) -> None:
        """Add new metrics to the history.

        Args:
            metrics: The efficiency metrics to add
        """
        pass

    def get_metrics_by_id(self, prompt_id: str) -> List[EfficiencyMetrics]:
        """Get all metrics for a specific prompt ID.

        Args:
            prompt_id: The ID of the prompt to get metrics for

        Returns:
            List of EfficiencyMetrics for the specified prompt
        """
        pass
```

### BulkOptimizer

```python
class BulkOptimizer:
    def __init__(
        self,
        compressor: BaseCompressor,
        analyzer: PromptAnalyzer,
        metrics_tracker: MetricsTracker,
        max_workers: int = 4
    ):
        """Initialize the bulk optimizer.

        Args:
            compressor: The compressor to use
            analyzer: The analyzer to use
            metrics_tracker: The metrics tracker to use
            max_workers: Maximum number of parallel workers
        """
        pass

    async def optimize_batch(
        self,
        prompts: List[str],
        target_ratio: Optional[float] = None,
        min_quality_score: float = 0.7
    ) -> List[Dict[str, Union[CompressionResult, PromptAnalysis]]]:
        """Optimize a batch of prompts.

        Args:
            prompts: List of prompts to optimize
            target_ratio: Optional target compression ratio
            min_quality_score: Minimum quality score to accept

        Returns:
            List of dictionaries containing compression and analysis results
        """
        pass
```

### MacroManager

```python
class MacroManager:
    def __init__(self):
        """Initialize the macro manager."""
        pass

    def register_macro(self, macro: MacroDefinition) -> None:
        """Register a new macro.

        Args:
            macro: The macro definition to register
        """
        pass

    def expand_macro(
        self,
        name: str,
        parameters: Dict[str, str]
    ) -> Optional[str]:
        """Expand a macro with the given parameters.

        Args:
            name: The name of the macro to expand
            parameters: Dictionary of parameter values

        Returns:
            The expanded macro text if successful, None otherwise
        """
        pass
```

### RepositoryScanner

```python
class RepositoryScanner:
    def __init__(self, max_workers: int = 4):
        """Initialize the repository scanner.

        Args:
            max_workers: Maximum number of parallel workers
        """
        pass

    def scan_repository(self, repo_path: str) -> List[PromptLocation]:
        """Scan a repository for prompts.

        Args:
            repo_path: Path to the repository

        Returns:
            List of found prompt locations
        """
        pass
```

### AdaptiveBudgetManager

```python
class AdaptiveBudgetManager:
    def __init__(
        self,
        initial_budget: int,
        allocation_period: timedelta = timedelta(days=1),
        min_budget: int = 1000,
        max_budget: int = 1000000
    ):
        """Initialize the budget manager.

        Args:
            initial_budget: Initial token budget
            allocation_period: Time period for budget allocation
            min_budget: Minimum allowed budget
            max_budget: Maximum allowed budget
        """
        pass

    def record_usage(self, metrics: EfficiencyMetrics) -> None:
        """Record token usage.

        Args:
            metrics: The efficiency metrics to record
        """
        pass

    def get_remaining_budget(self) -> int:
        """Get the remaining budget.

        Returns:
            Remaining token budget
        """
        pass
```

## Data Models

### CompressionResult

```python
class CompressionResult(BaseModel):
    """Model for storing compression results."""
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    compressed_text: str
    metadata: Dict[str, Union[str, int, float]]
```

### PromptAnalysis

```python
class PromptAnalysis(BaseModel):
    """Model for storing prompt analysis results."""
    token_count: int
    word_count: int
    sentence_count: int
    readability_score: float
    complexity_score: float
    redundancy_score: float
    key_phrases: List[str]
    metadata: Dict[str, Union[str, int, float]]
```

### EfficiencyMetrics

```python
class EfficiencyMetrics(BaseModel):
    """Model for storing efficiency metrics."""
    prompt_id: str
    timestamp: datetime
    token_count: int
    cost: float
    latency: float
    success_rate: float
    quality_score: float
    metadata: Dict[str, Union[str, int, float]]
```

### MacroDefinition

```python
class MacroDefinition(BaseModel):
    """Model for storing macro definitions."""
    name: str
    template: str
    description: str
    parameters: List[str]
    metadata: Dict[str, Union[str, int, float]]
```

### PromptLocation

```python
class PromptLocation:
    """Data class for storing prompt location information."""
    file_path: str
    line_number: int
    context: str
    prompt_text: str
    language: str
```

## Utility Functions

### Configuration

```python
def load_config(config_path: str) -> Dict:
    """Load configuration from a file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration
    """
    pass

def save_config(config: Dict, config_path: str) -> bool:
    """Save configuration to a file.

    Args:
        config: Configuration dictionary to save
        config_path: Path to save the configuration file

    Returns:
        True if successful, False otherwise
    """
    pass
```

### Token Management

```python
def calculate_token_estimate(
    text: str,
    model_name: str = "gpt-3.5-turbo"
) -> int:
    """Estimate the number of tokens in a text.

    Args:
        text: The text to estimate tokens for
        model_name: The model to estimate for

    Returns:
        Estimated number of tokens
    """
    pass
```

### File Operations

```python
def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to be safe for all operating systems.

    Args:
        filename: The filename to sanitize

    Returns:
        Sanitized filename
    """
    pass

def format_size(size_bytes: int) -> str:
    """Format a size in bytes to a human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human-readable size string
    """
    pass
```

### Text Processing

```python
def validate_prompt(prompt: str) -> bool:
    """Validate a prompt for basic requirements.

    Args:
        prompt: The prompt to validate

    Returns:
        True if valid, False otherwise
    """
    pass

def extract_parameters(text: str) -> List[str]:
    """Extract parameter names from a text.

    Args:
        text: The text to extract parameters from

    Returns:
        List of parameter names
    """
    pass
```

## Error Handling

The suite uses custom exceptions for better error handling:

```python
class PromptEfficiencyError(Exception):
    """Base exception for the Prompt Efficiency Suite."""
    pass

class CompressionError(PromptEfficiencyError):
    """Exception raised for compression errors."""
    pass

class AnalysisError(PromptEfficiencyError):
    """Exception raised for analysis errors."""
    pass

class BudgetError(PromptEfficiencyError):
    """Exception raised for budget-related errors."""
    pass
```

## Type Hints

The suite uses Python type hints for better code documentation and IDE support. Common types include:

```python
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
from pathlib import Path
```

## Constants

```python
# Default values
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TARGET_RATIO = 0.5
DEFAULT_MIN_QUALITY = 0.7
DEFAULT_MAX_WORKERS = 4

# File extensions
SUPPORTED_EXTENSIONS = {
    'python': ['.py'],
    'javascript': ['.js'],
    'typescript': ['.ts', '.tsx'],
    'java': ['.java'],
    'kotlin': ['.kt']
}

# Configuration keys
CONFIG_KEYS = {
    'compressor': ['model_name', 'target_ratio', 'min_quality_score'],
    'analyzer': ['model_name', 'metrics'],
    'budget': ['initial_budget', 'allocation_period_days', 'min_budget', 'max_budget']
}
```
