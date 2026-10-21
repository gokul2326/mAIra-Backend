import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_invalid_otp_fails():
    res = client.post("/api/auth/verify-login-mfa", json={"email": "existing.user@company.com", "otp": "000000"})
    assert res.status_code in [400, 401]
