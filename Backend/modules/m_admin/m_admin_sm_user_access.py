from fastapi import HTTPException, status
from modules.m_user.m_user_data import get_user_by_email, set_user_role, set_user_status
from modules.m_audit.m_audit_data import record_audit_event

def modify_user_role(target_email: str, new_role: str, admin_email: str) -> bool:
    user = get_user_by_email(target_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target user not found")
    set_user_role(target_email, new_role)
    record_audit_event("UPDATE_ROLE", admin_email, "SUCCESS", {"target": target_email, "new_role": new_role})
    return True

def toggle_user_account_state(target_email: str, is_active: bool, admin_email: str) -> bool:
    user = get_user_by_email(target_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target user not found")
    set_user_status(target_email, is_active)
    record_audit_event("TOGGLE_STATUS", admin_email, "SUCCESS", {"target": target_email, "is_active": is_active})
    return True
