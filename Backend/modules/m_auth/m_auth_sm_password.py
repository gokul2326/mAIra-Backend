from fastapi import HTTPException, status
from xsc_lib.xsc_lib_app.xsc_lib_a_security import hash_password, verify_password, decode_jwt_token
from modules.m_user.m_user_data import update_user_password, get_user_by_email
from modules.m_audit.m_audit_data import record_audit_event

def set_initial_password(token: str, new_password: str, confirm_password: str) -> str:
    if new_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match."
        )

    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )

    claims = decode_jwt_token(token)
    if not claims or claims.get("purpose") != "set_password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired set-password token."
        )

    email = claims.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token identity.")

    hashed = hash_password(new_password)
    success = update_user_password(email, hashed)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")

    record_audit_event("SET_PASSWORD", email, "SUCCESS")
    return email

def validate_user_credentials(email: str, plain_password: str) -> dict:
    clean_email = email.lower().strip()
    user = get_user_by_email(clean_email)

    if not user or not user.get("is_active"):
        record_audit_event("LOGIN_CREDENTIALS", clean_email, "FAILED_INVALID_OR_INACTIVE")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not user.get("is_registered") or not user.get("password_hash"):
        record_audit_event("LOGIN_CREDENTIALS", clean_email, "FAILED_NOT_REGISTERED")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account onboarding incomplete. Please register first."
        )

    if not verify_password(plain_password, user["password_hash"]):
        record_audit_event("LOGIN_CREDENTIALS", clean_email, "FAILED_BAD_PASSWORD")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    record_audit_event("LOGIN_CREDENTIALS", clean_email, "SUCCESS")
    return user
