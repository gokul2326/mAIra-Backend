import pytest
from fastapi.testclient import TestClient
from main import app
from modules.m_auth.m_auth_data import get_otp_record

client = TestClient(app)

def test_rbac_admin_vs_analyst():
    # Login as Senior Engineer
    client.post("/api/auth/login", json={"email": "existing.user@company.com", "password": "Password123!"})
    otp = get_otp_record("existing.user@company.com")["otp"]
    res = client.post("/api/auth/verify-login-mfa", json={"email": "existing.user@company.com", "otp": otp})
    token = res.json()["session"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Senior Engineer chat query -> Allowed
    chat_res = client.post("/api/chat/query", json={"prompt": "Review code"}, headers=headers)
    assert chat_res.status_code == 200

    # Senior Engineer accessing Admin user table -> Forbidden (403)
    admin_res = client.get("/api/admin/users", headers=headers)
    assert admin_res.status_code == 403
