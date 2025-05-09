import click
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from .benchmark.benchmark import (
    BenchmarkAggregator,
    BenchmarkMetrics,
    BenchmarkTask,
    TaskType
)
from .orchestrator.policy_engine import (
    RoutingPolicy,
    PolicyEngine
)
from .orchestrator.orchestrator import AdaptiveOrchestrator
from .telemetry.ci_report import CIReportGenerator, CIReportConfig
from .translator import PromptTranslator, ModelCapabilityRegistry

# Global state
aggregator: Optional[BenchmarkAggregator] = None
policy_engine: Optional[PolicyEngine] = None
orchestrator: Optional[AdaptiveOrchestrator] = None
translator: Optional[PromptTranslator] = None
model_registry: Optional[ModelCapabilityRegistry] = None

def initialize_components(data_dir: str):
    """Initialize all system components."""
    global aggregator, policy_engine, orchestrator, translator, model_registry
    
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    
    aggregator = BenchmarkAggregator(str(data_path))
    policy_engine = PolicyEngine(str(data_path))
    orchestrator = AdaptiveOrchestrator(
        policy_engine=policy_engine,
        metrics_dir=str(data_path)
    )
    translator = PromptTranslator()
    model_registry = ModelCapabilityRegistry()

@click.group()
@click.option('--data-dir', default='.prompt_efficiency_data',
              help='Directory to store system data')
def cli(data_dir: str):
    """Prompt Efficiency Suite CLI."""
    initialize_components(data_dir)

@cli.group()
def benchmark():
    """Benchmark management commands."""
    pass

@benchmark.command()
@click.argument('task_type')
@click.argument('name')
@click.option('--description', help='Task description')
def create_task(task_type: str, name: str, description: Optional[str]):
    """Create a new benchmark task."""
    try:
        task_type_enum = TaskType(task_type)
    except ValueError:
        click.echo(f"Invalid task type. Must be one of: {', '.join(t.value for t in TaskType)}")
        return
    
    task = BenchmarkTask(
        task_id=f"{task_type}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        name=name,
        task_type=task_type_enum,
        created_at=datetime.now()
    )
    
    click.echo(f"Created task: {task.task_id}")

@benchmark.command()
@click.argument('task_id')
@click.argument('prompt')
@click.argument('model')
@click.option('--accuracy', type=float, required=True)
@click.option('--latency-ms', type=int, required=True)
@click.option('--cost-per-token', type=float, required=True)
@click.option('--token-count', type=int, required=True)
@click.option('--quality-score', type=float, required=True)
@click.option('--success-rate', type=float, required=True)
@click.option('--error-rate', type=float, required=True)
@click.option('--metadata', type=str, help='JSON string of additional metadata')
def submit(task_id: str, prompt: str, model: str, **metrics):
    """Submit benchmark results."""
    metadata = {}
    if metrics.get('metadata'):
        try:
            metadata = json.loads(metrics['metadata'])
        except json.JSONDecodeError:
            click.echo("Error: metadata must be a valid JSON string")
            return
    
    benchmark_metrics = BenchmarkMetrics(
        accuracy=metrics['accuracy'],
        latency_ms=metrics['latency_ms'],
        cost_per_token=metrics['cost_per_token'],
        token_count=metrics['token_count'],
        quality_score=metrics['quality_score'],
        success_rate=metrics['success_rate'],
        error_rate=metrics['error_rate'],
        timestamp=datetime.now()
    )
    
    aggregator.submit_benchmark(
        task_id=task_id,
        prompt=prompt,
        model=model,
        metrics=benchmark_metrics,
        metadata=metadata
    )
    
    click.echo(f"Submitted benchmark for task {task_id}")

@benchmark.command()
@click.argument('task_id')
def leaderboard(task_id: str):
    """Show leaderboard for a task."""
    entries = aggregator.get_leaderboard(task_id)
    
    if not entries:
        click.echo(f"No entries found for task {task_id}")
        return
    
    # Print leaderboard
    click.echo(f"\nLeaderboard for task {task_id}:")
    click.echo("-" * 80)
    click.echo(f"{'Model':<20} {'Accuracy':<10} {'Latency':<10} {'Cost':<10} {'Quality':<10}")
    click.echo("-" * 80)
    
    for entry in entries:
        click.echo(
            f"{entry.model:<20} "
            f"{entry.metrics.accuracy:<10.2f} "
            f"{entry.metrics.latency_ms:<10} "
            f"{entry.metrics.cost_per_token:<10.4f} "
            f"{entry.metrics.quality_score:<10.2f}"
        )

@cli.group()
def policy():
    """Policy management commands."""
    pass

@policy.command()
@click.argument('task_type')
@click.option('--min-quality', type=float, required=True)
@click.option('--max-latency', type=int, required=True)
@click.option('--max-cost', type=float, required=True)
@click.option('--preferred-models', type=str, required=True)
@click.option('--fallback-models', type=str, required=True)
@click.option('--capabilities', type=str, required=True)
@click.option('--priority', type=int, default=1)
def add(task_type: str, **kwargs):
    """Add a new routing policy."""
    try:
        task_type_enum = TaskType(task_type)
    except ValueError:
        click.echo(f"Invalid task type. Must be one of: {', '.join(t.value for t in TaskType)}")
        return
    
    try:
        preferred_models = kwargs['preferred_models'].split(',')
        fallback_models = kwargs['fallback_models'].split(',')
        capabilities = kwargs['capabilities'].split(',')
    except Exception as e:
        click.echo(f"Error parsing lists: {str(e)}")
        return
    
    policy = RoutingPolicy(
        task_type=task_type_enum,
        min_quality_score=kwargs['min_quality'],
        max_latency_ms=kwargs['max_latency'],
        max_cost_per_token=kwargs['max_cost'],
        preferred_models=preferred_models,
        fallback_models=fallback_models,
        required_capabilities=capabilities,
        priority=kwargs['priority']
    )
    
    policy_engine.add_policy(policy)
    click.echo("Policy added successfully")

@cli.group()
def report():
    """Report generation commands."""
    pass

@report.command()
@click.argument('task_id')
@click.option('--format', type=click.Choice(['json', 'csv']), default='json')
@click.option('--output-dir', type=str, default='reports')
@click.option('--include-metadata/--no-metadata', default=True)
def generate(task_id: str, format: str, output_dir: str, include_metadata: bool):
    """Generate a benchmark report."""
    config = CIReportConfig(
        output_dir=output_dir,
        format=format,
        include_metadata=include_metadata
    )
    
    generator = CIReportGenerator(config, aggregator)
    
    # Get submissions for the task
    submissions = aggregator.get_submissions()
    task_submissions = [s for s in submissions if s.task_id == task_id]
    
    if not task_submissions:
        click.echo(f"No submissions found for task {task_id}")
        return
    
    # Convert submissions to report format
    report_results = [{
        "prompt": s.prompt,
        "model": s.model,
        "metrics": {
            "accuracy": s.metrics.accuracy,
            "latency_ms": s.metrics.latency_ms,
            "cost_per_token": s.metrics.cost_per_token,
            "token_count": s.metrics.token_count,
            "quality_score": s.metrics.quality_score,
            "success_rate": s.metrics.success_rate,
            "error_rate": s.metrics.error_rate
        },
        "metadata": s.metadata
    } for s in task_submissions]
    
    # Generate report
    report_path = generator.generate_report(report_results, task_submissions[0].task)
    click.echo(f"Report generated: {report_path}")

@cli.group()
def model():
    """Model management commands."""
    pass

@model.command()
@click.argument('model_name')
def capabilities(model_name: str):
    """Show model capabilities."""
    config = model_registry.get_config(model_name)
    
    if not config:
        click.echo(f"No configuration found for model {model_name}")
        return
    
    click.echo(f"\nCapabilities for {model_name}:")
    click.echo("-" * 40)
    for capability in config.capabilities:
        click.echo(f"- {capability.value}")

@model.command()
@click.argument('model_name')
@click.option('--latency-ms', type=int, required=True)
@click.option('--cost-per-token', type=float, required=True)
@click.option('--success-rate', type=float, required=True)
@click.option('--quality-score', type=float, required=True)
@click.option('--sample-size', type=int, required=True)
def update_performance(model_name: str, **metrics):
    """Update model performance metrics."""
    policy_engine.update_performance(
        model=model_name,
        latency_ms=metrics['latency_ms'],
        cost_per_token=metrics['cost_per_token'],
        success_rate=metrics['success_rate'],
        quality_score=metrics['quality_score'],
        sample_size=metrics['sample_size']
    )
    
    click.echo(f"Updated performance metrics for {model_name}")

if __name__ == '__main__':
    cli() 