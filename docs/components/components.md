# Core Components

This document details the core components of the Prompt Efficiency Suite and their usage.

## BaseCompressor

The `BaseCompressor` is the foundation for prompt compression functionality.

### Features
- Token counting
- Compression ratio calculation
- Asynchronous compression
- Batch processing

### Usage

```python
from prompt_efficiency_suite import BaseCompressor

compressor = BaseCompressor(model_name="gpt-3.5-turbo")

# Compress a single prompt
result = await compressor.compress(
    "Your prompt here",
    target_ratio=0.5
)

# Batch compress multiple prompts
results = await compressor.batch_compress(
    ["Prompt 1", "Prompt 2"],
    target_ratio=0.5
)
```

### Configuration Options
- `model_name`: The model to use for token counting
- `target_ratio`: Target compression ratio (0.0 to 1.0)
- `min_quality_score`: Minimum quality score to accept

## PromptAnalyzer

The `PromptAnalyzer` provides comprehensive prompt analysis capabilities.

### Features
- Quality metrics calculation
- Readability analysis
- Complexity assessment
- Redundancy detection

### Usage

```python
from prompt_efficiency_suite import PromptAnalyzer

analyzer = PromptAnalyzer(model_name="en_core_web_sm")

# Analyze a single prompt
analysis = analyzer.analyze("Your prompt here")

# Batch analyze multiple prompts
analyses = analyzer.batch_analyze(["Prompt 1", "Prompt 2"])

# Get analysis statistics
stats = analyzer.get_analysis_stats()
```

### Available Metrics
- Clarity score
- Completeness score
- Consistency score
- Efficiency score
- Complexity score

## MetricsTracker

The `MetricsTracker` manages and tracks efficiency metrics.

### Features
- Usage tracking
- Cost monitoring
- Performance metrics
- Historical analysis

### Usage

```python
from prompt_efficiency_suite import MetricsTracker, EfficiencyMetrics

tracker = MetricsTracker()

# Add metrics
metrics = EfficiencyMetrics(
    prompt_id="unique_id",
    token_count=100,
    cost=0.01,
    latency=0.5,
    success_rate=0.95,
    quality_score=0.85
)
tracker.add_metrics(metrics)

# Get metrics by ID
prompt_metrics = tracker.get_metrics_by_id("unique_id")

# Get average metrics
avg_metrics = tracker.get_average_metrics()
```

## BulkOptimizer

The `BulkOptimizer` handles optimization of multiple prompts efficiently.

### Features
- Parallel processing
- Quality control
- Progress tracking
- Resource management

### Usage

```python
from prompt_efficiency_suite import BulkOptimizer, BaseCompressor, PromptAnalyzer, MetricsTracker

# Initialize components
compressor = BaseCompressor()
analyzer = PromptAnalyzer()
tracker = MetricsTracker()

# Create optimizer
optimizer = BulkOptimizer(
    compressor=compressor,
    analyzer=analyzer,
    metrics_tracker=tracker,
    max_workers=4
)

# Optimize batch of prompts
results = await optimizer.optimize_batch(
    prompts=["Prompt 1", "Prompt 2"],
    target_ratio=0.5,
    min_quality_score=0.7
)
```

## MacroManager

The `MacroManager` handles prompt templates and macros.

### Features
- Template management
- Parameter handling
- Macro expansion
- Pattern matching

### Usage

```python
from prompt_efficiency_suite import MacroManager, MacroDefinition

manager = MacroManager()

# Register a macro
macro = MacroDefinition(
    name="greeting",
    template="Hello, {name}! How can I help you today?",
    description="A friendly greeting template",
    parameters=["name"]
)
manager.register_macro(macro)

# Use macros
expanded = manager.expand_macro("greeting", {"name": "Alice"})

# Find macros in text
found_macros = manager.find_macros_in_text("Use {{greeting}} here")
```

## RepositoryScanner

The `RepositoryScanner` scans code repositories for prompts.

### Features
- Multi-language support
- Context extraction
- Pattern matching
- Parallel scanning

### Usage

```python
from prompt_efficiency_suite import RepositoryScanner

scanner = RepositoryScanner(max_workers=4)

# Scan a repository
prompt_locations = scanner.scan_repository("/path/to/repo")

# Get scan statistics
stats = scanner.get_scan_stats(prompt_locations)

# Export results
scanner.export_results(Path("results.json"))
```

## AdaptiveBudgetManager

The `AdaptiveBudgetManager` manages token budgets dynamically.

### Features
- Dynamic budget adjustment
- Usage tracking
- Cost optimization
- Alert system

### Usage

```python
from prompt_efficiency_suite import AdaptiveBudgetManager
from datetime import timedelta

manager = AdaptiveBudgetManager(
    initial_budget=10000,
    allocation_period=timedelta(days=1),
    min_budget=1000,
    max_budget=1000000
)

# Record usage
manager.record_usage(metrics)

# Check budget
remaining = manager.get_remaining_budget()

# Adjust budget
manager.adjust_budget()

# Get statistics
stats = manager.get_budget_stats()
```

## Component Integration

Components are designed to work together seamlessly:

```python
from prompt_efficiency_suite import (
    BaseCompressor,
    PromptAnalyzer,
    MetricsTracker,
    BulkOptimizer,
    MacroManager,
    RepositoryScanner,
    AdaptiveBudgetManager
)

# Initialize components
compressor = BaseCompressor()
analyzer = PromptAnalyzer()
tracker = MetricsTracker()
optimizer = BulkOptimizer(compressor, analyzer, tracker)
macro_manager = MacroManager()
scanner = RepositoryScanner()
budget_manager = AdaptiveBudgetManager()

# Scan repository for prompts
prompts = scanner.scan_repository("/path/to/repo")

# Optimize found prompts
results = await optimizer.optimize_batch(
    [p.prompt_text for p in prompts],
    target_ratio=0.5
)

# Track metrics
for result in results:
    tracker.add_metrics(result.metrics)
    budget_manager.record_usage(result.metrics)
```

## Best Practices

1. **Component Initialization**
   - Initialize components once and reuse them
   - Use appropriate configuration for your use case
   - Consider resource constraints

2. **Error Handling**
   - Implement proper error handling for each component
   - Use try-except blocks for critical operations
   - Log errors appropriately

3. **Resource Management**
   - Monitor memory usage with large batches
   - Use appropriate worker counts for parallel operations
   - Clean up resources when done

4. **Performance Optimization**
   - Use batch operations when possible
   - Implement caching where appropriate
   - Monitor and adjust resource usage
