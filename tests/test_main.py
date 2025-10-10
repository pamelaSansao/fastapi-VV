from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Olá QTS"}


def test_read_user():
    user_id = 42
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "q": None}


def test_read_user_with_query_param():
    user_id = 10
    query_param = "test_query"
    response = client.get(f"/user/{user_id}?q={query_param}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "q": query_param}
