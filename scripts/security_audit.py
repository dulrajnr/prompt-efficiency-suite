#!/usr/bin/env python3

import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List

import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityAudit:
    def __init__(self):
        self.issues = []
        self.config_paths = [
            "~/.prompt-efficiency/config.yaml",
            "config.yaml",
            ".env",
            "prompt_efficiency_suite/config.yaml",
        ]
        # More specific patterns for sensitive data
        self.sensitive_patterns = [
            r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]",  # API keys with values
            r"secret\s*=\s*['\"][^'\"]+['\"]",  # Secrets with values
            r"password\s*=\s*['\"][^'\"]+['\"]",  # Passwords with values
            r"token\s*=\s*['\"][^'\"]+['\"]",  # Tokens with values
            r"credential\s*=\s*['\"][^'\"]+['\"]",  # Credentials with values
            r"private[_-]?key\s*=\s*['\"][^'\"]+['\"]",  # Private keys with values
        ]
        # Environment variables to ignore
        self.ignored_env_vars = {
            "SSH_AUTH_SOCK",
            "PATH",
            "HOME",
            "USER",
            "SHELL",
            "TERM",
            "LANG",
            "LC_ALL",
            "PYTHONPATH",
            "VIRTUAL_ENV",
        }

    def check_api_key_handling(self) -> List[str]:
        """Check API key handling in code and configuration."""
        issues = []

        # Check configuration files
        for config_path in self.config_paths:
            full_path = os.path.expanduser(config_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path, "r") as f:
                        content = f.read()
                        # Check for actual API key values, not just comments
                        if any(re.search(pattern, content, re.I) for pattern in self.sensitive_patterns):
                            issues.append(f"Potential sensitive data in {config_path}")
                except Exception as e:
                    issues.append(f"Error reading {config_path}: {str(e)}")

        # Check for hardcoded API keys in code
        for root, _, files in os.walk("prompt_efficiency_suite"):
            for file in files:
                if file.endswith((".py", ".kt", ".java")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()
                            if any(re.search(pattern, content, re.I) for pattern in self.sensitive_patterns):
                                issues.append(f"Potential hardcoded sensitive data in {file_path}")
                    except Exception as e:
                        issues.append(f"Error reading {file_path}: {str(e)}")

        return issues

    def check_file_permissions(self) -> List[str]:
        """Check file permissions for sensitive files."""
        issues = []

        for config_path in self.config_paths:
            full_path = os.path.expanduser(config_path)
            if os.path.exists(full_path):
                try:
                    mode = os.stat(full_path).st_mode
                    if mode & 0o777 != 0o600:  # Should be readable only by owner
                        issues.append(f"Insecure permissions on {config_path}: {oct(mode & 0o777)}")
                except Exception as e:
                    issues.append(f"Error checking permissions on {config_path}: {str(e)}")

        return issues

    def check_environment_variables(self) -> List[str]:
        """Check environment variable handling."""
        issues = []

        # Check for sensitive environment variables
        for key in os.environ:
            if key in self.ignored_env_vars:
                continue
            if any(re.search(pattern, key, re.I) for pattern in self.sensitive_patterns):
                issues.append(f"Sensitive environment variable found: {key}")

        return issues

    def check_network_security(self) -> List[str]:
        """Check network security settings."""
        issues = []

        # Check for hardcoded URLs
        for root, _, files in os.walk("prompt_efficiency_suite"):
            for file in files:
                if file.endswith((".py", ".kt", ".java")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()
                            if re.search(r"http://", content):
                                issues.append(f"Insecure HTTP URL found in {file_path}")
                    except Exception as e:
                        issues.append(f"Error reading {file_path}: {str(e)}")

        return issues

    def check_input_validation(self) -> List[str]:
        """Check input validation in code."""
        issues = []

        for root, _, files in os.walk("prompt_efficiency_suite"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()
                            # Check for potential SQL injection
                            if re.search(r"SELECT.*FROM.*WHERE.*%s", content):
                                issues.append(f"Potential SQL injection in {file_path}")
                            # Check for potential command injection
                            if re.search(r"os\.system|subprocess\.call", content):
                                issues.append(f"Potential command injection in {file_path}")
                    except Exception as e:
                        issues.append(f"Error reading {file_path}: {str(e)}")

        return issues

    def run_audit(self) -> Dict[str, Any]:
        """Run all security checks."""
        logger.info("Starting security audit...")

        self.issues.extend(self.check_api_key_handling())
        self.issues.extend(self.check_file_permissions())
        self.issues.extend(self.check_environment_variables())
        self.issues.extend(self.check_network_security())
        self.issues.extend(self.check_input_validation())

        return {
            "total_issues": len(self.issues),
            "issues": self.issues,
            "status": "PASS" if not self.issues else "FAIL",
        }


def main():
    audit = SecurityAudit()
    results = audit.run_audit()

    print("\nSecurity Audit Results:")
    print("======================")
    print(f"Status: {results['status']}")
    print(f"Total Issues: {results['total_issues']}")

    if results["issues"]:
        print("\nIssues Found:")
        for issue in results["issues"]:
            print(f"- {issue}")
    else:
        print("\nNo security issues found!")


if __name__ == "__main__":
    main()
