from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, List
from xsc_lib.xsc_lib_app.xsc_lib_a_security import get_current_user_claims, require_roles
from modules.m_admin.m_admin_data import list_all_system_users
from modules.m_admin.m_admin_sm_user_access import modify_user_role, toggle_user_account_state

router = APIRouter()

class ChangeRoleRequest(BaseModel):
    email: EmailStr
    new_role: str

class ToggleStatusRequest(BaseModel):
    email: EmailStr
    is_active: bool

@router.get("/users", response_model=List[Dict[str, Any]])
def get_all_users(user: Dict[str, Any] = Depends(get_current_user_claims)):
    require_roles(["Admin"])(user)
    return list_all_system_users()

@router.post("/change-role", status_code=status.HTTP_200_OK)
def change_role(payload: ChangeRoleRequest, user: Dict[str, Any] = Depends(get_current_user_claims)):
    require_roles(["Admin"])(user)
    modify_user_role(payload.email, payload.new_role, user["sub"])
    return {"message": f"Role updated to {payload.new_role} for {payload.email}"}

@router.post("/toggle-status", status_code=status.HTTP_200_OK)
def toggle_status(payload: ToggleStatusRequest, user: Dict[str, Any] = Depends(get_current_user_claims)):
    require_roles(["Admin"])(user)
    toggle_user_account_state(payload.email, payload.is_active, user["sub"])
    return {"message": f"Active status set to {payload.is_active} for {payload.email}"}
