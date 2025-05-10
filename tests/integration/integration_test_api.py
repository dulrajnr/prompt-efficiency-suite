"""
Integration tests for the API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from prompt_efficiency_suite.api import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_prompt():
    """Return a sample prompt for testing."""
    return "Write a function that calculates the Fibonacci sequence."


def test_analyze_endpoint(client, sample_prompt):
    """Test the analyze endpoint."""
    response = client.post("/api/v1/analyze", json={"prompt": sample_prompt})
    assert response.status_code == 200
    data = response.json()
    assert "clarity" in data
    assert "structure" in data
    assert "complexity" in data
    assert "suggestions" in data


def test_optimize_endpoint(client, sample_prompt):
    """Test the optimize endpoint."""
    response = client.post(
        "/api/v1/optimize",
        json={
            "prompt": sample_prompt,
            "method": "trim",
            "preserve_ratio": 0.8,
            "domain_terms": ["function", "Fibonacci"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "original_prompt" in data
    assert "optimized_prompt" in data
    assert "improvements" in data


def test_estimate_cost_endpoint(client, sample_prompt):
    """Test the estimate_cost endpoint."""
    response = client.post("/api/v1/estimate-cost", json={"prompt": sample_prompt, "model": "gpt-4", "currency": "USD"})
    assert response.status_code == 200
    data = response.json()
    assert "input_tokens" in data
    assert "output_tokens" in data
    assert "total_cost" in data
    assert "currency" in data


def test_scan_repository_endpoint(client, tmp_path):
    """Test the scan_repository endpoint."""
    # Create sample files
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "example1.txt").write_text("Write a function that calculates the Fibonacci sequence.")
    (tmp_path / "prompts" / "example2.txt").write_text("Create a REST API endpoint for user authentication.")

    response = client.post(
        "/api/v1/scan-repository",
        json={"directory": str(tmp_path), "include_patterns": ["*.txt"], "exclude_patterns": ["*.py"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "files_scanned" in data
    assert "prompts_found" in data
    assert "results" in data


def test_translate_endpoint(client, sample_prompt):
    """Test the translate endpoint."""
    response = client.post(
        "/api/v1/translate", json={"prompt": sample_prompt, "source_model": "gpt-4", "target_model": "gpt-3.5-turbo"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "original_prompt" in data
    assert "translated_prompt" in data
    assert "warnings" in data


def test_metrics_endpoint(client):
    """Test the metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "prompt_analysis_total" in response.text
    assert "prompt_optimization_total" in response.text
    assert "analysis_duration_seconds" in response.text


def test_websocket_endpoint(client, sample_prompt):
    """Test the WebSocket endpoint."""
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"action": "analyze", "prompt": sample_prompt})
        response = websocket.receive_json()
        assert "status" in response
        assert "data" in response
        assert "clarity" in response["data"]
        assert "structure" in response["data"]


def test_error_handling(client):
    """Test error handling."""
    # Test invalid JSON
    response = client.post("/api/v1/analyze", data="invalid json")
    assert response.status_code == 422

    # Test missing required field
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422

    # Test invalid method
    response = client.post("/api/v1/optimize", json={"prompt": "test", "method": "invalid_method"})
    assert response.status_code == 400


def test_rate_limiting(client, sample_prompt):
    """Test rate limiting."""
    # Make multiple requests in quick succession
    for _ in range(11):  # Assuming rate limit is 10 requests per minute
        response = client.post("/api/v1/analyze", json={"prompt": sample_prompt})

    # The last request should be rate limited
    assert response.status_code == 429
    assert "rate limit exceeded" in response.json()["detail"].lower()


def test_authentication(client, sample_prompt):
    """Test authentication."""
    # Test without token
    response = client.post("/api/v1/analyze", json={"prompt": sample_prompt})
    assert response.status_code == 401

    # Test with invalid token
    response = client.post(
        "/api/v1/analyze", json={"prompt": sample_prompt}, headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

    # Test with valid token
    response = client.post(
        "/api/v1/analyze", json={"prompt": sample_prompt}, headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
