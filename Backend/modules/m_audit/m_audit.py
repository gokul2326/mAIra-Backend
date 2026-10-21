from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from xsc_lib.xsc_lib_app.xsc_lib_a_security import get_current_user_claims, require_roles
from modules.m_audit.m_audit_data import query_audit_logs

router = APIRouter()

@router.get("/logs", response_model=List[Dict[str, Any]])
def get_logs(
    limit: int = Query(50, ge=1, le=200),
    user: Dict[str, Any] = Depends(get_current_user_claims)
):
    require_roles(["Admin"])(user)
    return query_audit_logs(limit=limit)
