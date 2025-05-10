from pathlib import Path

import pytest

from prompt_efficiency_suite.repository_scanner import FileAnalysis, RepositoryAnalysis, RepositoryScanner


@pytest.fixture
def scanner():
    return RepositoryScanner()


@pytest.fixture
def sample_repo(tmp_path):
    # Create a temporary repository structure
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    # Create Python files
    (repo_path / "module1.py").write_text(
        '''
import os
import sys

def complex_function(x, y):
    """A complex function with nested loops."""
    result = 0
    for i in range(x):
        for j in range(y):
            if i > 0 and j > 0 and x > y:
                result += i * j
    return result

class LargeClass:
    def __init__(self):
        self.data = []

    def add_data(self, item):
        self.data.append(item)

    def process_data(self):
        for item in self.data:
            if item > 0 and item < 100 and item % 2 == 0:
                print(item)
    '''
    )

    (repo_path / "module2.py").write_text(
        """
from module1 import complex_function

def another_function():
    return complex_function(5, 5)
    """
    )

    # Create JSON file
    (repo_path / "config.json").write_text(
        """
    {
        "name": "Test Project",
        "version": "1.0.0",
        "dependencies": {
            "package1": "^1.0.0",
            "package2": "^2.0.0"
        }
    }
    """
    )

    # Create YAML file
    (repo_path / "config.yaml").write_text(
        """
    name: Test Project
    version: 1.0.0
    dependencies:
      package1: ^1.0.0
      package2: ^2.0.0
    """
    )

    # Create Markdown file
    (repo_path / "README.md").write_text(
        """
    # Test Project

    This is a test project with multiple file types.

    ## Features

    - Feature 1
    - Feature 2

    ```python
    def example():
        pass
    ```
    """
    )

    return repo_path


def test_scan_repository(scanner, sample_repo):
    # Scan the repository
    analysis = scanner.scan_repository(str(sample_repo))

    # Verify basic analysis results
    assert isinstance(analysis, RepositoryAnalysis)
    assert analysis.total_files > 0
    assert analysis.total_lines > 0
    assert analysis.total_size > 0

    # Verify file types
    assert "python" in analysis.file_types
    assert "json" in analysis.file_types
    assert "yaml" in analysis.file_types
    assert "markdown" in analysis.file_types


def test_file_analysis(scanner, sample_repo):
    # Get analysis for a specific file
    analysis = scanner.scan_repository(str(sample_repo))
    module1_analysis = analysis.file_analyses[str(sample_repo / "module1.py")]

    # Verify file analysis
    assert isinstance(module1_analysis, FileAnalysis)
    assert module1_analysis.content_type == "python"
    assert module1_analysis.line_count > 0
    assert module1_analysis.complexity > 0
    assert len(module1_analysis.dependencies) > 0
    assert len(module1_analysis.patterns) > 0
    assert len(module1_analysis.suggestions) > 0


def test_dependency_analysis(scanner, sample_repo):
    # Scan the repository
    analysis = scanner.scan_repository(str(sample_repo))

    # Verify Python dependencies
    python_deps = analysis.dependencies.get("python", set())
    assert "os" in python_deps
    assert "sys" in python_deps
    assert "module1" in python_deps


def test_pattern_analysis(scanner, sample_repo):
    # Scan the repository
    analysis = scanner.scan_repository(str(sample_repo))

    # Verify Python patterns
    python_patterns = analysis.patterns.get("imports", [])
    assert len(python_patterns) > 0

    # Verify JSON patterns
    json_patterns = analysis.patterns.get("objects", [])
    assert len(json_patterns) > 0

    # Verify YAML patterns
    yaml_patterns = analysis.patterns.get("keys", [])
    assert len(yaml_patterns) > 0

    # Verify Markdown patterns
    markdown_patterns = analysis.patterns.get("headers", [])
    assert len(markdown_patterns) > 0


def test_suggestion_generation(scanner, sample_repo):
    # Scan the repository
    analysis = scanner.scan_repository(str(sample_repo))

    # Verify suggestions
    assert len(analysis.suggestions) > 0

    # Check for specific suggestion types
    suggestion_types = {s["type"] for s in analysis.suggestions}
    assert "complexity" in suggestion_types
    assert "imports" in suggestion_types


def test_exclude_patterns(scanner, sample_repo):
    # Create a file that should be excluded
    (sample_repo / "__pycache__").mkdir()
    (sample_repo / "__pycache__" / "module1.pyc").write_text("")

    # Scan with default exclude patterns
    analysis = scanner.scan_repository(str(sample_repo))

    # Verify excluded file is not in analysis
    assert str(sample_repo / "__pycache__" / "module1.pyc") not in analysis.file_analyses


def test_complexity_calculation(scanner, sample_repo):
    # Scan the repository
    analysis = scanner.scan_repository(str(sample_repo))

    # Get analysis for the complex Python file
    module1_analysis = analysis.file_analyses[str(sample_repo / "module1.py")]

    # Verify complexity calculation
    assert module1_analysis.complexity > 0

    # Get analysis for the simpler Python file
    module2_analysis = analysis.file_analyses[str(sample_repo / "module2.py")]

    # Verify that module1 has higher complexity than module2
    assert module1_analysis.complexity > module2_analysis.complexity


def test_structure_analysis(scanner, sample_repo):
    # Scan the repository
    analysis = scanner.scan_repository(str(sample_repo))

    # Get analysis for JSON file
    json_analysis = analysis.file_analyses[str(sample_repo / "config.json")]

    # Verify JSON structure analysis
    assert json_analysis.complexity > 0

    # Get analysis for YAML file
    yaml_analysis = analysis.file_analyses[str(sample_repo / "config.yaml")]

    # Verify YAML structure analysis
    assert yaml_analysis.complexity > 0
