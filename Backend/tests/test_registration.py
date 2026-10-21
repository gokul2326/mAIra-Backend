import pytest
from fastapi.testclient import TestClient
from main import app
from modules.m_auth.m_auth_data import get_otp_record

client = TestClient(app)

def test_full_registration_lifecycle():
    email = "onboarding.user@company.com"

    # Step 1: Request OTP
    r1 = client.post("/api/auth/register-request", json={"email": email})
    assert r1.status_code == 200

    # Step 2: Retrieve OTP from store
    record = get_otp_record(email)
    assert record is not None
    otp = record["otp"]

    # Step 3: Verify OTP
    r2 = client.post("/api/auth/verify-registration-otp", json={"email": email, "otp": otp})
    assert r2.status_code == 200
    token = r2.json()["set_password_token"]

    # Step 4: Set Password
    r3 = client.post("/api/auth/set-password", json={
        "token": token,
        "new_password": "NewUserPassword123!",
        "confirm_password": "NewUserPassword123!"
    })
    assert r3.status_code == 200
    res = r3.json()
    assert "access_token" in res["session"]
    assert res["session"]["user"]["role"] == "Data Analyst"
