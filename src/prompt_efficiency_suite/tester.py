"""Tester - A module for testing prompt performance and effectiveness."""

import json
import logging
import secrets
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """A test case for prompt testing."""

    prompt: str
    expected_output: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class TestResult:
    """A class for storing test results."""

    def __init__(self, prompt: str, result: Dict[str, Any]):
        """Initialize test result.

        Args:
            prompt: The prompt that was tested
            result: The test result
        """
        self.prompt = prompt
        self.result = result


@dataclass
class TestSuite:
    """A collection of test cases."""

    name: str
    test_cases: List[TestCase]
    metadata: Optional[Dict[str, Any]] = None


class PromptTester:
    """A class for testing prompts and their optimizations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the PromptTester.

        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.test_history: List[TestResult] = []

    def run_test_suite(self, test_suite: TestSuite) -> List[TestResult]:
        """Run a suite of tests and return results."""
        results: List[TestResult] = []
        for test_case in test_suite.test_cases:
            result = self._run_test_case(test_case)
            results.append(result)
            self.test_history.append(result)
        return results

    def create_test_suite(
        self,
        name: str,
        test_cases: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TestSuite:
        """Create a test suite from test cases.

        Args:
            name (str): Test suite name.
            test_cases (List[Dict[str, Any]]): Test cases.
            metadata (Optional[Dict[str, Any]]): Test suite metadata.

        Returns:
            TestSuite: Created test suite.
        """
        suite_test_cases = []

        for case in test_cases:
            test_case = TestCase(
                prompt=case["prompt"],
                expected_output=case.get("expected_output"),
                context=case.get("context"),
                metadata=case.get("metadata"),
            )
            suite_test_cases.append(test_case)

        return TestSuite(name=name, test_cases=suite_test_cases, metadata=metadata)

    def load_test_suite(self, file_path: Path) -> TestSuite:
        """Load a test suite from a file.

        Args:
            file_path (Path): Path to test suite file.

        Returns:
            TestSuite: Loaded test suite.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.create_test_suite(
            name=data["name"],
            test_cases=data["test_cases"],
            metadata=data.get("metadata"),
        )

    def save_test_suite(self, test_suite: TestSuite, file_path: Path) -> None:
        """Save a test suite to a file.

        Args:
            test_suite (TestSuite): Test suite to save.
            file_path (Path): Path to save test suite.
        """
        data = {
            "name": test_suite.name,
            "test_cases": [
                {
                    "prompt": case.prompt,
                    "expected_output": case.expected_output,
                    "context": case.context,
                    "metadata": case.metadata,
                }
                for case in test_suite.test_cases
            ],
            "metadata": test_suite.metadata,
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_test_stats(self) -> Dict[str, Any]:
        """Get statistics about test runs.

        Returns:
            Dict[str, Any]: Test statistics.
        """
        if not self.test_history:
            return {}

        total_tests = len(self.test_history)
        successful_tests = sum(1 for r in self.test_history if r.success)

        # Calculate average execution time
        execution_times: List[float] = [r.latency for r in self.test_history]
        avg_execution_time = (
            sum(execution_times) / len(execution_times) if execution_times else 0
        )

        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
            "average_execution_time": avg_execution_time,
        }

    def export_results(self, output_path: Path) -> None:
        """Export test results to a file.

        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            "statistics": self.get_test_stats(),
            "results": [
                {
                    "test_case": {
                        "prompt": result.prompt,
                        "expected_output": result.expected_output,
                        "context": result.context,
                        "metadata": result.metadata,
                    },
                    "actual_output": result.response,
                    "success": result.success,
                    "execution_time": result.latency,
                    "error": result.error,
                    "metadata": result.metadata,
                }
                for result in self.test_history
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2)

    def _run_test_case(self, test_case: TestCase) -> TestResult:
        """Run a single test case and return the result."""
        start_time = time.time()
        error = None
        response = None
        token_count = 0

        try:
            # Simulate model response
            response = self._simulate_model_response(
                test_case.prompt, test_case.context, self.config
            )
            token_count = len(response.split())

            # Check if output matches expected
            success = (
                test_case.expected_output is None
                or response == test_case.expected_output
            )

        except Exception as e:
            error = str(e)
            success = False

        latency = time.time() - start_time

        return TestResult(
            prompt=test_case.prompt,
            response=response,
            latency=latency,
            token_count=token_count,
            success=success,
            error=error,
        )

    def _simulate_model_response(
        self, prompt: str, context: Optional[Dict[str, Any]], params: Dict[str, Any]
    ) -> str:
        """Simulate a model response.

        Args:
            prompt (str): Input prompt.
            context (Optional[Dict[str, Any]]): Context information.
            params (Dict[str, Any]): Test parameters.

        Returns:
            str: Simulated response.
        """
        # Simulate processing delay
        time.sleep(self._secure_random_float(0.1, 0.5))

        # For testing purposes, return a simple response
        return f"Response to: {prompt[:50]}..."

    def _secure_random_float(self, min_val: float, max_val: float) -> float:
        """Generate a secure random float between min_val and max_val."""
        range_size = int(
            (max_val - min_val) * 1000
        )  # Convert to milliseconds for precision
        random_ms = secrets.randbelow(range_size)
        return min_val + (random_ms / 1000)

    def get_test_results(self) -> Generator[TestResult, None, None]:
        """Get all test results as a generator."""
        for result in self.test_history:
            yield result

    def get_success_rate(self) -> float:
        """Calculate the success rate of all tests."""
        if not self.test_history:
            return 0.0
        successful = sum(1 for r in self.test_history if r.success)
        return successful / len(self.test_history)

    def get_average_latency(self) -> float:
        """Calculate the average latency of all tests."""
        if not self.test_history:
            return 0.0
        return sum(r.latency for r in self.test_history) / len(self.test_history)
