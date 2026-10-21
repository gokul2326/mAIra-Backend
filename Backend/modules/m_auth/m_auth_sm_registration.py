from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from xsc_lib.xsc_lib_app.xsc_lib_a_config import settings
from xsc_lib.xsc_lib_app.xsc_lib_a_secrets import generate_secure_otp
from modules.m_user.m_user_data import get_user_by_email
from modules.m_auth.m_auth_data import save_otp
from modules.m_audit.m_audit_data import record_audit_event

def process_registration_initiation(email: str) -> str:
    clean_email = email.lower().strip()

    if not clean_email.endswith(f"@{settings.ALLOWED_EMAIL_DOMAIN}"):
        record_audit_event("REGISTER_ATTEMPT", clean_email, "FAILED_DOMAIN")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only company email addresses (@{settings.ALLOWED_EMAIL_DOMAIN}) are permitted."
        )

    user = get_user_by_email(clean_email)
    if not user:
        record_audit_event("REGISTER_ATTEMPT", clean_email, "NOT_IN_DB")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email address not found in organization records. Contact admin."
        )

    if user.get("is_registered"):
        record_audit_event("REGISTER_ATTEMPT", clean_email, "ALREADY_REGISTERED")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is already registered. Please proceed to Login."
        )

    otp = generate_secure_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    save_otp(email=clean_email, otp=otp, purpose="registration", expires_at=expires_at)
    record_audit_event("REGISTER_OTP_ISSUED", clean_email, "SUCCESS")
    return otp
