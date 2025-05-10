"""
Integration tests for the CLI commands.
"""

import os

import pytest
from click.testing import CliRunner

from prompt_efficiency_suite.cli import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def sample_prompt():
    """Return a sample prompt for testing."""
    return "Write a function that calculates the Fibonacci sequence."


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary repository with sample prompts."""
    # Create sample files
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "example1.txt").write_text("Write a function that calculates the Fibonacci sequence.")
    (tmp_path / "prompts" / "example2.txt").write_text("Create a REST API endpoint for user authentication.")
    return tmp_path


def test_analyze_command(runner, sample_prompt):
    """Test the analyze command."""
    result = runner.invoke(cli, ["analyze", sample_prompt])
    assert result.exit_code == 0
    assert "Analysis Results" in result.output
    assert "Clarity" in result.output
    assert "Structure" in result.output
    assert "Complexity" in result.output


def test_suggest_command(runner, sample_prompt):
    """Test the suggest command."""
    result = runner.invoke(cli, ["suggest", sample_prompt])
    assert result.exit_code == 0
    assert "Improvement Suggestions" in result.output


def test_trim_command(runner, sample_prompt):
    """Test the trim command."""
    result = runner.invoke(
        cli, ["trim", sample_prompt, "--preserve-ratio", "0.8", "--domain-terms", "function,Fibonacci"]
    )
    assert result.exit_code == 0
    assert "Original Prompt" in result.output
    assert "Trimmed Prompt" in result.output


def test_compress_code_command(runner, sample_prompt):
    """Test the compress_code command."""
    result = runner.invoke(cli, ["compress-code", sample_prompt, "--language", "python"])
    assert result.exit_code == 0
    assert "Original Prompt" in result.output
    assert "Compressed Prompt" in result.output


def test_bulk_optimize_command(runner, temp_repo):
    """Test the bulk_optimize command."""
    result = runner.invoke(cli, ["bulk-optimize", str(temp_repo / "prompts")])
    assert result.exit_code == 0
    assert "Bulk Optimization Results" in result.output
    assert "example1.txt" in result.output
    assert "example2.txt" in result.output


def test_macro_commands(runner):
    """Test macro management commands."""
    # Test install
    result = runner.invoke(cli, ["macro", "install", "test-pack"])
    assert result.exit_code == 0
    assert "Successfully installed macro pack" in result.output

    # Test list
    result = runner.invoke(cli, ["macro", "list"])
    assert result.exit_code == 0
    assert "Available Macro Packs" in result.output
    assert "test-pack" in result.output

    # Test apply
    result = runner.invoke(cli, ["macro", "apply", "test-pack", "test_file.txt"])
    assert result.exit_code == 0
    assert "Macro Application Results" in result.output


def test_estimate_cost_command(runner, sample_prompt):
    """Test the estimate_cost command."""
    result = runner.invoke(cli, ["estimate-cost", sample_prompt, "--model", "gpt-4", "--currency", "USD"])
    assert result.exit_code == 0
    assert "Cost Estimation Results" in result.output
    assert "Input Tokens" in result.output
    assert "Total Cost" in result.output


def test_scan_repository_command(runner, temp_repo):
    """Test the scan_repository command."""
    result = runner.invoke(
        cli,
        [
            "scan-repository",
            str(temp_repo),
            "--output",
            "scan_report.json",
            "--include-patterns",
            "*.txt",
            "--exclude-patterns",
            "*.py",
        ],
    )
    assert result.exit_code == 0
    assert "Repository Scan Summary" in result.output
    assert "Files Scanned" in result.output
    assert "Prompts Found" in result.output


def test_translate_model_command(runner, sample_prompt):
    """Test the translate_model command."""
    result = runner.invoke(
        cli, ["translate-model", sample_prompt, "--source-model", "gpt-4", "--target-model", "gpt-3.5-turbo"]
    )
    assert result.exit_code == 0
    assert "Original Prompt" in result.output
    assert "Translated Prompt" in result.output


def test_check_budget_command(runner, temp_repo):
    """Test the check_budget command."""
    result = runner.invoke(
        cli, ["check-budget", str(temp_repo / "prompts" / "example1.txt"), str(temp_repo / "prompts" / "example2.txt")]
    )
    assert result.exit_code == 0
    assert "Budget Check Results" in result.output
    assert "Usage" in result.output
    assert "Budget" in result.output


def test_generate_report_command(runner, temp_repo):
    """Test the generate_report command."""
    result = runner.invoke(
        cli,
        ["generate-report", str(temp_repo / "prompts" / "example1.txt"), "--output", "report.html", "--format", "html"],
    )
    assert result.exit_code == 0
    assert "Report generated" in result.output
    assert os.path.exists("report.html")
