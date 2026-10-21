from typing import List, Dict, Any
from modules.m_user.m_user_data import USER_DATABASE

def list_all_system_users() -> List[Dict[str, Any]]:
    return [
        {
            "email": u["email"],
            "name": u["name"],
            "role": u["role"],
            "is_registered": u["is_registered"],
            "is_active": u["is_active"]
        }
        for u in USER_DATABASE.values()
    ]
