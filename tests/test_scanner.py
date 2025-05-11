from pathlib import Path

import pytest

from prompt_efficiency_suite.scanner import RepositoryScanner


def test_scanner_initialization() -> None:
    """Test scanner initialization."""
    scanner = RepositoryScanner()
    assert scanner is not None


def test_scan_repository() -> None:
    """Test scanning a repository."""
    scanner = RepositoryScanner()
    repo_path = Path("tests/test_repo")
    results = scanner.scan(repo_path)
    assert isinstance(results, list)
    assert all(isinstance(r, dict) for r in results)
    assert all("file_path" in r for r in results)
    assert all("prompts" in r for r in results)


def test_scan_file() -> None:
    """Test scanning a single file."""
    scanner = RepositoryScanner()
    file_path = Path("tests/test_repo/test_file.py")
    results = scanner._scan_file(file_path)
    assert isinstance(results, dict)
    assert "file_path" in results
    assert "prompts" in results
    assert isinstance(results["prompts"], list)


def test_is_python_file() -> None:
    """Test checking if a file is a Python file."""
    scanner = RepositoryScanner()
    assert scanner._is_python_file(Path("test.py")) is True
    assert scanner._is_python_file(Path("test.txt")) is False
    assert scanner._is_python_file(Path("test.pyc")) is False


def test_extract_prompts() -> None:
    """Test extracting prompts from a file."""
    scanner = RepositoryScanner()
    content = '''
    prompt = "This is a test prompt"
    another_prompt = """This is a multi-line
    test prompt"""
    '''
    prompts = scanner._extract_prompts(content)
    assert isinstance(prompts, list)
    assert len(prompts) == 2
    assert "This is a test prompt" in prompts
    assert "This is a multi-line\ntest prompt" in prompts
