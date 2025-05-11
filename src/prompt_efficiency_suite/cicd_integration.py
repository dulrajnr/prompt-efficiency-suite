"""CICD Integration - A module for integrating with CI/CD systems."""

import json
import logging
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    prompt_id: str
    success: bool
    metrics: Dict[str, float]
    errors: List[str]
    warnings: List[str]
    timestamp: datetime


@dataclass
class DeploymentResult:
    """Result of a prompt deployment."""

    prompt_id: str
    version: str
    environment: str
    success: bool
    metrics: Dict[str, float]
    errors: List[str]
    warnings: List[str]
    deployment_time: datetime
    rollback_available: bool
    metadata: Dict[str, Any]


class CICDIntegration:
    """A class for integrating with CI/CD systems."""

    def __init__(self):
        """Initialize the CI/CD integration."""
        self.logger = logging.getLogger(__name__)

    def integrate(self, system: str, config: Dict[str, Any]) -> bool:
        """Integrate with a CI/CD system.

        Args:
            system: The CI/CD system to integrate with
            config: Configuration for the integration

        Returns:
            True if integration was successful, False otherwise
        """
        # Validate system
        if not self._is_valid_system(system):
            raise ValueError(f"Invalid CI/CD system: {system}")

        # Get integration steps
        steps = self._get_integration_steps(system)

        # Execute steps
        for step in steps:
            if not self._execute_step(step, config):
                return False

        return True

    def _is_valid_system(self, system: str) -> bool:
        """Check if a CI/CD system is valid.

        Args:
            system: The system to check

        Returns:
            True if the system is valid, False otherwise
        """
        valid_systems = ["github", "gitlab", "jenkins", "circleci"]
        return system.lower() in valid_systems

    def _get_integration_steps(self, system: str) -> List[Dict[str, Any]]:
        """Get integration steps for a CI/CD system.

        Args:
            system: The system to get steps for

        Returns:
            List of integration steps
        """
        # This would be implemented to get steps
        return []

    def _execute_step(self, step: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Execute an integration step.

        Args:
            step: The step to execute
            config: Configuration for the step

        Returns:
            True if the step was successful, False otherwise
        """
        # This would be implemented to execute steps
        return True

    def run_pipeline(self, prompts_dir: Path) -> bool:
        """Run the CI/CD pipeline for prompt testing.

        Args:
            prompts_dir (Path): Directory containing prompt files.

        Returns:
            bool: True if all tests pass, False otherwise.
        """
        self.logger.info(f"Starting CI/CD pipeline for prompts in {prompts_dir}")

        # Load prompts
        prompts = self._load_prompts(prompts_dir)
        if not prompts:
            self.logger.error("No prompts found to test")
            return False

        # Run tests
        all_passed = True
        for prompt_id, prompt_data in prompts.items():
            result = self._test_prompt(prompt_id, prompt_data)
            self.test_results.append(result)

            if not result.success:
                all_passed = False
                self.logger.error(f"Tests failed for prompt {prompt_id}")
                for error in result.errors:
                    self.logger.error(f"  - {error}")

        # Generate report
        self._generate_report()

        return all_passed

    def get_test_summary(self) -> Dict[str, Any]:
        """Get a summary of test results.

        Returns:
            Dict[str, Any]: Test summary statistics.
        """
        if not self.test_results:
            return {}

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": passed_tests / total_tests,
            "average_metrics": self._calculate_average_metrics(),
            "timestamp": datetime.now().isoformat(),
        }

    def export_results(self, output_path: Path, format: str = "json") -> None:
        """Export test results to a file.

        Args:
            output_path (Path): Path to save results.
            format (str): Output format ('json' or 'yaml').
        """
        results_data = {
            "summary": self.get_test_summary(),
            "results": [
                {
                    "prompt_id": result.prompt_id,
                    "success": result.success,
                    "metrics": result.metrics,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "timestamp": result.timestamp.isoformat(),
                }
                for result in self.test_results
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            if format.lower() == "json":
                json.dump(results_data, f, indent=2)
            else:
                yaml.dump(results_data, f, default_flow_style=False)

    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from file."""
        with open(config_path, "r", encoding="utf-8") as f:
            if config_path.suffix.lower() == ".json":
                return json.load(f)
            return yaml.safe_load(f)

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("cicd_integration")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_prompts(self, prompts_dir: Path) -> Dict[str, Dict[str, Any]]:
        """Load prompts from directory."""
        prompts: Dict[str, Dict[str, Any]] = {}

        for file_path in prompts_dir.glob("**/*.{json,yaml,yml}"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    if file_path.suffix.lower() == ".json":
                        data = json.load(f)
                    else:
                        data = yaml.safe_load(f)

                prompt_id = file_path.stem
                prompts[prompt_id] = data

            except Exception as e:
                self.logger.error(f"Error loading prompt from {file_path}: {str(e)}")

        return prompts

    def _test_prompt(self, prompt_id: str, prompt_data: Dict[str, Any]) -> TestResult:
        """Run tests for a single prompt."""
        errors = []
        warnings = []
        metrics = {}

        try:
            # Validate prompt structure
            if not self._validate_prompt_structure(prompt_data):
                errors.append("Invalid prompt structure")

            # Run quality checks
            quality_metrics = self._check_prompt_quality(prompt_data)
            metrics.update(quality_metrics)

            # Run performance tests
            perf_metrics = self._run_performance_tests(prompt_data)
            metrics.update(perf_metrics)

            # Check for warnings
            warnings.extend(self._check_for_warnings(prompt_data))

        except Exception as e:
            errors.append(f"Test execution error: {str(e)}")

        success = len(errors) == 0

        return TestResult(
            prompt_id=prompt_id,
            success=success,
            metrics=metrics,
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
        )

    def _validate_prompt_structure(self, prompt_data: Dict[str, Any]) -> bool:
        """Validate the structure of a prompt."""
        required_fields = {"text", "metadata", "tests"}
        return all(field in prompt_data for field in required_fields)

    def _check_prompt_quality(self, prompt_data: Dict[str, Any]) -> Dict[str, float]:
        """Run quality checks on a prompt."""
        metrics = {
            "clarity_score": 0.0,
            "completeness_score": 0.0,
            "consistency_score": 0.0,
        }

        # Implement quality checks here
        # This is a placeholder implementation
        text = prompt_data.get("text", "")
        metrics["clarity_score"] = len(text.split()) / 100
        metrics["completeness_score"] = (
            1.0 if len(prompt_data.get("tests", [])) > 0 else 0.0
        )
        metrics["consistency_score"] = 1.0

        return metrics

    def _run_performance_tests(self, prompt_data: Dict[str, Any]) -> Dict[str, float]:
        """Run performance tests on a prompt."""
        metrics = {"response_time": 0.0, "token_usage": 0.0, "success_rate": 0.0}

        # Implement performance tests here
        # This is a placeholder implementation
        metrics["response_time"] = 1.0
        metrics["token_usage"] = len(prompt_data.get("text", "").split()) * 1.3
        metrics["success_rate"] = 1.0

        return metrics

    def _check_for_warnings(self, prompt_data: Dict[str, Any]) -> List[str]:
        """Check for potential issues that should generate warnings."""
        warnings = []

        text = prompt_data.get("text", "")
        if len(text.split()) > 100:
            warnings.append("Prompt is longer than recommended")

        if not prompt_data.get("metadata", {}).get("version"):
            warnings.append("No version information in metadata")

        return warnings

    def _calculate_average_metrics(self) -> Dict[str, float]:
        """Calculate average metrics across all test results."""
        if not self.test_results:
            return {}

        total_metrics: Dict[str, float] = {}
        metric_counts: Dict[str, int] = {}

        for result in self.test_results:
            for metric, value in result.metrics.items():
                total_metrics[metric] = total_metrics.get(metric, 0.0) + value
                metric_counts[metric] = metric_counts.get(metric, 0) + 1

        return {
            metric: total / metric_counts[metric]
            for metric, total in total_metrics.items()
        }

    def _generate_report(self) -> None:
        """Generate a test report."""
        summary = self.get_test_summary()

        self.logger.info("\n=== Test Report ===")
        self.logger.info(f"Total Tests: {summary['total_tests']}")
        self.logger.info(f"Passed: {summary['passed_tests']}")
        self.logger.info(f"Failed: {summary['failed_tests']}")
        self.logger.info(f"Success Rate: {summary['success_rate']:.2%}")

        if summary.get("average_metrics"):
            self.logger.info("\nAverage Metrics:")
            for metric, value in summary["average_metrics"].items():
                self.logger.info(f"  {metric}: {value:.2f}")

        self.logger.info("\nDetailed Results:")
        for result in self.test_results:
            status = "✓" if result.success else "✗"
            self.logger.info(f"\n{status} Prompt: {result.prompt_id}")

            if result.errors:
                self.logger.info("  Errors:")
                for error in result.errors:
                    self.logger.info(f"    - {error}")

            if result.warnings:
                self.logger.info("  Warnings:")
                for warning in result.warnings:
                    self.logger.info(f"    - {warning}")

    def _run_command_safely(
        self, command: List[str], **kwargs
    ) -> subprocess.CompletedProcess:
        """Run a command safely without shell injection vulnerabilities."""
        if not isinstance(command, list):
            raise ValueError("Command must be a list of strings")
        if any(not isinstance(arg, str) for arg in command):
            raise ValueError("All command arguments must be strings")
        return subprocess.run(command, check=True, shell=False, **kwargs)

    def run_tests(self, test_path: Optional[str] = None) -> TestResult:
        """Run tests with specified configuration."""
        command = ["pytest"]
        if test_path:
            if not Path(test_path).exists():
                raise ValueError(f"Test path does not exist: {test_path}")
            command.append(str(test_path))

        if self.config.get("test_args"):
            command.extend(self.config["test_args"])

        try:
            result = self._run_command_safely(command, capture_output=True, text=True)
            # Process test results...
            return TestResult(passed=True, output=result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Tests failed: {e.stderr}")
            return TestResult(passed=False, output=e.stderr)
