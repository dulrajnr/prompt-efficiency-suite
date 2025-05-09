"""
Test suite for the CICDIntegration class.
"""

import pytest
from pathlib import Path
import json
import tempfile
from prompt_efficiency_suite.cicd_integration import CICDIntegration, TestResult, DeploymentResult

@pytest.fixture
def cicd():
    """Create a CICDIntegration instance for testing."""
    return CICDIntegration()

@pytest.fixture
def sample_config():
    """Create a sample CI/CD configuration."""
    return {
        'test_args': ['-v', '--tb=short'],
        'coverage': True
    }

@pytest.fixture
def temp_config_file(sample_config):
    """Create a temporary configuration file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_config, f)
        return f.name

def test_load_config(cicd, temp_config_file):
    """Test loading configuration file."""
    cicd = CICDIntegration(temp_config_file)
    assert cicd.config == {
        'test_args': ['-v', '--tb=short'],
        'coverage': True
    }

def test_load_invalid_config(cicd):
    """Test loading invalid configuration file."""
    with pytest.raises(FileNotFoundError):
        CICDIntegration('nonexistent.json')

def test_run_tests(cicd):
    """Test running tests."""
    result = cicd.run_tests()
    assert isinstance(result, TestResult)
    assert hasattr(result, 'passed')
    assert hasattr(result, 'total_tests')
    assert hasattr(result, 'passed_tests')
    assert hasattr(result, 'failed_tests')
    assert hasattr(result, 'coverage')
    assert hasattr(result, 'duration')

def test_run_tests_with_path(cicd):
    """Test running tests with specific path."""
    result = cicd.run_tests('tests/test_domain_aware_trimmer.py')
    assert isinstance(result, TestResult)

def test_run_tests_with_config(cicd, temp_config_file):
    """Test running tests with configuration."""
    cicd = CICDIntegration(temp_config_file)
    result = cicd.run_tests()
    assert isinstance(result, TestResult)
    assert hasattr(result, 'coverage')

def test_deploy_pypi(cicd):
    """Test deploying to PyPI."""
    with pytest.raises(subprocess.CalledProcessError):
        # This will fail without proper credentials
        cicd.deploy('0.1.0', 'pypi')

def test_deploy_github(cicd):
    """Test deploying to GitHub."""
    with pytest.raises(subprocess.CalledProcessError):
        # This will fail without proper credentials
        cicd.deploy('0.1.0', 'github')

def test_deploy_invalid_target(cicd):
    """Test deploying to invalid target."""
    with pytest.raises(ValueError):
        cicd.deploy('0.1.0', 'invalid_target')

def test_generate_report(cicd, tempfile):
    """Test generating report."""
    # Run some tests first
    cicd.run_tests()
    
    # Generate report
    report_path = tempfile.NamedTemporaryFile(suffix='.json', delete=False).name
    cicd.generate_report(report_path)
    
    # Verify report
    with open(report_path, 'r') as f:
        report = json.load(f)
        assert 'timestamp' in report
        assert 'test_results' in report
        assert 'deployment_results' in report

def test_generate_report_invalid_format(cicd):
    """Test generating report with invalid format."""
    with pytest.raises(ValueError):
        cicd.generate_report('report.txt')

def test_get_test_history(cicd):
    """Test getting test history."""
    # Run some tests
    cicd.run_tests()
    
    # Get history
    history = cicd.get_test_history()
    assert isinstance(history, list)
    assert all(isinstance(r, TestResult) for r in history)

def test_get_deployment_history(cicd):
    """Test getting deployment history."""
    history = cicd.get_deployment_history()
    assert isinstance(history, list)
    assert all(isinstance(r, DeploymentResult) for r in history) 