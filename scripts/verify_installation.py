#!/usr/bin/env python3

import importlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import pkg_resources


class InstallationVerifier:
    def __init__(self):
        self.system = platform.system()
        self.python_version = platform.python_version()
        self.checks = {
            "core": [],
            "extensions": [],
            "dependencies": [],
            "configuration": [],
        }
        self.results = {"status": "pending", "checks": {}, "errors": [], "warnings": []}

    def check_python_version(self):
        """Verify Python version compatibility."""
        required_version = (3, 8)
        current_version = tuple(map(int, self.python_version.split(".")))

        if current_version < required_version:
            self.results["errors"].append(
                f"Python version {self.python_version} is not supported. "
                f"Required version: {'.'.join(map(str, required_version))} or higher."
            )
            return False
        return True

    def check_core_installation(self):
        """Verify core package installation."""
        try:
            import prompt_efficiency_suite

            version = pkg_resources.get_distribution("prompt-efficiency-suite").version
            self.checks["core"].append({"name": "Core Package", "status": "success", "version": version})
            return True
        except ImportError:
            self.results["errors"].append("Core package not installed correctly.")
            return False

    def check_vscode_extension(self):
        """Verify VS Code extension installation."""
        if self.system == "Windows":
            extension_path = os.path.expanduser("~/.vscode/extensions")
        else:
            extension_path = os.path.expanduser("~/.vscode/extensions")

        if not os.path.exists(extension_path):
            self.results["warnings"].append("VS Code extensions directory not found.")
            return False

        # Check for our extension
        extension_found = False
        for ext in os.listdir(extension_path):
            if "prompt-efficiency-suite" in ext.lower():
                extension_found = True
                break

        self.checks["extensions"].append(
            {
                "name": "VS Code Extension",
                "status": "success" if extension_found else "warning",
                "message": "Extension found" if extension_found else "Extension not found",
            }
        )
        return extension_found

    def check_jetbrains_plugin(self):
        """Verify JetBrains plugin installation."""
        if self.system == "Windows":
            plugin_path = os.path.expanduser("~/AppData/Roaming/JetBrains")
        elif self.system == "Darwin":
            plugin_path = os.path.expanduser("~/Library/Application Support/JetBrains")
        else:
            plugin_path = os.path.expanduser("~/.config/JetBrains")

        if not os.path.exists(plugin_path):
            self.results["warnings"].append("JetBrains configuration directory not found.")
            return False

        # Check for our plugin
        plugin_found = False
        for root, dirs, files in os.walk(plugin_path):
            if "prompt-efficiency-suite" in str(files).lower():
                plugin_found = True
                break

        self.checks["extensions"].append(
            {
                "name": "JetBrains Plugin",
                "status": "success" if plugin_found else "warning",
                "message": "Plugin found" if plugin_found else "Plugin not found",
            }
        )
        return plugin_found

    def check_dependencies(self):
        """Verify all required dependencies."""
        required_packages = [
            "requests",
            "numpy",
            "pandas",
            "scikit-learn",
            "transformers",
            "torch",
        ]

        for package in required_packages:
            try:
                version = pkg_resources.get_distribution(package).version
                self.checks["dependencies"].append({"name": package, "status": "success", "version": version})
            except pkg_resources.DistributionNotFound:
                self.results["errors"].append(f"Required package {package} not found.")
                return False
        return True

    def check_configuration(self):
        """Verify configuration files and settings."""
        config_path = os.path.expanduser("~/.prompt-efficiency/config.yaml")

        if not os.path.exists(config_path):
            self.results["warnings"].append("Configuration file not found.")
            return False

        try:
            import yaml

            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

            required_keys = ["api_key", "model", "default_settings"]
            missing_keys = [key for key in required_keys if key not in config]

            if missing_keys:
                self.results["errors"].append(f"Missing required configuration keys: {', '.join(missing_keys)}")
                return False

            self.checks["configuration"].append(
                {
                    "name": "Configuration",
                    "status": "success",
                    "message": "Configuration file valid",
                }
            )
            return True
        except Exception as e:
            self.results["errors"].append(f"Error reading configuration: {str(e)}")
            return False

    def run_checks(self):
        """Run all verification checks."""
        checks = [
            self.check_python_version,
            self.check_core_installation,
            self.check_vscode_extension,
            self.check_jetbrains_plugin,
            self.check_dependencies,
            self.check_configuration,
        ]

        all_passed = True
        for check in checks:
            if not check():
                all_passed = False

        self.results["status"] = "success" if all_passed else "failed"
        return self.results

    def print_results(self):
        """Print verification results in a user-friendly format."""
        print("\n=== Prompt Efficiency Suite Installation Verification ===\n")

        print(f"System: {self.system}")
        print(f"Python Version: {self.python_version}\n")

        for category, checks in self.checks.items():
            if checks:
                print(f"\n{category.upper()} CHECKS:")
                for check in checks:
                    status = "✓" if check["status"] == "success" else "⚠" if check["status"] == "warning" else "✗"
                    print(f"{status} {check['name']}")
                    if "version" in check:
                        print(f"   Version: {check['version']}")
                    if "message" in check:
                        print(f"   {check['message']}")

        if self.results["errors"]:
            print("\nERRORS:")
            for error in self.results["errors"]:
                print(f"✗ {error}")

        if self.results["warnings"]:
            print("\nWARNINGS:")
            for warning in self.results["warnings"]:
                print(f"⚠ {warning}")

        print(f"\nOverall Status: {self.results['status'].upper()}")


def main():
    verifier = InstallationVerifier()
    results = verifier.run_checks()
    verifier.print_results()

    # Exit with appropriate status code
    sys.exit(0 if results["status"] == "success" else 1)


if __name__ == "__main__":
    main()
