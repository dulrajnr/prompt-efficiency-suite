"""
End-to-end tests for the Prompt Efficiency Suite.
"""

import json
import os
from pathlib import Path

import pytest

from prompt_efficiency_suite import AdaptiveBudgeting, CICDIntegration, DomainAwareTrimmer


class TestEndToEnd:
    """End-to-end test scenarios."""

    @pytest.fixture
    def domain_dict_path(self, tmp_path):
        """Create a temporary domain dictionary file."""
        domain_dict = {
            "terms": ["API", "token", "model", "GPT", "prompt"],
            "compound_terms": ["machine learning", "natural language"],
            "preserve_patterns": [r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"],
            "remove_patterns": [r"\s+"],
        }
        path = tmp_path / "domain.json"
        with open(path, "w") as f:
            json.dump(domain_dict, f)
        return str(path)

    def test_domain_aware_trimming(self, domain_dict_path):
        """Test domain-aware text trimming functionality."""
        trimmer = DomainAwareTrimmer()
        trimmer.load_domain("technical", domain_dict_path)

        test_text = """
        This is a test prompt about machine learning and natural language processing.
        The GPT model requires API tokens for processing. Contact support@example.com
        for more information about token usage and prompt optimization.
        """

        result = trimmer.trim(test_text, domain="technical", preserve_ratio=0.7)

        assert result.trimmed_text != ""
        assert "machine learning" in result.preserved_terms
        assert "natural language" in result.preserved_terms
        assert "GPT" in result.preserved_terms
        assert "API" in result.preserved_terms
        assert "support@example.com" in result.preserved_terms
        assert result.compression_ratio <= 1.0
        assert result.compression_ratio >= 0.5

    def test_adaptive_budgeting(self):
        """Test adaptive budgeting functionality."""
        budgeting = AdaptiveBudgeting()

        # Track usage for GPT-4
        budgeting.track_usage("gpt-4", tokens=1000, cost=0.5)
        budgeting.track_usage("gpt-4", tokens=2000, cost=1.0)

        # Track usage for GPT-3.5-turbo
        budgeting.track_usage("gpt-3.5-turbo", tokens=5000, cost=0.25)
        budgeting.track_usage("gpt-3.5-turbo", tokens=10000, cost=0.5)

        # Get metrics for GPT-4
        gpt4_metrics = budgeting.get_metrics("gpt-4")[0]
        assert gpt4_metrics["total_tokens"] == 3000
        assert gpt4_metrics["total_cost"] == 1.5
        assert gpt4_metrics["peak_tokens"] == 2000
        assert gpt4_metrics["peak_cost"] == 1.0
        assert gpt4_metrics["average_tokens_per_request"] == 1500
        assert gpt4_metrics["average_cost_per_request"] == 0.75

        # Get metrics for GPT-3.5-turbo
        gpt35_metrics = budgeting.get_metrics("gpt-3.5-turbo")[0]
        assert gpt35_metrics["total_tokens"] == 15000
        assert gpt35_metrics["total_cost"] == 0.75
        assert gpt35_metrics["peak_tokens"] == 10000
        assert gpt35_metrics["peak_cost"] == 0.5
        assert gpt35_metrics["average_tokens_per_request"] == 7500
        assert gpt35_metrics["average_cost_per_request"] == 0.375

        # Check alerts
        alerts = budgeting.get_alerts()
        assert len(alerts) > 0  # Should have alerts for exceeding thresholds

    def test_cicd_integration(self, tmp_path):
        """Test CI/CD integration functionality."""
        cicd = CICDIntegration()

        # Run tests
        test_results = cicd.run_tests()
        assert isinstance(test_results, dict)
        assert "passed_tests" in test_results
        assert "failed_tests" in test_results
        assert "coverage" in test_results
        assert "duration" in test_results
        assert "output" in test_results

        # Test deployment
        deploy_results = cicd.deploy("test")
        assert isinstance(deploy_results, dict)
        assert deploy_results["status"] in ["success", "failed"]
        assert "version" in deploy_results
        assert "duration" in deploy_results
        assert "artifacts" in deploy_results
        assert "logs" in deploy_results
