from datetime import datetime

import pytest

from prompt_efficiency_suite.model_translator import ModelType
from prompt_efficiency_suite.orchestrator import (
    ModelPerformance,
    PerformanceMetrics,
    PromptOrchestrator,
)


@pytest.fixture
def orchestrator():
    return PromptOrchestrator()


def test_initialization(orchestrator):
    """Test that the orchestrator initializes correctly."""
    assert len(orchestrator.model_performance) == len(ModelType)
    for model in ModelType:
        assert model in orchestrator.model_performance
        performance = orchestrator.model_performance[model]
        assert isinstance(performance, ModelPerformance)
        assert len(performance.metrics) == 0
        assert performance.average_latency == 0.0
        assert performance.average_cost == 0.0
        assert performance.success_rate == 1.0


def test_model_selection(orchestrator):
    """Test model selection based on requirements."""
    prompt = "This is a test prompt."
    requirements = {"latency": 0.5, "cost": 0.3, "quality": 0.2}

    selected_model, confidence = orchestrator.select_model(
        prompt=prompt, requirements=requirements
    )

    assert isinstance(selected_model, ModelType)
    assert 0 <= confidence <= 1


def test_performance_update(orchestrator):
    """Test updating performance metrics."""
    model = ModelType.GPT4
    initial_performance = orchestrator.get_model_performance(model)

    # Update metrics
    orchestrator.update_performance_metrics(
        model=model, latency=100.0, tokens=50, cost=0.001, success=True
    )

    updated_performance = orchestrator.get_model_performance(model)
    assert len(updated_performance.metrics) == 1
    assert updated_performance.average_latency == 100.0
    assert updated_performance.average_cost == 0.001
    assert updated_performance.success_rate == 1.0


def test_performance_window(orchestrator):
    """Test that performance metrics are limited to the window size."""
    model = ModelType.GPT4

    # Add more metrics than the window size
    for i in range(orchestrator.performance_window + 10):
        orchestrator.update_performance_metrics(
            model=model, latency=float(i), tokens=50, cost=0.001, success=True
        )

    performance = orchestrator.get_model_performance(model)
    assert len(performance.metrics) == orchestrator.performance_window


def test_best_model_selection(orchestrator):
    """Test selecting the best model based on requirements."""
    # Update performance metrics for different models
    for model in ModelType:
        orchestrator.update_performance_metrics(
            model=model, latency=100.0, tokens=50, cost=0.001, success=True
        )

    requirements = {"latency": 0.5, "cost": 0.3, "quality": 0.2}

    best_model = orchestrator.get_best_model_for_requirements(requirements)
    assert isinstance(best_model, ModelType)


def test_performance_summary(orchestrator):
    """Test getting performance summary."""
    # Update some metrics
    for model in ModelType:
        orchestrator.update_performance_metrics(
            model=model, latency=100.0, tokens=50, cost=0.001, success=True
        )

    summary = orchestrator.get_performance_summary()
    assert len(summary) == len(ModelType)

    for model_value, metrics in summary.items():
        assert "average_latency" in metrics
        assert "average_cost" in metrics
        assert "success_rate" in metrics
        assert "last_updated" in metrics
        assert "metrics_count" in metrics


def test_model_selection_with_available_models(orchestrator):
    """Test model selection with specific available models."""
    prompt = "This is a test prompt."
    requirements = {"latency": 0.33, "cost": 0.33, "quality": 0.33}
    available_models = [ModelType.GPT4, ModelType.CLAUDE]

    selected_model, confidence = orchestrator.select_model(
        prompt=prompt, requirements=requirements, available_models=available_models
    )

    assert selected_model in available_models
    assert 0 <= confidence <= 1


def test_performance_metrics_creation():
    """Test creation of performance metrics."""
    metrics = PerformanceMetrics(
        latency=100.0,
        tokens_per_second=500.0,
        cost=0.001,
        success_rate=1.0,
        error_rate=0.0,
        timestamp=datetime.now(),
    )

    assert metrics.latency == 100.0
    assert metrics.tokens_per_second == 500.0
    assert metrics.cost == 0.001
    assert metrics.success_rate == 1.0
    assert metrics.error_rate == 0.0
    assert isinstance(metrics.timestamp, datetime)


def test_model_performance_creation():
    """Test creation of model performance object."""
    performance = ModelPerformance(
        metrics=[],
        average_latency=0.0,
        average_cost=0.0,
        success_rate=1.0,
        last_updated=datetime.now(),
    )

    assert len(performance.metrics) == 0
    assert performance.average_latency == 0.0
    assert performance.average_cost == 0.0
    assert performance.success_rate == 1.0
    assert isinstance(performance.last_updated, datetime)
