from typing import Dict, List

ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "Admin": ["chat:read", "chat:write", "admin:all", "user:manage", "audit:read"],
    "Senior Engineer": ["chat:read", "chat:write", "code:execute"],
    "Data Analyst": ["chat:read", "chat:write", "data:query"],
    "Employee": ["chat:read", "chat:write"]
}

def get_permissions_for_role(role: str) -> List[str]:
    return ROLE_PERMISSIONS.get(role, ["chat:read"])
