from fastapi.testclient import TestClient

from prompt_efficiency_suite.api.optimizer_api import router
from prompt_efficiency_suite.model_translator import ModelType

client = TestClient(router)


def test_optimize_prompt():
    """Test the /optimize endpoint."""
    response = client.post(
        "/optimize",
        json={
            "prompt": "Please tell me what is the sum of 2 plus 2?",
            "test_cases": [
                {
                    "name": "Test Case 1",
                    "prompt": "What is 2+2?",
                    "expected_response": "4",
                    "expected_patterns": ["number", "sum"],
                    "expected_tokens": 10,
                    "timeout": 5.0,
                }
            ],
            "config": {
                "target_model": "gpt-4",
                "max_iterations": 5,
                "min_improvement": 0.1,
                "token_reduction_target": 5,
                "execution_time_target": 0.5,
                "preserve_patterns": ["number", "sum"],
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "original_prompt" in data
    assert "optimized_prompt" in data
    assert "improvement_percentage" in data
    assert "token_reduction" in data
    assert "execution_time_reduction" in data
    assert "test_results" in data
    assert isinstance(data["test_results"], list)


def test_optimize_prompt_invalid_model():
    """Test the /optimize endpoint with invalid model."""
    response = client.post(
        "/optimize",
        json={
            "prompt": "Test prompt",
            "test_cases": [{"name": "Test Case 1", "prompt": "Test prompt"}],
            "config": {"target_model": "invalid-model"},
        },
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_get_optimization_history():
    """Test the /history endpoint."""
    # First run an optimization to generate history
    client.post(
        "/optimize",
        json={
            "prompt": "Test prompt",
            "test_cases": [{"name": "Test Case 1", "prompt": "Test prompt"}],
            "config": {"target_model": "gpt-4"},
        },
    )

    # Then get history
    response = client.get("/history")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for entry in data:
        assert "original_prompt" in entry
        assert "result" in entry
        assert "optimized_prompt" in entry["result"]
        assert "improvement_percentage" in entry["result"]
        assert "token_reduction" in entry["result"]
        assert "execution_time_reduction" in entry["result"]
        assert "test_results" in entry["result"]


def test_clear_optimization_history():
    """Test the /history endpoint DELETE method."""
    # First run an optimization to generate history
    client.post(
        "/optimize",
        json={
            "prompt": "Test prompt",
            "test_cases": [{"name": "Test Case 1", "prompt": "Test prompt"}],
            "config": {"target_model": "gpt-4"},
        },
    )

    # Clear history
    response = client.delete("/history")

    assert response.status_code == 200
    assert response.json()["message"] == "Optimization history cleared successfully"

    # Verify history is cleared
    history_response = client.get("/history")
    assert len(history_response.json()) == 0


def test_optimization_metadata():
    """Test metadata handling in optimization."""
    response = client.post(
        "/optimize",
        json={
            "prompt": "Test prompt",
            "test_cases": [
                {"name": "Test Case 1", "prompt": "Test prompt", "metadata": {"key": "value", "number": 42}}
            ],
            "config": {"target_model": "gpt-4", "metadata": {"key": "value", "number": 42}},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert data["metadata"] is not None
    assert data["metadata"]["key"] == "value"
    assert data["metadata"]["number"] == 42


def test_optimization_config_validation():
    """Test optimization config validation."""
    response = client.post(
        "/optimize",
        json={
            "prompt": "Test prompt",
            "test_cases": [{"name": "Test Case 1", "prompt": "Test prompt"}],
            "config": {
                "target_model": "gpt-4",
                "max_iterations": 0,  # Invalid value
                "min_improvement": 2.0,  # Invalid value
            },
        },
    )

    assert response.status_code == 422  # Validation error


def test_optimization_with_multiple_test_cases():
    """Test optimization with multiple test cases."""
    response = client.post(
        "/optimize",
        json={
            "prompt": "Test prompt",
            "test_cases": [
                {"name": "Test Case 1", "prompt": "Test prompt 1", "expected_response": "Response 1"},
                {"name": "Test Case 2", "prompt": "Test prompt 2", "expected_response": "Response 2"},
            ],
            "config": {"target_model": "gpt-4"},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "test_results" in data
    assert len(data["test_results"]) == 2
    for result in data["test_results"]:
        assert "success" in result
        assert "response" in result
        assert "execution_time" in result
        assert "token_usage" in result


def test_optimize_endpoint():
    """Test the /optimize endpoint."""
    response = client.post(
        "/optimize",
        json={
            "prompt": """
            System: You are a helpful assistant.
            Context: This is some background information that is really very important.
            Instruction: Please kindly help me with this task in order to achieve the goal.
            """,
            "model": "gpt-4",
            "config": {
                "max_tokens": 1000,
                "min_quality_score": 0.8,
                "preserve_structure": True,
                "aggressive_optimization": True,
                "target_cost_reduction": 0.2,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "optimized_prompt" in data
    assert "metrics" in data
    assert "suggestions" in data

    metrics = data["metrics"]
    assert "original_tokens" in metrics
    assert "optimized_tokens" in metrics
    assert "token_reduction" in metrics
    assert "estimated_cost_reduction" in metrics
    assert "quality_score" in metrics
    assert "structure_score" in metrics


def test_optimize_endpoint_invalid_model():
    """Test the /optimize endpoint with invalid model."""
    response = client.post("/optimize", json={"prompt": "Test prompt", "model": "invalid-model"})

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_optimize_endpoint_default_config():
    """Test the /optimize endpoint with default config."""
    response = client.post("/optimize", json={"prompt": "Test prompt", "model": "gpt-4"})

    assert response.status_code == 200
    data = response.json()
    assert "optimized_prompt" in data
    assert "metrics" in data
    assert "suggestions" in data


def test_suggestions_endpoint():
    """Test the /suggestions endpoint."""
    response = client.get(
        "/suggestions",
        params={
            "prompt": """
            This is really very important and in order to achieve the goal,
            we need to do something that is in need of attention.
            """
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    assert len(data["suggestions"]) > 0


def test_suggestions_endpoint_empty_prompt():
    """Test the /suggestions endpoint with empty prompt."""
    response = client.get("/suggestions", params={"prompt": ""})

    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)


def test_optimize_endpoint_quality_preservation():
    """Test that optimization preserves quality."""
    prompt = """
    System: You are a helpful assistant.
    Instruction: Please help me with this task.
    """

    response = client.post("/optimize", json={"prompt": prompt, "model": "gpt-4", "config": {"min_quality_score": 0.9}})

    assert response.status_code == 200
    data = response.json()
    assert data["metrics"]["quality_score"] >= 0.9


def test_optimize_endpoint_structure_preservation():
    """Test that optimization preserves structure when configured."""
    prompt = """
    System: You are a helpful assistant.
    Context: Some background.
    Instruction: Do something.
    """

    response = client.post(
        "/optimize", json={"prompt": prompt, "model": "gpt-4", "config": {"preserve_structure": True}}
    )

    assert response.status_code == 200
    data = response.json()
    optimized = data["optimized_prompt"].lower()
    assert "system:" in optimized
    assert "context:" in optimized
    assert "instruction:" in optimized
