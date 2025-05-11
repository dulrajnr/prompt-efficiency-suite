#!/usr/bin/env python3

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import pkg_resources
import requests
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DependencyVerifier:
    def __init__(self):
        self.issues = []
        self.requirements_files = [
            "requirements.txt",
            "requirements-dev.txt",
            "requirements-test.txt",
        ]

    def get_installed_packages(self) -> Dict[str, str]:
        """Get currently installed packages and their versions."""
        return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

    def get_requirements(self) -> Dict[str, str]:
        """Get required packages and their versions from requirements files."""
        requirements = {}
        for req_file in self.requirements_files:
            if Path(req_file).exists():
                with open(req_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            try:
                                if "==" in line:
                                    pkg, version = line.split("==")
                                    requirements[pkg.lower()] = version
                                elif ">=" in line:
                                    pkg, version = line.split(">=")
                                    requirements[pkg.lower()] = f">={version}"
                                elif "<=" in line:
                                    pkg, version = line.split("<=")
                                    requirements[pkg.lower()] = f"<={version}"
                            except ValueError:
                                self.issues.append(
                                    f"Invalid requirement format in {req_file}: {line}"
                                )
        return requirements

    def check_package_versions(self) -> List[str]:
        """Check if installed packages match requirements."""
        issues = []
        installed = self.get_installed_packages()
        required = self.get_requirements()

        for pkg, version in required.items():
            if pkg not in installed:
                issues.append(f"Required package {pkg} is not installed")
            elif version.startswith(">="):
                min_version = version[2:]
                if pkg_resources.parse_version(
                    installed[pkg]
                ) < pkg_resources.parse_version(min_version):
                    issues.append(
                        f"Package {pkg} version {installed[pkg]} is below required minimum {min_version}"
                    )
            elif version.startswith("<="):
                max_version = version[2:]
                if pkg_resources.parse_version(
                    installed[pkg]
                ) > pkg_resources.parse_version(max_version):
                    issues.append(
                        f"Package {pkg} version {installed[pkg]} is above required maximum {max_version}"
                    )
            elif installed[pkg] != version:
                issues.append(
                    f"Package {pkg} version mismatch: installed {installed[pkg]}, required {version}"
                )

        return issues

    def check_pypi_updates(self) -> List[str]:
        """Check for available updates on PyPI."""
        issues = []
        installed = self.get_installed_packages()

        for pkg, version in installed.items():
            try:
                response = requests.get(f"https://pypi.org/pypi/{pkg}/json")
                if response.status_code == 200:
                    latest_version = response.json()["info"]["version"]
                    if pkg_resources.parse_version(
                        latest_version
                    ) > pkg_resources.parse_version(version):
                        issues.append(
                            f"Package {pkg} has update available: {version} -> {latest_version}"
                        )
            except Exception as e:
                self.issues.append(f"Error checking PyPI for {pkg}: {str(e)}")

        return issues

    def check_security_vulnerabilities(self) -> List[str]:
        """Check for known security vulnerabilities."""
        issues = []
        try:
            # Run safety check
            result = subprocess.run(
                ["safety", "check", "--json"], capture_output=True, text=True
            )
            if result.returncode != 0:
                vulnerabilities = json.loads(result.stdout)
                for vuln in vulnerabilities:
                    issues.append(
                        f"Security vulnerability in {vuln['package']} {vuln['installed_version']}: "
                        f"{vuln['description']}"
                    )
        except Exception as e:
            self.issues.append(f"Error running safety check: {str(e)}")

        return issues

    def check_dependency_conflicts(self) -> List[str]:
        """Check for dependency conflicts."""
        issues = []
        try:
            # Run pip check
            result = subprocess.run(["pip", "check"], capture_output=True, text=True)
            if result.returncode != 0:
                for line in result.stdout.splitlines():
                    issues.append(f"Dependency conflict: {line}")
        except Exception as e:
            self.issues.append(f"Error running pip check: {str(e)}")

        return issues

    def verify(self) -> Dict[str, Any]:
        """Run all dependency verification checks."""
        logger.info("Starting dependency verification...")

        self.issues.extend(self.check_package_versions())
        self.issues.extend(self.check_pypi_updates())
        self.issues.extend(self.check_security_vulnerabilities())
        self.issues.extend(self.check_dependency_conflicts())

        return {
            "total_issues": len(self.issues),
            "issues": self.issues,
            "status": "PASS" if not self.issues else "FAIL",
        }


def main():
    verifier = DependencyVerifier()
    results = verifier.verify()

    print("\nDependency Verification Results:")
    print("==============================")
    print(f"Status: {results['status']}")
    print(f"Total Issues: {results['total_issues']}")

    if results["issues"]:
        print("\nIssues Found:")
        for issue in results["issues"]:
            print(f"- {issue}")
    else:
        print("\nNo dependency issues found!")


if __name__ == "__main__":
    main()
