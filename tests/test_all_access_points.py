import json
import subprocess
import unittest
from pathlib import Path

import pytest
import requests

from prompt_efficiency_suite import (
    AdaptiveBudgeting,
    CICDIntegration,
    CodeAwareCompressor,
    DomainAwareTrimmer,
    PromptAnalyzer,
)


class TestAllAccessPoints(unittest.TestCase):
    """Test suite for all Prompt Efficiency Suite access points."""

    def setUp(self):
        """Set up test environment."""
        self.test_prompt = "You are a helpful assistant. Please help with: {task}"
        self.api_base_url = "http://localhost:8000/api/v1"
        self.test_data_dir = Path(".prompt_efficiency_data")
        self.test_data_dir.mkdir(exist_ok=True)

    def test_01_cli_commands(self):
        """Test CLI functionality."""
        # Test basic commands
        result = subprocess.run(
            ["prompt-efficiency", "--help"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)

        # Test benchmark creation
        result = subprocess.run(
            ["prompt-efficiency", "benchmark", "create-task", "TEST_TASK", "Test Task"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        task_id = json.loads(result.stdout)["task_id"]

        # Test benchmark submission
        result = subprocess.run(
            [
                "prompt-efficiency",
                "benchmark",
                "submit",
                task_id,
                self.test_prompt,
                "gpt-4",
                "--accuracy",
                "0.95",
                "--latency-ms",
                "100",
                "--cost-per-token",
                "0.01",
                "--token-count",
                "50",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)

    def test_02_python_sdk(self):
        """Test Python SDK functionality."""
        # Initialize components
        analyzer = PromptAnalyzer()
        trimmer = DomainAwareTrimmer()
        budget_tracker = AdaptiveBudgeting()
        compressor = CodeAwareCompressor()

        # Test prompt analysis
        analysis_result = analyzer.analyze_prompt(self.test_prompt)
        self.assertIsNotNone(analysis_result)
        self.assertIn("quality_score", analysis_result)

        # Test trimming
        trimmed = trimmer.trim(
            text=self.test_prompt,
            preserve_ratio=0.8,
            domain_terms=["assistant", "help"],
        )
        self.assertIsNotNone(trimmed)
        self.assertLess(len(trimmed), len(self.test_prompt))

        # Test budget tracking
        budget_result = budget_tracker.track_usage(
            prompt=self.test_prompt, model="gpt-4", tokens=150
        )
        self.assertIsNotNone(budget_result)
        self.assertIn("remaining_budget", budget_result)

        # Test code compression
        code_prompt = (
            self.test_prompt + "\n```python\ndef hello():\n    print('Hello')\n```"
        )
        compressed = compressor.compress(prompt=code_prompt, language="python")
        self.assertIsNotNone(compressed)
        self.assertLess(len(compressed), len(code_prompt))

    def test_03_rest_api(self):
        """Test REST API functionality."""
        # Test API health
        response = requests.get(f"{self.api_base_url}/health")
        self.assertEqual(response.status_code, 200)

        # Test prompt analysis
        response = requests.post(
            f"{self.api_base_url}/analyze", json={"prompt": self.test_prompt}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("quality_score", response.json())

        # Test quick analysis
        response = requests.post(
            f"{self.api_base_url}/analyze/quick", json={"prompt": self.test_prompt}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token_count", response.json())

    def test_04_jetbrains_plugin(self):
        """Test JetBrains plugin functionality."""
        # Note: This test requires a running IDE instance
        # We'll test the plugin's core functionality through its API
        from prompt_efficiency_suite.ide import JetBrainsPluginAPI

        plugin_api = JetBrainsPluginAPI()

        # Test pattern management
        pattern_result = plugin_api.create_pattern(
            name="Test Pattern", template=self.test_prompt, category="test"
        )
        self.assertIsNotNone(pattern_result)
        self.assertIn("pattern_id", pattern_result)

        # Test cost analytics
        analytics_result = plugin_api.get_cost_analytics()
        self.assertIsNotNone(analytics_result)
        self.assertIn("total_cost", analytics_result)

    def test_05_vscode_extension(self):
        """Test VS Code extension functionality."""
        # Note: This test requires a running VS Code instance
        # We'll test the extension's core functionality through its API
        from prompt_efficiency_suite.ide import VSCodeExtensionAPI

        extension_api = VSCodeExtensionAPI()

        # Test inline suggestions
        suggestions = extension_api.get_inline_suggestions(self.test_prompt)
        self.assertIsNotNone(suggestions)
        self.assertIsInstance(suggestions, list)

        # Test token count display
        token_count = extension_api.get_token_count(self.test_prompt)
        self.assertIsNotNone(token_count)
        self.assertIsInstance(token_count, int)

    def test_06_web_ui(self):
        """Test Web UI functionality."""
        # Test web UI endpoints
        response = requests.get(f"{self.api_base_url}/ui/dashboard")
        self.assertEqual(response.status_code, 200)

        # Test benchmark leaderboard
        response = requests.get(f"{self.api_base_url}/ui/leaderboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("benchmarks", response.json())

        # Test dictionary health
        response = requests.get(f"{self.api_base_url}/ui/dictionary/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    def test_07_grafana_integration(self):
        """Test Grafana integration."""
        # Test metrics endpoint
        response = requests.get(f"{self.api_base_url}/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn("prompt_efficiency_", response.text)

        # Test dashboard data
        response = requests.get(f"{self.api_base_url}/grafana/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("panels", response.json())

    def tearDown(self):
        """Clean up test environment."""
        # Clean up test data
        if self.test_data_dir.exists():
            for file in self.test_data_dir.glob("*"):
                file.unlink()
            self.test_data_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
