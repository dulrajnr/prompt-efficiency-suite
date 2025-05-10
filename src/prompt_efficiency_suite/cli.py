"""
CLI - Command-line interface for the prompt efficiency suite.
"""

import argparse
import json
import logging
import sys
from datetime import timedelta
from pathlib import Path
from typing import Dict, Optional

import click

from .adaptive_budgeting import AdaptiveBudgetManager
from .analyzer import PromptAnalyzer
from .base_compressor import BaseCompressor
from .bulk_optimizer import BulkOptimizer
from .cost_estimator import CostEstimator
from .macro_manager import MacroManager
from .macro_suggester import MacroSuggester
from .metrics import MetricsTracker
from .multimodal_compressor import MultimodalCompressor
from .optimizer import PromptOptimizer
from .repository_scanner import RepositoryScanner
from .token_counter import TokenCounter
from .utils import format_size, format_timestamp, load_config, save_config

logger = logging.getLogger(__name__)


def setup_parser() -> argparse.ArgumentParser:
    """Set up command-line argument parser.

    Returns:
        argparse.ArgumentParser: Argument parser.
    """
    parser = argparse.ArgumentParser(description="Prompt Efficiency Suite CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a prompt")
    analyze_parser.add_argument("prompt", help="Prompt to analyze")
    analyze_parser.add_argument("--output", help="Output file path")
    analyze_parser.add_argument("--config", help="Configuration file path")

    # Optimize command
    optimize_parser = subparsers.add_parser("optimize", help="Optimize a prompt")
    optimize_parser.add_argument("prompt", help="Prompt to optimize")
    optimize_parser.add_argument("--output", help="Output file path")
    optimize_parser.add_argument("--config", help="Configuration file path")

    # Estimate command
    estimate_parser = subparsers.add_parser("estimate", help="Estimate prompt cost")
    estimate_parser.add_argument("prompt", help="Prompt to estimate")
    estimate_parser.add_argument("--model", default="gpt-4", help="Model name")
    estimate_parser.add_argument("--output", help="Output file path")

    # Count command
    count_parser = subparsers.add_parser("count", help="Count tokens in a prompt")
    count_parser.add_argument("prompt", help="Prompt to count tokens in")
    count_parser.add_argument("--model", default="gpt-4", help="Model name")
    count_parser.add_argument("--output", help="Output file path")

    return parser


def load_config(config_path: Optional[str] = None) -> Dict:
    """Load configuration from file.

    Args:
        config_path (Optional[str]): Path to configuration file.

    Returns:
        Dict: Configuration dictionary.
    """
    if not config_path:
        return {}

    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        return {}


def save_output(data: Dict, output_path: Optional[str] = None) -> None:
    """Save output to file.

    Args:
        data (Dict): Data to save.
        output_path (Optional[str]): Output file path.
    """
    if not output_path:
        print(json.dumps(data, indent=2))
        return

    try:
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save output to {output_path}: {e}")
        print(json.dumps(data, indent=2))


def handle_analyze(args: argparse.Namespace) -> None:
    """Handle analyze command.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """
    config = load_config(args.config)
    analyzer = PromptAnalyzer(**config)
    result = analyzer.analyze(args.prompt)
    save_output(result.__dict__, args.output)


def handle_optimize(args: argparse.Namespace) -> None:
    """Handle optimize command.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """
    config = load_config(args.config)
    optimizer = PromptOptimizer(**config)
    result = optimizer.optimize(args.prompt)
    save_output(result.__dict__, args.output)


def handle_estimate(args: argparse.Namespace) -> None:
    """Handle estimate command.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """
    estimator = CostEstimator()
    result = estimator.estimate_cost(args.prompt, args.model)
    save_output(result.__dict__, args.output)


def handle_count(args: argparse.Namespace) -> None:
    """Handle count command.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """
    counter = TokenCounter()
    result = counter.count_tokens(args.prompt, args.model)
    save_output(result.__dict__, args.output)


def cli() -> None:
    """Main CLI entry point."""
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "analyze": handle_analyze,
        "optimize": handle_optimize,
        "estimate": handle_estimate,
        "count": handle_count,
    }

    try:
        handlers[args.command](args)
    except Exception as e:
        logger.error(f"Error executing command {args.command}: {e}")
        sys.exit(1)


@click.group()
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to configuration file")
@click.pass_context
def cli(ctx, config):
    """Prompt Efficiency Suite CLI."""
    ctx.ensure_object(dict)
    if config:
        ctx.obj["config"] = load_config(config)
    else:
        ctx.obj["config"] = {}


@cli.command()
@click.argument("prompt", type=str)
@click.option("--target-ratio", "-r", type=float, help="Target compression ratio")
@click.option("--min-quality", "-q", type=float, default=0.7, help="Minimum quality score")
@click.pass_context
def optimize(ctx, prompt, target_ratio, min_quality):
    """Optimize a single prompt."""
    try:
        # Initialize components
        compressor = MultimodalCompressor()
        analyzer = PromptAnalyzer()
        metrics_tracker = MetricsTracker()
        optimizer = BulkOptimizer(compressor, analyzer, metrics_tracker)

        # Optimize the prompt
        result = optimizer.optimize_batch([prompt], target_ratio, min_quality)

        if result:
            click.echo(json.dumps(result[0], indent=2))
        else:
            click.echo("No valid optimization found.")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.pass_context
def scan(ctx, repo_path, output):
    """Scan a repository for prompts."""
    try:
        scanner = RepositoryScanner()
        prompt_locations = scanner.scan_repository(repo_path)

        if output:
            with open(output, "w") as f:
                json.dump([vars(loc) for loc in prompt_locations], f, indent=2)
        else:
            click.echo(json.dumps([vars(loc) for loc in prompt_locations], indent=2))

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("prompts", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.pass_context
def suggest_macros(ctx, prompts, output):
    """Suggest macros based on prompt patterns."""
    try:
        # Load prompts
        with open(prompts, "r") as f:
            prompt_list = [line.strip() for line in f if line.strip()]

        # Initialize components
        macro_manager = MacroManager()
        suggester = MacroSuggester(macro_manager)

        # Analyze prompts and suggest macros
        patterns = suggester.analyze_prompts(prompt_list)
        suggested_macros = suggester.suggest_macros(patterns)

        if output:
            with open(output, "w") as f:
                json.dump([macro.dict() for macro in suggested_macros], f, indent=2)
        else:
            click.echo(json.dumps([macro.dict() for macro in suggested_macros], indent=2))

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("config_path", type=click.Path())
@click.option("--initial-budget", "-b", type=int, default=10000, help="Initial token budget")
@click.option("--period", "-p", type=int, default=1, help="Budget period in days")
@click.pass_context
def budget(ctx, config_path, initial_budget, period):
    """Manage token budget."""
    try:
        # Initialize budget manager
        budget_manager = AdaptiveBudgetManager(initial_budget=initial_budget, allocation_period=timedelta(days=period))

        # Load and apply configuration
        config = load_config(config_path)
        if config:
            # Apply configuration
            pass

        # Get and display budget stats
        stats = budget_manager.get_budget_stats()
        click.echo(json.dumps(stats, indent=2))

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("prompt", type=str)
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.pass_context
def analyze(ctx, prompt, output):
    """Analyze a prompt."""
    try:
        analyzer = PromptAnalyzer()
        analysis = analyzer.analyze(prompt)

        if output:
            with open(output, "w") as f:
                json.dump(analysis.dict(), f, indent=2)
        else:
            click.echo(json.dumps(analysis.dict(), indent=2))

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


def main():
    """Main entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
