import json
import os
from pathlib import Path
from typing import Optional

import click
import yaml

from app.compressor.multimodal import MultimodalCompressor

from .batch.optimizer import BatchOptimizer
from .cicd.integration import CICDIntegration
from .trimmer.domain_aware import DomainAwareTrimmer


def load_config(config_path: Optional[str] = None) -> dict:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = "config.yaml"

    config_path = Path(config_path)
    if not config_path.exists():
        return {}

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


@click.group()
def cli():
    """Prompt Efficiency Suite CLI"""
    pass


@cli.command()
@click.option("--domain", required=True, help="Domain for trimming (e.g., legal, medical)")
@click.option("--input", required=True, help="Input file path")
@click.option("--output", required=True, help="Output file path")
@click.option("--min-importance", default=0.7, help="Minimum importance score for tokens")
@click.option("--config", help="Path to config file")
def trim(domain: str, input: str, output: str, min_importance: float, config: Optional[str]):
    """Trim a prompt while preserving important domain-specific terms."""
    config_data = load_config(config)
    dictionary_path = config_data.get("paths", {}).get("dictionary_path", "data/dicts")

    # Use Path for path handling
    dictionary_path = Path(dictionary_path)
    input_path = Path(input)
    output_path = Path(output)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    trimmer = DomainAwareTrimmer(str(dictionary_path))

    with open(input_path, "r") as f:
        prompt = f.read()

    try:
        trimmed_prompt = trimmer.trim_prompt(prompt, domain, min_importance)
        tokens_before = trimmer.get_token_count(prompt)
        tokens_after = trimmer.get_token_count(trimmed_prompt)

        with open(output_path, "w") as f:
            f.write(trimmed_prompt)

        click.echo(f"Tokens before: {tokens_before}")
        click.echo(f"Tokens after: {tokens_after}")
        click.echo(f"Reduction: {((tokens_before - tokens_after) / tokens_before) * 100:.2f}%")

    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--repo", type=click.Path(exists=True), help="Path to prompt repository")
@click.option(
    "--report",
    type=click.Path(),
    default="reports/bulk_report.json",
    help="Path to output report",
)
@click.option("--config", type=click.Path(), help="Path to configuration file")
def bulk_optimize(repo, report, config):
    """Optimize prompts in bulk across a repository."""
    optimizer = BatchOptimizer(scan_paths=[repo])
    optimizer.scan_repository()
    optimizer.generate_macros()
    report_data = optimizer.generate_report()

    report_dir = Path(report).parent
    report_dir.mkdir(parents=True, exist_ok=True)

    with open(report, "w") as f:
        json.dump(report_data, f, indent=2)

    click.echo(f"Optimization complete. Report saved to {report}")


@cli.command()
@click.option("--input", type=click.Path(exists=True), help="Path to input file")
@click.option("--output", type=click.Path(), help="Path to output file")
@click.option(
    "--format",
    type=click.Choice(["json", "yaml", "python", "text", "image"]),
    help="Content format",
)
def compress(input, output, format):
    """Compress content using the multimodal compressor."""
    compressor = MultimodalCompressor()

    with open(input, "r") as f:
        content = f.read()

    compressed = compressor.compress(content, format)
    ratio = compressor.get_compression_ratio()

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w") as f:
        f.write(compressed)

    click.echo(f"Compression complete. Ratio: {ratio:.2f}")


if __name__ == "__main__":
    cli()
