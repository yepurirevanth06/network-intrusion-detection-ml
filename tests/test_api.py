"""Tests for the NIDS Flask REST API."""

import io
import pytest

from app.app import app


@pytest.fixture
def client():
    """Flask test client — hits endpoints without running a server."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """GET /health responds with 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_home_page_loads(client):
    """GET / serves the dashboard."""
    response = client.get("/")
    assert response.status_code == 200


def test_predict_rejects_missing_file(client):
    """POST /predict with no file returns an error, not a crash."""
    response = client.post("/predict", data={})
    assert response.status_code in (400, 422)


def test_predict_returns_results_for_valid_csv(client):
    """POST /predict with a real CSV returns summary and results."""
    with open("sample_test.csv", "rb") as f:
        data = {"file": (io.BytesIO(f.read()), "sample_test.csv")}
    response = client.post(
        "/predict", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    body = response.get_json()
    assert "summary" in body
    assert "results" in body
