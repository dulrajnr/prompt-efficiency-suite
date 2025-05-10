"""
Test suite for the REST API module.
"""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import jwt
import pytest
from fastapi.testclient import TestClient

from prompt_efficiency_suite.api import ALGORITHM, SECRET_KEY, app, create_access_token


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def token():
    """Create a test token."""
    access_token_expires = timedelta(minutes=30)
    return create_access_token(data={"sub": "test"}, expires_delta=access_token_expires)


@pytest.fixture
def auth_headers(token):
    """Create authorization headers."""
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_domain_dict():
    """Create a sample domain dictionary."""
    return {"terms": ["test", "domain"], "compound_terms": [], "preserve_patterns": [], "remove_patterns": []}


def test_login(client):
    """Test login endpoint."""
    response = client.post("/token", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post("/token", data={"username": "test", "password": "wrong"})
    assert response.status_code == 401


def test_trim_text(client, auth_headers, sample_domain_dict):
    """Test text trimming endpoint."""
    # Create temporary domain dictionary
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample_domain_dict, f)
        domain_path = f.name

    response = client.post(
        "/trim",
        headers=auth_headers,
        json={"text": "This is a test text with some domain terms.", "domain": domain_path, "preserve_ratio": 0.8},
    )
    assert response.status_code == 200
    data = response.json()
    assert "trimmed_text" in data
    assert "original_tokens" in data
    assert "trimmed_tokens" in data
    assert "compression_ratio" in data
    assert "preserved_terms" in data
    assert "removed_terms" in data


def test_get_budget_metrics(client, auth_headers):
    """Test getting budget metrics."""
    response = client.get("/budget/metrics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for metrics in data:
        assert "model" in metrics
        assert "total_tokens" in metrics
        assert "total_cost" in metrics
        assert "request_count" in metrics


def test_reset_budget_metrics(client, auth_headers):
    """Test resetting budget metrics."""
    response = client.post("/budget/metrics/reset", headers=auth_headers, params={"model": "gpt-4"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Reset metrics for model: gpt-4" in data["message"]


def test_get_budget_alerts(client, auth_headers):
    """Test getting budget alerts."""
    response = client.get("/budget/alerts", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for alert in data:
        assert "timestamp" in alert
        assert "alert_type" in alert
        assert "message" in alert
        assert "threshold" in alert
        assert "current_value" in alert


def test_run_tests(client, auth_headers):
    """Test running test suite."""
    response = client.post("/cicd/tests", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "passed_tests" in data
    assert "failed_tests" in data
    assert "coverage" in data
    assert "duration" in data
    assert "output" in data


def test_deploy_package(client, auth_headers):
    """Test deploying package."""
    response = client.post("/cicd/deploy", headers=auth_headers, params={"target": "pypi"})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "duration" in data
    assert "artifacts" in data
    assert "logs" in data


def test_unauthorized_access(client):
    """Test unauthorized access to protected endpoints."""
    endpoints = [
        ("/trim", "post"),
        ("/budget/metrics", "get"),
        ("/budget/metrics/reset", "post"),
        ("/budget/alerts", "get"),
        ("/cicd/tests", "post"),
        ("/cicd/deploy", "post"),
    ]

    for endpoint, method in endpoints:
        if method == "get":
            response = client.get(endpoint)
        else:
            response = client.post(endpoint)
        assert response.status_code == 401


def test_invalid_token(client):
    """Test access with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/budget/metrics", headers=headers)
    assert response.status_code == 401


def test_docs_endpoint(client):
    """Test API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text


def test_openapi_schema(client):
    """Test OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
