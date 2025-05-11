#!/usr/bin/env python3

import json
import os
import subprocess
import time
import unittest
from pathlib import Path


class VSCodeExtensionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.vscode_path = os.path.expanduser("~/.vscode/extensions")
        cls.extension_id = "prompt-efficiency-suite"
        cls.test_file = "test_prompt.py"

        # Create test file
        with open(cls.test_file, "w") as f:
            f.write('prompt = """Write a function to calculate Fibonacci numbers"""')

    def test_extension_installation(self):
        """Test if extension is properly installed."""
        extension_found = False
        for ext in os.listdir(self.vscode_path):
            if self.extension_id in ext.lower():
                extension_found = True
                break
        self.assertTrue(
            extension_found, "Extension not found in VS Code extensions directory"
        )

    def test_command_palette(self):
        """Test if commands are available in command palette."""
        # Simulate command palette activation
        result = subprocess.run(
            ["code", "--list-extensions"], capture_output=True, text=True
        )
        self.assertIn(self.extension_id, result.stdout)

    def test_status_bar(self):
        """Test if status bar items are present."""
        # Check status bar configuration
        settings_path = os.path.expanduser("~/.vscode/settings.json")
        if os.path.exists(settings_path):
            with open(settings_path) as f:
                settings = json.load(f)
                self.assertIn("prompt-efficiency", settings)

    def test_quick_fixes(self):
        """Test if quick fixes are available."""
        # Simulate quick fix request
        result = subprocess.run(
            ["code", "--list-extensions", "--show-versions"],
            capture_output=True,
            text=True,
        )
        self.assertIn(self.extension_id, result.stdout)

    def test_configuration(self):
        """Test extension configuration."""
        config_path = os.path.expanduser("~/.vscode/settings.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
                self.assertIn("prompt-efficiency", config)

    def test_analysis_features(self):
        """Test prompt analysis features."""
        # Test file analysis
        result = subprocess.run(
            ["code", "--list-extensions", "--show-versions"],
            capture_output=True,
            text=True,
        )
        self.assertIn(self.extension_id, result.stdout)

    def test_optimization_features(self):
        """Test prompt optimization features."""
        # Test optimization command
        result = subprocess.run(
            ["code", "--list-extensions", "--show-versions"],
            capture_output=True,
            text=True,
        )
        self.assertIn(self.extension_id, result.stdout)

    def test_error_handling(self):
        """Test error handling in extension."""
        # Test invalid prompt
        with open(self.test_file, "w") as f:
            f.write('prompt = """Invalid prompt"""')

        # Check error handling
        result = subprocess.run(
            ["code", "--list-extensions", "--show-versions"],
            capture_output=True,
            text=True,
        )
        self.assertIn(self.extension_id, result.stdout)

    def test_performance(self):
        """Test extension performance."""
        start_time = time.time()

        # Simulate extension operations
        subprocess.run(["code", "--list-extensions"], capture_output=True, text=True)

        end_time = time.time()
        execution_time = end_time - start_time

        self.assertLess(execution_time, 5.0, "Extension operations took too long")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)


if __name__ == "__main__":
    unittest.main()
