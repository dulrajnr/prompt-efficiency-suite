"""
Test suite for the AdaptiveBudgeting class.
"""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from prompt_efficiency_suite.adaptive_budgeting import AdaptiveBudgeting, BudgetAlert, BudgetMetrics


@pytest.fixture
def budgeting():
    """Create an AdaptiveBudgeting instance for testing."""
    return AdaptiveBudgeting()


@pytest.fixture
def sample_config():
    """Create a sample budget configuration."""
    return {
        "monitoring_interval": 60,
        "thresholds": {
            "gpt-4": {"max_tokens": 1000000, "max_cost": 100.0},
            "gpt-3.5-turbo": {"max_tokens": 2000000, "max_cost": 50.0},
        },
        "notifications": {"enabled": True, "channels": ["email", "slack"]},
    }


@pytest.fixture
def temp_config_file(sample_config):
    """Create a temporary configuration file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample_config, f)
        return f.name


def test_load_config(budgeting, temp_config_file):
    """Test loading configuration file."""
    budgeting = AdaptiveBudgeting(temp_config_file)
    assert budgeting.config == {
        "monitoring_interval": 60,
        "thresholds": {
            "gpt-4": {"max_tokens": 1000000, "max_cost": 100.0},
            "gpt-3.5-turbo": {"max_tokens": 2000000, "max_cost": 50.0},
        },
        "notifications": {"enabled": True, "channels": ["email", "slack"]},
    }


def test_load_invalid_config(budgeting):
    """Test loading invalid configuration file."""
    with pytest.raises(FileNotFoundError):
        AdaptiveBudgeting("nonexistent.json")


def test_update_metrics(budgeting):
    """Test updating budget metrics."""
    # Update metrics for a model
    budgeting.update_metrics("gpt-4", 1000, 0.1)
    metrics = budgeting.get_metrics("gpt-4")

    assert metrics.total_tokens == 1000
    assert metrics.total_cost == 0.1
    assert metrics.request_count == 1
    assert metrics.average_tokens_per_request == 1000.0
    assert metrics.average_cost_per_request == 0.1
    assert metrics.peak_tokens == 1000
    assert metrics.peak_cost == 0.1

    # Update metrics again
    budgeting.update_metrics("gpt-4", 2000, 0.2)
    metrics = budgeting.get_metrics("gpt-4")

    assert metrics.total_tokens == 3000
    assert metrics.total_cost == 0.3
    assert metrics.request_count == 2
    assert metrics.average_tokens_per_request == 1500.0
    assert metrics.average_cost_per_request == 0.15
    assert metrics.peak_tokens == 2000
    assert metrics.peak_cost == 0.2


def test_get_metrics(budgeting):
    """Test getting budget metrics."""
    # Update metrics for multiple models
    budgeting.update_metrics("gpt-4", 1000, 0.1)
    budgeting.update_metrics("gpt-3.5-turbo", 2000, 0.05)

    # Get metrics for each model
    gpt4_metrics = budgeting.get_metrics("gpt-4")
    gpt35_metrics = budgeting.get_metrics("gpt-3.5-turbo")

    assert gpt4_metrics.total_tokens == 1000
    assert gpt4_metrics.total_cost == 0.1
    assert gpt35_metrics.total_tokens == 2000
    assert gpt35_metrics.total_cost == 0.05


def test_get_alerts(budgeting, temp_config_file):
    """Test getting budget alerts."""
    budgeting = AdaptiveBudgeting(temp_config_file)

    # Update metrics to trigger alerts
    budgeting.update_metrics("gpt-4", 2000000, 200.0)  # Exceeds both thresholds

    # Get all alerts
    alerts = budgeting.get_alerts()
    assert len(alerts) > 0

    # Get alerts for specific model
    gpt4_alerts = budgeting.get_alerts(model="gpt-4")
    assert all(a.metrics.model == "gpt-4" for a in gpt4_alerts)

    # Get alerts by type
    token_alerts = budgeting.get_alerts(alert_type="token_threshold")
    assert all(a.alert_type == "token_threshold" for a in token_alerts)

    # Get alerts by time range
    start_time = datetime.now() - timedelta(minutes=5)
    end_time = datetime.now() + timedelta(minutes=5)
    time_alerts = budgeting.get_alerts(start_time=start_time, end_time=end_time)
    assert all(start_time <= datetime.fromisoformat(a.timestamp) <= end_time for a in time_alerts)


def test_reset_metrics(budgeting):
    """Test resetting budget metrics."""
    # Update metrics for multiple models
    budgeting.update_metrics("gpt-4", 1000, 0.1)
    budgeting.update_metrics("gpt-3.5-turbo", 2000, 0.05)

    # Reset metrics for specific model
    budgeting.reset_metrics("gpt-4")
    gpt4_metrics = budgeting.get_metrics("gpt-4")
    assert gpt4_metrics.total_tokens == 0
    assert gpt4_metrics.total_cost == 0.0
    assert gpt4_metrics.request_count == 0

    # Verify other model is unchanged
    gpt35_metrics = budgeting.get_metrics("gpt-3.5-turbo")
    assert gpt35_metrics.total_tokens == 2000
    assert gpt35_metrics.total_cost == 0.05

    # Reset all metrics
    budgeting.reset_metrics()
    assert len(budgeting.metrics) == 0


def test_export_metrics(budgeting, tempfile):
    """Test exporting budget metrics."""
    # Update metrics
    budgeting.update_metrics("gpt-4", 1000, 0.1)
    budgeting.update_metrics("gpt-3.5-turbo", 2000, 0.05)

    # Export metrics
    metrics_path = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
    budgeting.export_metrics(metrics_path)

    # Verify exported data
    with open(metrics_path, "r") as f:
        metrics_data = json.load(f)
        assert "gpt-4" in metrics_data
        assert "gpt-3.5-turbo" in metrics_data
        assert metrics_data["gpt-4"]["total_tokens"] == 1000
        assert metrics_data["gpt-3.5-turbo"]["total_tokens"] == 2000


def test_export_alerts(budgeting, temp_config_file, tempfile):
    """Test exporting budget alerts."""
    budgeting = AdaptiveBudgeting(temp_config_file)

    # Generate some alerts
    budgeting.update_metrics("gpt-4", 2000000, 200.0)

    # Export alerts
    alerts_path = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
    budgeting.export_alerts(alerts_path)

    # Verify exported data
    with open(alerts_path, "r") as f:
        alerts_data = json.load(f)
        assert len(alerts_data) > 0
        assert all(
            key in alerts_data[0]
            for key in [
                "timestamp",
                "alert_type",
                "message",
                "threshold",
                "current_value",
            ]
        )


def test_export_invalid_format(budgeting):
    """Test exporting with invalid format."""
    with pytest.raises(ValueError):
        budgeting.export_metrics("metrics.txt")
    with pytest.raises(ValueError):
        budgeting.export_alerts("alerts.txt")
