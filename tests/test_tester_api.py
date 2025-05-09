from fastapi.testclient import TestClient
from prompt_efficiency_suite.api.tester_api import router
from prompt_efficiency_suite.model_translator import ModelType

client = TestClient(router)

def test_run_test_case():
    """Test the /test-case endpoint."""
    response = client.post(
        "/test-case",
        json={
            "name": "Test Case 1",
            "prompt": "What is 2+2?",
            "expected_response": "4",
            "expected_patterns": ["number", "sum"],
            "expected_tokens": 10,
            "timeout": 5.0
        },
        params={
            "model": "gpt-4",
            "max_retries": 3,
            "timeout": 5.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "response" in data
    assert "execution_time" in data
    assert "token_usage" in data
    assert "prompt" in data["token_usage"]
    assert "completion" in data["token_usage"]

def test_run_test_case_invalid_model():
    """Test the /test-case endpoint with invalid model."""
    response = client.post(
        "/test-case",
        json={
            "name": "Test Case 1",
            "prompt": "Test prompt"
        },
        params={
            "model": "invalid-model"
        }
    )
    
    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]

def test_run_test_suite():
    """Test the /test-suite endpoint."""
    response = client.post(
        "/test-suite",
        json={
            "name": "Math Test Suite",
            "description": "Test basic math operations",
            "test_cases": [
                {
                    "name": "Test Case 1",
                    "prompt": "What is 2+2?",
                    "expected_response": "4"
                },
                {
                    "name": "Test Case 2",
                    "prompt": "What is 3+3?",
                    "expected_response": "6"
                }
            ],
            "model": "gpt-4",
            "max_retries": 3,
            "timeout": 10.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for result in data:
        assert "success" in result
        assert "response" in result
        assert "execution_time" in result
        assert "token_usage" in result

def test_run_test_suite_invalid_model():
    """Test the /test-suite endpoint with invalid model."""
    response = client.post(
        "/test-suite",
        json={
            "name": "Test Suite",
            "description": "Test suite",
            "test_cases": [
                {
                    "name": "Test Case 1",
                    "prompt": "Test prompt"
                }
            ],
            "model": "invalid-model"
        }
    )
    
    assert response.status_code == 400
    assert "Invalid model type" in response.json()["detail"]

def test_get_test_history():
    """Test the /history endpoint."""
    # First run a test to generate history
    client.post(
        "/test-case",
        json={
            "name": "Test Case 1",
            "prompt": "Test prompt"
        },
        params={
            "model": "gpt-4"
        }
    )
    
    # Then get history
    response = client.get("/history")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for entry in data:
        assert "test_case" in entry
        assert "result" in entry
        assert "name" in entry["test_case"]
        assert "prompt" in entry["test_case"]
        assert "success" in entry["result"]
        assert "response" in entry["result"]

def test_clear_test_history():
    """Test the /history endpoint DELETE method."""
    # First run a test to generate history
    client.post(
        "/test-case",
        json={
            "name": "Test Case 1",
            "prompt": "Test prompt"
        },
        params={
            "model": "gpt-4"
        }
    )
    
    # Clear history
    response = client.delete("/history")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Test history cleared successfully"
    
    # Verify history is cleared
    history_response = client.get("/history")
    assert len(history_response.json()) == 0

def test_test_case_metadata():
    """Test metadata handling in test cases."""
    response = client.post(
        "/test-case",
        json={
            "name": "Test Case 1",
            "prompt": "Test prompt",
            "metadata": {
                "key": "value",
                "number": 42
            }
        },
        params={
            "model": "gpt-4"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert data["metadata"] is not None

def test_test_suite_metadata():
    """Test metadata handling in test suites."""
    response = client.post(
        "/test-suite",
        json={
            "name": "Test Suite",
            "description": "Test suite",
            "test_cases": [
                {
                    "name": "Test Case 1",
                    "prompt": "Test prompt"
                }
            ],
            "model": "gpt-4",
            "metadata": {
                "key": "value",
                "number": 42
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for result in data:
        assert "metadata" in result
        assert result["metadata"] is not None 