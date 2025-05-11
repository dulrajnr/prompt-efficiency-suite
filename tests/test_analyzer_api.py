from fastapi import FastAPI
from fastapi.testclient import TestClient

from prompt_efficiency_suite.api.analyzer_api import router
from prompt_efficiency_suite.model_translator import ModelType

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_analyze_prompt():
    """Test the /analyze endpoint."""
    response = client.post(
        "/analyze",
        json={
            "prompt": """
            System: You are a helpful assistant.
            Context: This is some background information.
            Instruction: Please help me with this task step by step.
            """,
            "model": "gpt-4",
            "metadata": {"key": "value", "number": 42},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "prompt" in data
    assert "metrics" in data
    assert "structure_analysis" in data
    assert "pattern_analysis" in data
    assert "quality_analysis" in data
    assert "metadata" in data

    metrics = data["metrics"]
    assert "clarity_score" in metrics
    assert "structure_score" in metrics
    assert "complexity_score" in metrics
    assert "token_estimate" in metrics
    assert "quality_score" in metrics
    assert "improvement_suggestions" in metrics


def test_analyze_prompt_invalid_model():
    """Test the /analyze endpoint with invalid model."""
    response = client.post(
        "/analyze", json={"prompt": "Test prompt", "model": "invalid-model"}
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_quick_analyze():
    """Test the /analyze/quick endpoint."""
    response = client.get(
        "/analyze/quick",
        params={
            "prompt": """
            System: You are a helpful assistant.
            Context: This is some background information.
            Instruction: Please help me with this task step by step.
            """
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "quality_score" in data
    assert "clarity_score" in data
    assert "structure_score" in data
    assert "complexity_score" in data
    assert "token_estimate" in data
    assert "top_suggestions" in data
    assert len(data["top_suggestions"]) <= 3


def test_analyze_patterns():
    """Test the /analyze/patterns endpoint."""
    response = client.get(
        "/analyze/patterns",
        params={
            "prompt": """
            This is really very important.
            Please clearly explain this complex task.
            """
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "clarity_patterns" in data
    assert "complexity_patterns" in data
    assert "redundant_patterns" in data
    assert isinstance(data["clarity_patterns"], list)
    assert isinstance(data["complexity_patterns"], list)
    assert isinstance(data["redundant_patterns"], list)


def test_analyze_structure():
    """Test the /analyze/structure endpoint."""
    response = client.get(
        "/analyze/structure",
        params={
            "prompt": """
            System: You are a helpful assistant.
            Context: Some background.
            Instruction: Do something.
            Example: Here's how.
            """
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "system_prompt" in data
    assert "context_block" in data
    assert "instruction_block" in data
    assert "example_block" in data
    assert isinstance(data["system_prompt"], list)
    assert isinstance(data["context_block"], list)
    assert isinstance(data["instruction_block"], list)
    assert isinstance(data["example_block"], list)


def test_analyze_empty_prompt():
    """Test analysis with empty prompt."""
    response = client.post("/analyze", json={"prompt": "", "model": "gpt-4"})

    assert response.status_code == 200
    data = response.json()
    assert data["metrics"]["quality_score"] < 0.5
    assert len(data["metrics"]["improvement_suggestions"]) > 0


def test_analyze_long_prompt():
    """Test analysis with long prompt."""
    long_prompt = "This is a test prompt. " * 100

    response = client.post("/analyze", json={"prompt": long_prompt, "model": "gpt-4"})

    assert response.status_code == 200
    data = response.json()
    assert data["metrics"]["token_estimate"] > 100
    assert any(
        "length" in s.lower() for s in data["metrics"]["improvement_suggestions"]
    )


def test_analyze_complex_prompt():
    """Test analysis with complex prompt."""
    complex_prompt = """
    This is a complex and sophisticated task that requires advanced expertise.
    Please provide a detailed analysis of the following complex concepts:
    1. Quantum mechanics
    2. String theory
    3. General relativity
    """

    response = client.post(
        "/analyze", json={"prompt": complex_prompt, "model": "gpt-4"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["metrics"]["complexity_score"] > 0.7
    assert any(
        "simplify" in s.lower() for s in data["metrics"]["improvement_suggestions"]
    )


def test_analyze_well_structured_prompt():
    """Test analysis with well-structured prompt."""
    well_structured_prompt = """
    System: You are a helpful assistant.
    Context: This is some background information.
    Instruction: Please help me with this task step by step.
    Example: Here's how to do it.
    """

    response = client.post(
        "/analyze", json={"prompt": well_structured_prompt, "model": "gpt-4"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["metrics"]["structure_score"] > 0.7
    assert len(data["structure_analysis"]) > 0


def test_analyze_with_metadata():
    """Test analysis with metadata."""
    metadata = {"key": "value", "number": 42, "tags": ["test", "analysis"]}

    response = client.post(
        "/analyze",
        json={"prompt": "Test prompt", "model": "gpt-4", "metadata": metadata},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["metadata"] == metadata


def test_analyze_with_special_characters():
    """Test analysis with special characters."""
    special_prompt = """
    System: You are a helpful assistant!@#$%^&*()
    Context: This is some background information...?!?
    Instruction: Please help me with this task!!!
    """

    response = client.post(
        "/analyze", json={"prompt": special_prompt, "model": "gpt-4"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["metrics"]["quality_score"] >= 0
    assert data["metrics"]["quality_score"] <= 1


def test_analyze_endpoint():
    """Test the /analyze endpoint."""
    response = client.post(
        "/analyze",
        json={
            "prompt": """
            System: You are a helpful assistant.
            Context: This is some background information.
            Instruction: Please help me with this task.
            """,
            "model": "gpt-4",
            "target_complexity": "medium",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "suggestions" in data
    assert "strengths" in data
    assert "weaknesses" in data
    assert "timestamp" in data

    metrics = data["metrics"]
    assert "clarity_score" in metrics
    assert "specificity_score" in metrics
    assert "structure_score" in metrics
    assert "context_score" in metrics
    assert "instruction_score" in metrics
    assert "overall_score" in metrics
    assert "token_count" in metrics
    assert "estimated_cost" in metrics


def test_analyze_endpoint_invalid_model():
    """Test the /analyze endpoint with invalid model."""
    response = client.post(
        "/analyze", json={"prompt": "Test prompt", "model": "invalid-model"}
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_analyze_endpoint_default_complexity():
    """Test the /analyze endpoint with default complexity."""
    response = client.post("/analyze", json={"prompt": "Test prompt", "model": "gpt-4"})

    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "suggestions" in data
    assert "strengths" in data
    assert "weaknesses" in data


def test_metrics_endpoint():
    """Test the /metrics endpoint."""
    response = client.get(
        "/metrics",
        params={
            "prompt": """
            System: You are a helpful assistant.
            Context: This is some background information.
            Instruction: Please help me with this task.
            """,
            "model": "gpt-4",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data

    metrics = data["metrics"]
    assert "clarity_score" in metrics
    assert "specificity_score" in metrics
    assert "structure_score" in metrics
    assert "context_score" in metrics
    assert "instruction_score" in metrics
    assert "overall_score" in metrics
    assert "token_count" in metrics
    assert "estimated_cost" in metrics
    assert "complexity_level" in metrics


def test_metrics_endpoint_invalid_model():
    """Test the /metrics endpoint with invalid model."""
    response = client.get(
        "/metrics", params={"prompt": "Test prompt", "model": "invalid-model"}
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_suggestions_endpoint():
    """Test the /suggestions endpoint."""
    response = client.get(
        "/suggestions",
        params={
            "prompt": "Do something about this.",
            "model": "gpt-4",
            "target_complexity": "medium",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert "strengths" in data
    assert "weaknesses" in data
    assert isinstance(data["suggestions"], list)
    assert isinstance(data["strengths"], list)
    assert isinstance(data["weaknesses"], list)


def test_suggestions_endpoint_invalid_model():
    """Test the /suggestions endpoint with invalid model."""
    response = client.get(
        "/suggestions", params={"prompt": "Test prompt", "model": "invalid-model"}
    )

    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]


def test_suggestions_endpoint_default_complexity():
    """Test the /suggestions endpoint with default complexity."""
    response = client.get(
        "/suggestions", params={"prompt": "Test prompt", "model": "gpt-4"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert "strengths" in data
    assert "weaknesses" in data
