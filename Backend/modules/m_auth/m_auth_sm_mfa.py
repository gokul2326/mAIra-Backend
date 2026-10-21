from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from xsc_lib.xsc_lib_app.xsc_lib_a_config import settings
from xsc_lib.xsc_lib_app.xsc_lib_a_secrets import generate_secure_otp
from modules.m_auth.m_auth_data import save_otp, get_otp_record, delete_otp_record
from modules.m_audit.m_audit_data import record_audit_event

def initiate_login_mfa(email: str) -> str:
    otp = generate_secure_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    save_otp(email=email, otp=otp, purpose="login_mfa", expires_at=expires_at)
    record_audit_event("MFA_OTP_ISSUED", email, "SUCCESS")
    return otp

def verify_submitted_otp(email: str, input_otp: str, expected_purpose: str) -> bool:
    clean_email = email.lower().strip()
    record = get_otp_record(clean_email)

    if not record:
        record_audit_event("VERIFY_OTP", clean_email, "NOT_FOUND_OR_EXPIRED")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verification code was requested or code has expired."
        )

    if record["purpose"] != expected_purpose:
        record_audit_event("VERIFY_OTP", clean_email, "WRONG_PURPOSE")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid OTP scope for {expected_purpose}."
        )

    if datetime.now(timezone.utc) > record["expires_at"]:
        delete_otp_record(clean_email)
        record_audit_event("VERIFY_OTP", clean_email, "EXPIRED")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired. Please request a new code."
        )

    if record["otp"] != input_otp.strip():
        record_audit_event("VERIFY_OTP", clean_email, "MISMATCH")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid verification code."
        )

    delete_otp_record(clean_email)
    record_audit_event("VERIFY_OTP", clean_email, "SUCCESS", {"purpose": expected_purpose})
    return True
