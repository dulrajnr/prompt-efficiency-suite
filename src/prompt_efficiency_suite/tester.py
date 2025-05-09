"""
Tester module for testing prompts and their optimizations.
"""

from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass
import json
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """A test case for prompt testing."""
    prompt: str
    expected_output: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class TestResult:
    """Result of a test case."""
    test_case: TestCase
    actual_output: Optional[str] = None
    success: bool = False
    execution_time: float = 0.0
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class TestSuite:
    """A collection of test cases."""
    name: str
    test_cases: List[TestCase]
    metadata: Optional[Dict[str, Any]] = None

class PromptTester:
    """A class for testing prompts and their optimizations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the PromptTester.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.test_history: List[Tuple[TestSuite, List[TestResult]]] = []
        
    def run_test_suite(
        self,
        test_suite: TestSuite,
        test_params: Optional[Dict[str, Any]] = None
    ) -> List[TestResult]:
        """Run a test suite.
        
        Args:
            test_suite (TestSuite): Test suite to run.
            test_params (Optional[Dict[str, Any]]): Test parameters.
            
        Returns:
            List[TestResult]: Test results.
        """
        params = test_params or {}
        results = []
        
        with ThreadPoolExecutor(max_workers=params.get('max_workers', 4)) as executor:
            futures = [
                executor.submit(self._run_test_case, test_case, params)
                for test_case in test_suite.test_cases
            ]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error running test case: {e}")
                    
        self.test_history.append((test_suite, results))
        return results
        
    def create_test_suite(
        self,
        name: str,
        test_cases: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
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
                prompt=case['prompt'],
                expected_output=case.get('expected_output'),
                context=case.get('context'),
                metadata=case.get('metadata')
            )
            suite_test_cases.append(test_case)
            
        return TestSuite(
            name=name,
            test_cases=suite_test_cases,
            metadata=metadata
        )
        
    def load_test_suite(self, file_path: Path) -> TestSuite:
        """Load a test suite from a file.
        
        Args:
            file_path (Path): Path to test suite file.
            
        Returns:
            TestSuite: Loaded test suite.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return self.create_test_suite(
            name=data['name'],
            test_cases=data['test_cases'],
            metadata=data.get('metadata')
        )
        
    def save_test_suite(self, test_suite: TestSuite, file_path: Path) -> None:
        """Save a test suite to a file.
        
        Args:
            test_suite (TestSuite): Test suite to save.
            file_path (Path): Path to save test suite.
        """
        data = {
            'name': test_suite.name,
            'test_cases': [
                {
                    'prompt': case.prompt,
                    'expected_output': case.expected_output,
                    'context': case.context,
                    'metadata': case.metadata
                }
                for case in test_suite.test_cases
            ],
            'metadata': test_suite.metadata
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    def get_test_stats(self) -> Dict[str, Any]:
        """Get statistics about test runs.
        
        Returns:
            Dict[str, Any]: Test statistics.
        """
        if not self.test_history:
            return {}
            
        total_tests = sum(
            len(results)
            for _, results in self.test_history
        )
        successful_tests = sum(
            sum(1 for result in results if result.success)
            for _, results in self.test_history
        )
        
        # Calculate average execution time
        execution_times = [
            result.execution_time
            for _, results in self.test_history
            for result in results
        ]
        avg_execution_time = (
            sum(execution_times) / len(execution_times)
            if execution_times else 0
        )
        
        return {
            'total_test_suites': len(self.test_history),
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': successful_tests / total_tests if total_tests > 0 else 0,
            'average_execution_time': avg_execution_time
        }
        
    def export_results(self, output_path: Path) -> None:
        """Export test results to a file.
        
        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            'statistics': self.get_test_stats(),
            'results': [
                {
                    'test_suite': {
                        'name': suite.name,
                        'metadata': suite.metadata
                    },
                    'test_results': [
                        {
                            'test_case': {
                                'prompt': result.test_case.prompt,
                                'expected_output': result.test_case.expected_output,
                                'context': result.test_case.context,
                                'metadata': result.test_case.metadata
                            },
                            'actual_output': result.actual_output,
                            'success': result.success,
                            'execution_time': result.execution_time,
                            'error': result.error,
                            'metadata': result.metadata
                        }
                        for result in results
                    ]
                }
                for suite, results in self.test_history
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2)
            
    def _run_test_case(
        self,
        test_case: TestCase,
        params: Dict[str, Any]
    ) -> TestResult:
        """Run a test case.
        
        Args:
            test_case (TestCase): Test case to run.
            params (Dict[str, Any]): Test parameters.
            
        Returns:
            TestResult: Test result.
        """
        start_time = time.time()
        error = None
        actual_output = None
        
        try:
            # Simulate model response
            actual_output = self._simulate_model_response(
                test_case.prompt,
                test_case.context,
                params
            )
            
            # Check if output matches expected
            success = (
                test_case.expected_output is None or
                actual_output == test_case.expected_output
            )
            
        except Exception as e:
            error = str(e)
            success = False
            
        execution_time = time.time() - start_time
        
        return TestResult(
            test_case=test_case,
            actual_output=actual_output,
            success=success,
            execution_time=execution_time,
            error=error,
            metadata={
                'timestamp': datetime.now().isoformat()
            }
        )
        
    def _simulate_model_response(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]],
        params: Dict[str, Any]
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
        time.sleep(random.uniform(0.1, 0.5))
        
        # For testing purposes, return a simple response
        return f"Response to: {prompt[:50]}..." 