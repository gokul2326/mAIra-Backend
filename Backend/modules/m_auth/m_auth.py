from fastapi import APIRouter, BackgroundTasks, status
from pydantic import BaseModel, EmailStr
from modules.m_auth.m_auth_sm_registration import process_registration_initiation
from modules.m_auth.m_auth_sm_mfa import initiate_login_mfa, verify_submitted_otp
from modules.m_auth.m_auth_sm_password import set_initial_password, validate_user_credentials
from modules.m_auth.m_auth_sm_session import issue_set_password_token, issue_authenticated_session
from modules.m_user.m_user_data import get_user_by_email
from xsc_lib.xsc_lib_app.xsc_lib_a_email import dispatch_otp_email

router = APIRouter()

class RegisterInitRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class SetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginMFARequest(BaseModel):
    email: EmailStr
    otp: str

# 1. New User Registration Request
@router.post("/register-request", status_code=status.HTTP_200_OK)
def register_request(payload: RegisterInitRequest, background_tasks: BackgroundTasks):
    otp = process_registration_initiation(payload.email)
    background_tasks.add_task(dispatch_otp_email, payload.email, otp, "Registration")
    return {"message": "Verification code sent to your email.", "email": payload.email}

# 2. Verify Registration OTP
@router.post("/verify-registration-otp", status_code=status.HTTP_200_OK)
def verify_registration_otp(payload: VerifyOTPRequest):
    verify_submitted_otp(payload.email, payload.otp, expected_purpose="registration")
    set_password_token = issue_set_password_token(payload.email)
    return {
        "message": "OTP verified successfully. You can now set your password.",
        "set_password_token": set_password_token
    }

# 3. Set Password & Auto-login
@router.post("/set-password", status_code=status.HTTP_200_OK)
def set_password(payload: SetPasswordRequest):
    email = set_initial_password(payload.token, payload.new_password, payload.confirm_password)
    user = get_user_by_email(email)
    session_data = issue_authenticated_session(user)
    return {
        "message": "Password successfully created.",
        "session": session_data
    }

# 4. Existing User Login & Trigger 2FA
@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, background_tasks: BackgroundTasks):
    user = validate_user_credentials(payload.email, payload.password)
    otp = initiate_login_mfa(user["email"])
    background_tasks.add_task(dispatch_otp_email, user["email"], otp, "Login MFA")
    return {
        "message": "Credentials verified. An MFA code has been dispatched to your email.",
        "email": user["email"]
    }

# 5. Verify Login MFA & Issue Session
@router.post("/verify-login-mfa", status_code=status.HTTP_200_OK)
def verify_login_mfa(payload: LoginMFARequest):
    verify_submitted_otp(payload.email, payload.otp, expected_purpose="login_mfa")
    user = get_user_by_email(payload.email)
    session_data = issue_authenticated_session(user)
    return {
        "message": "Authentication successful.",
        "session": session_data
    }
