import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_list_conversations_empty(client):
    response = client.get("/api/conversations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.django_db
def test_create_conversation(client):
    response = client.post(
        "/api/conversations/",
        data={"model": "meta-llama/llama-3.3-70b-instruct:free"},
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["model"] == "meta-llama/llama-3.3-70b-instruct:free"