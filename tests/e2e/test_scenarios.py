#!/usr/bin/env python3

import json
import os
import subprocess
import time
import unittest
from pathlib import Path

import yaml


class PromptEfficiencyE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = Path("test_workspace")
        cls.test_dir.mkdir(exist_ok=True)

        # Create test files
        cls.create_test_files()

        # Set up configuration
        cls.setup_configuration()

    @classmethod
    def create_test_files(cls):
        """Create test files with prompts."""
        # Python file with prompts
        with open(cls.test_dir / "test_prompts.py", "w") as f:
            f.write(
                '''
prompt1 = """Write a function to calculate Fibonacci numbers"""
prompt2 = """Create a REST API endpoint for user authentication"""
prompt3 = """Implement a binary search tree in Python"""
'''
            )

        # JavaScript file with prompts
        with open(cls.test_dir / "test_prompts.js", "w") as f:
            f.write(
                """
const prompt1 = `Write a function to calculate Fibonacci numbers`;
const prompt2 = `Create a REST API endpoint for user authentication`;
const prompt3 = `Implement a binary search tree in JavaScript`;
"""
            )

    @classmethod
    def setup_configuration(cls):
        """Set up test configuration."""
        config_dir = Path.home() / ".prompt-efficiency"
        config_dir.mkdir(exist_ok=True)

        config = {
            "api_key": "test_api_key",
            "model": "gpt-4",
            "default_settings": {"temperature": 0.7, "max_tokens": 2000},
        }

        with open(config_dir / "config.yaml", "w") as f:
            yaml.dump(config, f)

    def test_installation(self):
        """Test complete installation process."""
        # Test pip installation
        result = subprocess.run(
            ["pip", "install", "prompt-efficiency-suite"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Pip installation failed")

        # Test verification
        result = subprocess.run(
            ["prompt-efficiency", "verify"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, "Verification failed")

    def test_prompt_analysis(self):
        """Test prompt analysis features."""
        # Test single prompt analysis
        result = subprocess.run(
            [
                "prompt-efficiency",
                "analyze",
                "Write a function to calculate Fibonacci numbers",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Single prompt analysis failed")

        # Test batch analysis
        result = subprocess.run(
            [
                "prompt-efficiency",
                "analyze-batch",
                str(self.test_dir / "test_prompts.py"),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Batch analysis failed")

    def test_prompt_optimization(self):
        """Test prompt optimization features."""
        # Test single prompt optimization
        result = subprocess.run(
            [
                "prompt-efficiency",
                "optimize",
                "Write a function to calculate Fibonacci numbers",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Single prompt optimization failed")

        # Test batch optimization
        result = subprocess.run(
            [
                "prompt-efficiency",
                "optimize-batch",
                str(self.test_dir / "test_prompts.py"),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Batch optimization failed")

    def test_repository_scanning(self):
        """Test repository scanning features."""
        # Test repository scan
        result = subprocess.run(
            ["prompt-efficiency", "scan", str(self.test_dir)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Repository scanning failed")

    def test_cost_management(self):
        """Test cost management features."""
        # Test cost estimation
        result = subprocess.run(
            [
                "prompt-efficiency",
                "estimate-cost",
                str(self.test_dir / "test_prompts.py"),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Cost estimation failed")

        # Test budget setting
        result = subprocess.run(
            ["prompt-efficiency", "budget", "--set", "1000"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, "Budget setting failed")

    def test_ide_integration(self):
        """Test IDE integration features."""
        # Test VS Code extension
        result = subprocess.run(
            ["code", "--list-extensions"], capture_output=True, text=True
        )
        self.assertIn(
            "prompt-efficiency-suite", result.stdout, "VS Code extension not found"
        )

        # Test JetBrains plugin
        if os.path.exists(
            os.path.expanduser("~/Library/Application Support/JetBrains")
        ):
            result = subprocess.run(
                ["ls", os.path.expanduser("~/Library/Application Support/JetBrains")],
                capture_output=True,
                text=True,
            )
            self.assertIn(
                "prompt-efficiency-suite", result.stdout, "JetBrains plugin not found"
            )

    def test_web_interface(self):
        """Test web interface features."""
        # Start web interface
        process = subprocess.Popen(
            ["prompt-efficiency", "web"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Wait for server to start
        time.sleep(5)

        # Test web interface
        result = subprocess.run(
            ["curl", "http://localhost:3000/health"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, "Web interface health check failed")

        # Stop web interface
        process.terminate()

    def test_error_handling(self):
        """Test error handling features."""
        # Test invalid API key
        config_path = Path.home() / ".prompt-efficiency" / "config.yaml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        config["api_key"] = "invalid_key"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        result = subprocess.run(
            ["prompt-efficiency", "analyze", "Test prompt"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0, "Invalid API key not detected")

        # Restore valid API key
        config["api_key"] = "test_api_key"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

    def test_performance(self):
        """Test performance features."""
        start_time = time.time()

        # Run performance test
        result = subprocess.run(
            [
                "prompt-efficiency",
                "analyze-batch",
                str(self.test_dir / "test_prompts.py"),
            ],
            capture_output=True,
            text=True,
        )

        end_time = time.time()
        execution_time = end_time - start_time

        self.assertEqual(result.returncode, 0, "Performance test failed")
        self.assertLess(execution_time, 30.0, "Performance test took too long")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        # Remove test directory
        if cls.test_dir.exists():
            for file in cls.test_dir.glob("*"):
                file.unlink()
            cls.test_dir.rmdir()

        # Remove test configuration
        config_dir = Path.home() / ".prompt-efficiency"
        if config_dir.exists():
            for file in config_dir.glob("*"):
                file.unlink()
            config_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
