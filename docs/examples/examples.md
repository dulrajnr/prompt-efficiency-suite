# Examples

This document provides practical examples of using the Prompt Efficiency Suite.

## Basic Usage

### Optimizing a Single Prompt

```python
from prompt_efficiency_suite import BaseCompressor, PromptAnalyzer, MetricsTracker

async def optimize_prompt(prompt: str):
    # Initialize components
    compressor = BaseCompressor()
    analyzer = PromptAnalyzer()
    tracker = MetricsTracker()
    
    # Compress the prompt
    compression_result = await compressor.compress(
        text=prompt,
        target_ratio=0.7
    )
    
    # Analyze the compressed prompt
    analysis = analyzer.analyze(compression_result.compressed_text)
    
    # Track metrics
    metrics = EfficiencyMetrics(
        prompt_id="prompt_1",
        token_count=compression_result.compressed_tokens,
        cost=0.0003,  # Example cost
        success_rate=0.95,
        quality_score=analysis.readability_score
    )
    tracker.add_metrics(metrics)
    
    return {
        "compressed_text": compression_result.compressed_text,
        "compression_ratio": compression_result.compression_ratio,
        "analysis": analysis
    }

# Usage
prompt = """
Please analyze the following text and provide a detailed summary
of the key points, including any important statistics or figures
mentioned in the content.
"""
result = await optimize_prompt(prompt)
print(f"Compression ratio: {result['compression_ratio']:.2f}")
print(f"Readability score: {result['analysis'].readability_score:.2f}")
```

### Batch Processing Prompts

```python
from prompt_efficiency_suite import BulkOptimizer

async def process_prompt_batch(prompts: List[str]):
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
    
    # Process batch
    results = await optimizer.optimize_batch(
        prompts=prompts,
        target_ratio=0.7,
        min_quality_score=0.8
    )
    
    return results

# Usage
prompts = [
    "Summarize the key points from the following text...",
    "Analyze the sentiment of the following review...",
    "Extract the main topics from the following article..."
]
results = await process_prompt_batch(prompts)
```

## Advanced Usage

### Using Macros

```python
from prompt_efficiency_suite import MacroManager, MacroDefinition

def setup_macros():
    # Initialize macro manager
    manager = MacroManager()
    
    # Define macros
    summary_macro = MacroDefinition(
        name="summary",
        template="""
        Please provide a {length} summary of the following text:
        
        {text}
        
        Focus on the following aspects:
        {aspects}
        """,
        parameters=["length", "text", "aspects"],
        description="Creates a summary prompt with specified length and focus"
    )
    
    analysis_macro = MacroDefinition(
        name="analysis",
        template="""
        Analyze the following {type} with respect to:
        
        {criteria}
        
        Text to analyze:
        {text}
        """,
        parameters=["type", "criteria", "text"],
        description="Creates an analysis prompt with specific criteria"
    )
    
    # Register macros
    manager.register_macro(summary_macro)
    manager.register_macro(analysis_macro)
    
    return manager

# Usage
manager = setup_macros()

# Expand summary macro
summary_prompt = manager.expand_macro(
    name="summary",
    parameters={
        "length": "concise",
        "text": "Your text here...",
        "aspects": "- Key points\n- Main arguments\n- Conclusions"
    }
)

# Expand analysis macro
analysis_prompt = manager.expand_macro(
    name="analysis",
    parameters={
        "type": "article",
        "criteria": "- Clarity\n- Accuracy\n- Relevance",
        "text": "Your text here..."
    }
)
```

### Repository Scanning

```python
from prompt_efficiency_suite import RepositoryScanner

async def scan_codebase(repo_path: str):
    # Initialize scanner
    scanner = RepositoryScanner(max_workers=4)
    
    # Scan repository
    locations = scanner.scan_repository(repo_path)
    
    # Process results
    for location in locations:
        print(f"Found prompt in {location.file_path}:{location.line_number}")
        print(f"Language: {location.language}")
        print(f"Context: {location.context}")
        print(f"Prompt: {location.prompt_text}")
        print("---")

# Usage
await scan_codebase("/path/to/your/repo")
```

### Budget Management

```python
from prompt_efficiency_suite import AdaptiveBudgetManager
from datetime import timedelta

def setup_budget_management():
    # Initialize budget manager
    budget_manager = AdaptiveBudgetManager(
        initial_budget=100000,  # 100K tokens
        allocation_period=timedelta(days=1),
        min_budget=10000,      # 10K minimum
        max_budget=1000000     # 1M maximum
    )
    
    return budget_manager

async def process_with_budget(prompt: str, budget_manager: AdaptiveBudgetManager):
    # Check budget
    if not budget_manager.can_allocate(1000):  # Example token requirement
        raise BudgetError("Insufficient budget")
    
    # Process prompt
    result = await optimize_prompt(prompt)
    
    # Record usage
    budget_manager.record_usage(
        EfficiencyMetrics(
            prompt_id="prompt_1",
            token_count=result["compression"].compressed_tokens,
            cost=0.0003,
            success_rate=0.95
        )
    )
    
    return result

# Usage
budget_manager = setup_budget_management()
try:
    result = await process_with_budget(prompt, budget_manager)
    print(f"Remaining budget: {budget_manager.get_remaining_budget()}")
except BudgetError as e:
    print(f"Budget error: {e}")
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from prompt_efficiency_suite import (
    BaseCompressor,
    PromptAnalyzer,
    AdaptiveBudgetManager
)

app = FastAPI()

# Initialize components
compressor = BaseCompressor()
analyzer = PromptAnalyzer()
budget_manager = AdaptiveBudgetManager(initial_budget=100000)

@app.post("/optimize")
async def optimize_prompt(prompt: str):
    try:
        # Check budget
        if not budget_manager.can_allocate(1000):
            raise HTTPException(status_code=429, detail="Budget exceeded")
        
        # Process prompt
        compression_result = await compressor.compress(prompt)
        analysis = analyzer.analyze(compression_result.compressed_text)
        
        # Record usage
        budget_manager.record_usage(
            EfficiencyMetrics(
                prompt_id="api_request",
                token_count=compression_result.compressed_tokens,
                cost=0.0003,
                success_rate=0.95
            )
        )
        
        return {
            "compressed_text": compression_result.compressed_text,
            "compression_ratio": compression_result.compression_ratio,
            "analysis": analysis.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### CLI Integration

```python
import click
from prompt_efficiency_suite import (
    BaseCompressor,
    PromptAnalyzer,
    RepositoryScanner
)

@click.group()
def cli():
    """Prompt Efficiency Suite CLI"""
    pass

@cli.command()
@click.argument('prompt')
@click.option('--target-ratio', default=0.7, help='Target compression ratio')
def optimize(prompt, target_ratio):
    """Optimize a single prompt"""
    compressor = BaseCompressor()
    analyzer = PromptAnalyzer()
    
    result = await compressor.compress(prompt, target_ratio)
    analysis = analyzer.analyze(result.compressed_text)
    
    click.echo(f"Compression ratio: {result.compression_ratio:.2f}")
    click.echo(f"Readability score: {analysis.readability_score:.2f}")
    click.echo(f"Compressed text: {result.compressed_text}")

@cli.command()
@click.argument('repo_path')
def scan(repo_path):
    """Scan repository for prompts"""
    scanner = RepositoryScanner()
    locations = scanner.scan_repository(repo_path)
    
    for location in locations:
        click.echo(f"Found in {location.file_path}:{location.line_number}")
        click.echo(f"Prompt: {location.prompt_text}")
        click.echo("---")

if __name__ == '__main__':
    cli()
```

## Configuration Examples

### YAML Configuration

```yaml
# config.yaml
compressor:
  model_name: "gpt-3.5-turbo"
  target_ratio: 0.7
  min_quality_score: 0.8

analyzer:
  model_name: "en_core_web_sm"
  metrics:
    - readability
    - complexity
    - redundancy

budget:
  initial_budget: 100000
  allocation_period_days: 1
  min_budget: 10000
  max_budget: 1000000

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Loading Configuration

```python
from prompt_efficiency_suite import load_config

def setup_from_config():
    # Load configuration
    config = load_config("config.yaml")
    
    # Initialize components with config
    compressor = BaseCompressor(
        model_name=config["compressor"]["model_name"]
    )
    
    analyzer = PromptAnalyzer(
        model_name=config["analyzer"]["model_name"]
    )
    
    budget_manager = AdaptiveBudgetManager(
        initial_budget=config["budget"]["initial_budget"],
        min_budget=config["budget"]["min_budget"],
        max_budget=config["budget"]["max_budget"]
    )
    
    return compressor, analyzer, budget_manager
```

## Testing Examples

### Unit Tests

```python
import pytest
from prompt_efficiency_suite import BaseCompressor, PromptAnalyzer

@pytest.mark.asyncio
async def test_compressor():
    compressor = BaseCompressor()
    result = await compressor.compress("Test prompt")
    
    assert result.compression_ratio > 0
    assert result.compressed_text != ""
    assert result.original_tokens > result.compressed_tokens

def test_analyzer():
    analyzer = PromptAnalyzer()
    analysis = analyzer.analyze("Test prompt")
    
    assert analysis.readability_score >= 0
    assert analysis.complexity_score >= 0
    assert len(analysis.key_phrases) >= 0

@pytest.mark.asyncio
async def test_budget_manager():
    budget_manager = AdaptiveBudgetManager(initial_budget=1000)
    
    assert budget_manager.get_remaining_budget() == 1000
    assert budget_manager.can_allocate(500)
    assert not budget_manager.can_allocate(1500)
```

### Integration Tests

```python
import pytest
from prompt_efficiency_suite import BulkOptimizer

@pytest.mark.asyncio
async def test_optimization_workflow():
    # Initialize components
    compressor = BaseCompressor()
    analyzer = PromptAnalyzer()
    tracker = MetricsTracker()
    
    # Create optimizer
    optimizer = BulkOptimizer(
        compressor=compressor,
        analyzer=analyzer,
        metrics_tracker=tracker
    )
    
    # Test batch processing
    prompts = ["Test prompt 1", "Test prompt 2"]
    results = await optimizer.optimize_batch(prompts)
    
    assert len(results) == len(prompts)
    assert all(r["compression"].compression_ratio > 0 for r in results)
    assert all(r["analysis"].readability_score >= 0 for r in results)
```

## Performance Examples

### Caching

```python
from cachetools import TTLCache
from prompt_efficiency_suite import PromptAnalyzer

# Create cache
analysis_cache = TTLCache(maxsize=100, ttl=3600)  # 1 hour TTL

def get_cached_analysis(prompt: str) -> Optional[PromptAnalysis]:
    # Check cache
    if prompt in analysis_cache:
        return analysis_cache[prompt]
    
    # Perform analysis
    analyzer = PromptAnalyzer()
    analysis = analyzer.analyze(prompt)
    
    # Cache result
    analysis_cache[prompt] = analysis
    return analysis
```

### Parallel Processing

```python
import asyncio
from prompt_efficiency_suite import BaseCompressor

async def process_prompts_parallel(prompts: List[str]):
    compressor = BaseCompressor()
    
    # Create tasks
    tasks = [
        compressor.compress(prompt)
        for prompt in prompts
    ]
    
    # Process in parallel
    results = await asyncio.gather(*tasks)
    return results

# Usage
prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
results = await process_prompts_parallel(prompts)
``` 