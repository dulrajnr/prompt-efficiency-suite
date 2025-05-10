from pathlib import Path

import pytest

from prompt_efficiency_suite.macro_suggester import MacroSuggester, Suggestion


@pytest.fixture
def macro_suggester():
    return MacroSuggester()


@pytest.fixture
def sample_python_code():
    return '''
def complex_function(x, y):
    """This is a complex function with nested loops."""
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


def test_analyze_file(macro_suggester, tmp_path):
    # Create a temporary Python file
    file_path = tmp_path / "test.py"
    file_path.write_text(sample_python_code())

    # Analyze the file
    suggestions = macro_suggester.analyze_file(str(file_path))

    # Verify suggestions
    assert len(suggestions) > 0

    # Check for specific suggestion types
    suggestion_types = {s.type for s in suggestions}
    assert "function_length" in suggestion_types
    assert "complex_condition" in suggestion_types
    assert "class_length" in suggestion_types


def test_analyze_repository(macro_suggester, tmp_path):
    # Create a temporary repository structure
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    # Create some Python files
    (repo_path / "module1.py").write_text(sample_python_code())
    (repo_path / "module2.py").write_text(sample_python_code())

    # Create a non-Python file
    (repo_path / "README.md").write_text("# Test Repository")

    # Analyze the repository
    results = macro_suggester.analyze_repository(str(repo_path))

    # Verify results
    assert len(results) == 2  # Only Python files should be analyzed
    assert "module1.py" in results
    assert "module2.py" in results
    assert "README.md" not in results


def test_get_optimization_summary(macro_suggester, tmp_path):
    # Create a temporary Python file
    file_path = tmp_path / "test.py"
    file_path.write_text(sample_python_code())

    # Analyze the file
    suggestions = macro_suggester.analyze_file(str(file_path))

    # Create a results dictionary
    results = {str(file_path): suggestions}

    # Get optimization summary
    summary = macro_suggester.get_optimization_summary(results)

    # Verify summary
    assert summary["total_files"] == 1
    assert summary["total_suggestions"] > 0
    assert "suggestions_by_type" in summary
    assert "suggestions_by_severity" in summary

    # Verify severity counts
    severity_counts = summary["suggestions_by_severity"]
    assert "low" in severity_counts
    assert "medium" in severity_counts
    assert "high" in severity_counts


def test_suggestion_dataclass():
    # Test Suggestion dataclass
    suggestion = Suggestion(
        type="test",
        description="Test suggestion",
        severity="medium",
        location="test.py:1",
        suggestion="Test suggestion",
        code_snippet="test code",
    )

    assert suggestion.type == "test"
    assert suggestion.description == "Test suggestion"
    assert suggestion.severity == "medium"
    assert suggestion.location == "test.py:1"
    assert suggestion.suggestion == "Test suggestion"
    assert suggestion.code_snippet == "test code"


def test_analyze_complex_conditions(macro_suggester, tmp_path):
    # Create a Python file with complex conditions
    code = """
def test_function(x, y, z):
    if x > 0 and y > 0 and z > 0 and x < y and y < z:
        return True
    return False
"""
    file_path = tmp_path / "complex.py"
    file_path.write_text(code)

    # Analyze the file
    suggestions = macro_suggester.analyze_file(str(file_path))

    # Verify complex condition suggestion
    complex_conditions = [s for s in suggestions if s.type == "complex_condition"]
    assert len(complex_conditions) > 0


def test_analyze_nested_loops(macro_suggester, tmp_path):
    # Create a Python file with nested loops
    code = """
def nested_loops():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)
"""
    file_path = tmp_path / "nested.py"
    file_path.write_text(code)

    # Analyze the file
    suggestions = macro_suggester.analyze_file(str(file_path))

    # Verify nested loops suggestion
    nested_loops = [s for s in suggestions if s.type == "repeated_loops"]
    assert len(nested_loops) > 0
