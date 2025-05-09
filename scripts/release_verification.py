#!/usr/bin/env python3

import subprocess
import json
import yaml
import sys
import os
import logging
from pathlib import Path
from typing import Dict, List, Any
import platform
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReleaseVerifier:
    def __init__(self):
        self.issues = []
        self.platform = platform.system().lower()
        self.python_version = platform.python_version()
        self.required_python = "3.8.0"

    def check_python_version(self) -> List[str]:
        """Check Python version compatibility."""
        issues = []
        if self.python_version < self.required_python:
            issues.append(f"Python version {self.python_version} is below required minimum {self.required_python}")
        return issues

    def check_installation(self) -> List[str]:
        """Test installation in a clean environment."""
        issues = []
        try:
            # Create temporary virtual environment
            venv_path = "test_venv"
            if os.path.exists(venv_path):
                shutil.rmtree(venv_path)
            
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            
            # Activate virtual environment and install package
            if self.platform == "windows":
                pip_path = os.path.join(venv_path, "Scripts", "pip")
                python_path = os.path.join(venv_path, "Scripts", "python")
            else:
                pip_path = os.path.join(venv_path, "bin", "pip")
                python_path = os.path.join(venv_path, "bin", "python")

            # Install package
            subprocess.run([pip_path, "install", "."], check=True)
            
            # Verify installation
            result = subprocess.run(
                [python_path, "-c", "import prompt_efficiency_suite; print(prompt_efficiency_suite.__version__)"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Clean up
            shutil.rmtree(venv_path)
            
        except subprocess.CalledProcessError as e:
            issues.append(f"Installation test failed: {str(e)}")
        except Exception as e:
            issues.append(f"Error during installation test: {str(e)}")
            
        return issues

    def run_tests(self) -> List[str]:
        """Run all test suites."""
        issues = []
        try:
            # Run unit tests
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                issues.append("Unit tests failed")
                issues.append(result.stdout)
                issues.append(result.stderr)

            # Run integration tests
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/integration/"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                issues.append("Integration tests failed")
                issues.append(result.stdout)
                issues.append(result.stderr)

            # Run end-to-end tests
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/e2e/"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                issues.append("End-to-end tests failed")
                issues.append(result.stdout)
                issues.append(result.stderr)

        except Exception as e:
            issues.append(f"Error running tests: {str(e)}")
            
        return issues

    def check_documentation(self) -> List[str]:
        """Verify documentation completeness and links."""
        issues = []
        required_docs = [
            "README.md",
            "docs/README.md",
            "docs/getting-started/installation.md",
            "docs/getting-started/quickstart.md",
            "docs/user-guide/overview.md",
            "docs/api/rest-api.md",
            "docs/examples/README.md",
            "CHANGELOG.md",
            "LICENSE"
        ]
        
        for doc in required_docs:
            if not os.path.exists(doc):
                issues.append(f"Missing required documentation: {doc}")
            else:
                # Check for broken links
                with open(doc, 'r') as f:
                    content = f.read()
                    # Simple link check - can be enhanced
                    if "](http://" in content:
                        issues.append(f"Found HTTP link in {doc} - should use HTTPS")

        return issues

    def check_version_consistency(self) -> List[str]:
        """Check version numbers are consistent across files."""
        issues = []
        version = None
        
        # Check setup.py
        with open("setup.py", 'r') as f:
            content = f.read()
            import re
            match = re.search(r'version="([^"]+)"', content)
            if match:
                version = match.group(1)
            else:
                issues.append("Could not find version in setup.py")

        # Check __init__.py
        init_path = "prompt_efficiency_suite/__init__.py"
        if os.path.exists(init_path):
            with open(init_path, 'r') as f:
                content = f.read()
                if f'__version__ = "{version}"' not in content:
                    issues.append(f"Version mismatch in {init_path}")

        # Check CHANGELOG.md
        with open("CHANGELOG.md", 'r') as f:
            content = f.read()
            if f"## [{version}]" not in content:
                issues.append(f"Version {version} not found in CHANGELOG.md")

        return issues

    def verify(self) -> Dict[str, Any]:
        """Run all release verification checks."""
        logger.info("Starting release verification...")
        
        self.issues.extend(self.check_python_version())
        self.issues.extend(self.check_installation())
        self.issues.extend(self.run_tests())
        self.issues.extend(self.check_documentation())
        self.issues.extend(self.check_version_consistency())

        return {
            "total_issues": len(self.issues),
            "issues": self.issues,
            "status": "PASS" if not self.issues else "FAIL"
        }

def main():
    verifier = ReleaseVerifier()
    results = verifier.verify()
    
    print("\nRelease Verification Results:")
    print("===========================")
    print(f"Status: {results['status']}")
    print(f"Total Issues: {results['total_issues']}")
    
    if results['issues']:
        print("\nIssues Found:")
        for issue in results['issues']:
            print(f"- {issue}")
    else:
        print("\nNo issues found! Ready for release!")

if __name__ == "__main__":
    main() 