from typing import Optional, Dict, Any
from modules.m_user.m_user_data import get_user_by_email

def get_profile_details(email: str) -> Optional[Dict[str, Any]]:
    user = get_user_by_email(email)
    if not user:
        return None
    return {
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
        "is_registered": user["is_registered"],
        "is_active": user["is_active"]
    }
