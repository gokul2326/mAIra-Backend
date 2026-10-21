from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
from xsc_lib.xsc_lib_app.xsc_lib_a_security import get_current_user_claims
from modules.m_user.m_user_sm_profile import get_profile_details

router = APIRouter()

@router.get("/me", status_code=status.HTTP_200_OK)
def get_my_profile(current_user: Dict[str, Any] = Depends(get_current_user_claims)):
    profile = get_profile_details(current_user["sub"])
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile
