from typing import Dict, Any, Optional
from datetime import datetime

OTP_STORE: Dict[str, Dict[str, Any]] = {}

def save_otp(email: str, otp: str, purpose: str, expires_at: datetime):
    OTP_STORE[email.lower().strip()] = {
        "otp": otp,
        "purpose": purpose,
        "expires_at": expires_at
    }

def get_otp_record(email: str) -> Optional[Dict[str, Any]]:
    return OTP_STORE.get(email.lower().strip())

def delete_otp_record(email: str):
    OTP_STORE.pop(email.lower().strip(), None)
