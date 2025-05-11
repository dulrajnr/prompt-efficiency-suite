from fastapi import FastAPI
from fastapi.testclient import TestClient

from prompt_efficiency_suite.api.orchestrator_api import router
from prompt_efficiency_suite.model_translator import ModelType

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_select_model_endpoint():
    """Test the /select-model endpoint."""
    response = client.post(
        "/select-model",
        json={
            "prompt": "This is a test prompt.",
            "requirements": {"latency": 0.5, "cost": 0.3, "quality": 0.2},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "selected_model" in data
    assert "confidence_score" in data
    assert "performance_metrics" in data

    metrics = data["performance_metrics"]
    assert "average_latency" in metrics
    assert "average_cost" in metrics
    assert "success_rate" in metrics


def test_select_model_with_available_models():
    """Test the /select-model endpoint with specific available models."""
    response = client.post(
        "/select-model",
        json={
            "prompt": "This is a test prompt.",
            "requirements": {"latency": 0.33, "cost": 0.33, "quality": 0.33},
            "available_models": ["gpt-4", "claude-3"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["selected_model"] in ["gpt-4", "claude-3"]


def test_select_model_invalid_model():
    """Test the /select-model endpoint with invalid model."""
    response = client.post(
        "/select-model",
        json={
            "prompt": "This is a test prompt.",
            "requirements": {"latency": 0.33, "cost": 0.33, "quality": 0.33},
            "available_models": ["invalid-model"],
        },
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_update_performance_endpoint():
    """Test the /update-performance endpoint."""
    response = client.post(
        "/update-performance",
        json={
            "model": "gpt-4",
            "latency": 100.0,
            "tokens": 50,
            "cost": 0.001,
            "success": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_update_performance_invalid_model():
    """Test the /update-performance endpoint with invalid model."""
    response = client.post(
        "/update-performance",
        json={
            "model": "invalid-model",
            "latency": 100.0,
            "tokens": 50,
            "cost": 0.001,
            "success": True,
        },
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_performance_summary_endpoint():
    """Test the /performance-summary endpoint."""
    # First update some metrics
    for model in ModelType:
        client.post(
            "/update-performance",
            json={
                "model": model.value,
                "latency": 100.0,
                "tokens": 50,
                "cost": 0.001,
                "success": True,
            },
        )

    response = client.get("/performance-summary")

    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "timestamp" in data

    models = data["models"]
    assert len(models) == len(ModelType)

    for model_value, metrics in models.items():
        assert "average_latency" in metrics
        assert "average_cost" in metrics
        assert "success_rate" in metrics
        assert "last_updated" in metrics
        assert "metrics_count" in metrics


def test_best_model_endpoint():
    """Test the /best-model endpoint."""
    # First update some metrics
    for model in ModelType:
        client.post(
            "/update-performance",
            json={
                "model": model.value,
                "latency": 100.0,
                "tokens": 50,
                "cost": 0.001,
                "success": True,
            },
        )

    response = client.get(
        "/best-model",
        params={"latency_weight": 0.5, "cost_weight": 0.3, "quality_weight": 0.2},
    )

    assert response.status_code == 200
    data = response.json()
    assert "model" in data
    assert "performance" in data

    performance = data["performance"]
    assert "average_latency" in performance
    assert "average_cost" in performance
    assert "success_rate" in performance
