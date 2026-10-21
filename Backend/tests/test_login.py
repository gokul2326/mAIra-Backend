import pytest
from fastapi.testclient import TestClient
from main import app
from modules.m_auth.m_auth_data import get_otp_record

client = TestClient(app)

def test_full_login_mfa_lifecycle():
    email = "existing.user@company.com"

    # Step 1: Submit Credentials
    r1 = client.post("/api/auth/login", json={"email": email, "password": "Password123!"})
    assert r1.status_code == 200

    # Step 2: Retrieve OTP
    record = get_otp_record(email)
    assert record is not None
    otp = record["otp"]

    # Step 3: Verify MFA OTP
    r2 = client.post("/api/auth/verify-login-mfa", json={"email": email, "otp": otp})
    assert r2.status_code == 200
    res = r2.json()
    assert "access_token" in res["session"]
    assert res["session"]["user"]["role"] == "Senior Engineer"
