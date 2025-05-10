#!/usr/bin/env python3
"""
Test runner for the Prompt Efficiency Suite.
This script ensures all components are running before executing tests.
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import pytest
        import requests
        import uvicorn

        from prompt_efficiency_suite import PromptAnalyzer
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False
    return True


def start_api_server():
    """Start the API server for testing."""
    server_process = subprocess.Popen(
        [
            "uvicorn",
            "prompt_efficiency_suite.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)  # Wait for server to start
    return server_process


def check_ide_plugins():
    """Check if IDE plugins are installed and running."""
    # Check JetBrains plugin
    jetbrains_plugin_path = Path.home() / ".IntelliJIdea" / "plugins" / "prompt-efficiency"
    if not jetbrains_plugin_path.exists():
        print("Warning: JetBrains plugin not found")

    # Check VS Code extension
    vscode_extension_path = Path.home() / ".vscode" / "extensions" / "prompt-efficiency"
    if not vscode_extension_path.exists():
        print("Warning: VS Code extension not found")


def run_tests():
    """Run all test suites."""
    # Run unit tests
    print("\nRunning unit tests...")
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/test_all_access_points.py", "-v"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print("Unit tests failed!")
        print(result.stderr)
        return False

    # Run integration tests
    print("\nRunning integration tests...")
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/test_integration.py", "-v"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print("Integration tests failed!")
        print(result.stderr)
        return False

    return True


def main():
    """Main test runner function."""
    print("Starting Prompt Efficiency Suite tests...")

    # Check dependencies
    if not check_dependencies():
        print("Please install all required dependencies first.")
        sys.exit(1)

    # Start API server
    print("\nStarting API server...")
    server_process = start_api_server()

    try:
        # Check IDE plugins
        print("\nChecking IDE plugins...")
        check_ide_plugins()

        # Run tests
        success = run_tests()

        if success:
            print("\nAll tests completed successfully!")
        else:
            print("\nSome tests failed. Please check the output above.")
            sys.exit(1)

    finally:
        # Clean up
        print("\nCleaning up...")
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    main()
