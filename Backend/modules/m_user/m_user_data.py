from typing import Optional, Dict, Any

USER_DATABASE: Dict[str, Dict[str, Any]] = {
    "onboarding.user@company.com": {
        "email": "onboarding.user@company.com",
        "name": "Jane Doe",
        "password_hash": None,
        "role": "Data Analyst",
        "is_registered": False,
        "is_active": True
    },
    "existing.user@company.com": {
        "email": "existing.user@company.com",
        "name": "John Smith",
        # Default bcrypt hash for 'Password123!'
        "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "role": "Senior Engineer",
        "is_registered": True,
        "is_active": True
    },
    "admin.user@company.com": {
        "email": "admin.user@company.com",
        "name": "Sarah Connor",
        # Default bcrypt hash for 'AdminPassword123!'
        "password_hash": "$2b$12$4mU8dJox9KjVw2V0R7ZkE.L3R3yL7R2QfA6.79iM.aJz6O6s6uGeq",
        "role": "Admin",
        "is_registered": True,
        "is_active": True
    }
}

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    return USER_DATABASE.get(email.lower().strip())

def update_user_password(email: str, password_hash: str) -> bool:
    user = get_user_by_email(email)
    if not user:
        return False
    user["password_hash"] = password_hash
    user["is_registered"] = True
    return True

def set_user_role(email: str, new_role: str) -> bool:
    user = get_user_by_email(email)
    if not user:
        return False
    user["role"] = new_role
    return True

def set_user_status(email: str, is_active: bool) -> bool:
    user = get_user_by_email(email)
    if not user:
        return False
    user["is_active"] = is_active
    return True
