
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.main import app, posting_service


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200


def test_invalid_message_without_url():

    response = client.post(
        "/posting",
        json={
            "message": "Hello world"
        }
    )

    assert response.status_code == 422


def test_invalid_message_with_two_urls():

    response = client.post(
        "/posting",
        json={
            "message": "Visit https://google.com and https://github.com"
        }
    )

    assert response.status_code == 422


def test_message_over_200_characters():

    response = client.post(
        "/posting",
        json={
            "message": "A" * 201 + " https://example.com"
        }
    )

    assert response.status_code == 422


def test_valid_posting(monkeypatch):

    mock_result = {
        "success": True,
        "results": [
            {
                "platform": "Bluesky",
                "status": "success",
                "posted_url": "https://example.com/post/123",
                "public_access": True,
                "date": "2026-11-15",
                "time": "10:30:00",
                "error": None
            }
        ]
    }

    monkeypatch.setattr(
        posting_service,
        "publish",
        AsyncMock(return_value=mock_result)
    )

    response = client.post(
        "/posting",
        json={
            "message": "Check out our platform https://example.com"
        }
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
