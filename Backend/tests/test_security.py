import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_unauthorized_endpoints():
    res = client.get("/api/user/me")
    assert res.status_code == 401
