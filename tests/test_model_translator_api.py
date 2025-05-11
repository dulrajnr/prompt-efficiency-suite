from fastapi.testclient import TestClient

from prompt_efficiency_suite.api.model_translator_api import router
from prompt_efficiency_suite.model_translator import ModelType

client = TestClient(router)


def test_translate_endpoint():
    """Test the /translate endpoint."""
    response = client.post(
        "/translate",
        json={
            "prompt": "This is a test prompt.",
            "source_model": "gpt-4",
            "target_model": "claude-3",
            "preserve_style": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "translated_prompt" in data
    assert "original_tokens" in data
    assert "translated_tokens" in data
    assert "estimated_cost" in data
    assert "style_compatibility" in data
    assert "format_compatibility" in data


def test_translate_endpoint_invalid_model():
    """Test the /translate endpoint with invalid model."""
    response = client.post(
        "/translate",
        json={
            "prompt": "This is a test prompt.",
            "source_model": "invalid-model",
            "target_model": "gpt-4",
            "preserve_style": True,
        },
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_compare_endpoint():
    """Test the /compare endpoint."""
    response = client.post(
        "/compare",
        json={"prompt": "This is a test prompt.", "models": ["gpt-4", "claude-3"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "gpt-4" in data["results"]
    assert "claude-3" in data["results"]

    for model in ["gpt-4", "claude-3"]:
        model_results = data["results"][model]
        assert "estimated_tokens" in model_results
        assert "estimated_cost" in model_results
        assert "style_compatibility" in model_results
        assert "format_compatibility" in model_results


def test_compare_endpoint_invalid_model():
    """Test the /compare endpoint with invalid model."""
    response = client.post(
        "/compare",
        json={"prompt": "This is a test prompt.", "models": ["invalid-model"]},
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_list_models_endpoint():
    """Test the /models endpoint."""
    response = client.get("/models")

    assert response.status_code == 200
    data = response.json()
    assert "models" in data

    for model in ModelType:
        assert model.value in data["models"]
        model_config = data["models"][model.value]
        assert "max_tokens" in model_config
        assert "cost_per_1k_tokens" in model_config
        assert "preferred_style" in model_config
        assert "temperature_range" in model_config
        assert "stop_sequences" in model_config
        assert "special_tokens" in model_config
