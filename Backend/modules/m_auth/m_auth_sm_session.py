from datetime import timedelta
from typing import Dict, Any
from xsc_lib.xsc_lib_app.xsc_lib_a_config import settings
from xsc_lib.xsc_lib_app.xsc_lib_a_security import create_jwt_token
from modules.m_user.m_user_sm_roles import get_permissions_for_role

def issue_set_password_token(email: str) -> str:
    payload = {"sub": email, "purpose": "set_password"}
    return create_jwt_token(
        payload=payload,
        expires_delta=timedelta(minutes=settings.SET_PASSWORD_TOKEN_EXPIRE_MINUTES)
    )

def issue_authenticated_session(user: Dict[str, Any]) -> Dict[str, Any]:
    permissions = get_permissions_for_role(user["role"])
    payload = {
        "sub": user["email"],
        "name": user["name"],
        "role": user["role"],
        "permissions": permissions,
        "purpose": "access_token"
    }
    token = create_jwt_token(
        payload=payload,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "permissions": permissions
        }
    }
