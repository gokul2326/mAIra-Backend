from datetime import datetime, timezone
from typing import List, Dict, Any

AUDIT_LOGS: List[Dict[str, Any]] = []

def record_audit_event(action: str, email: str, status_str: str, metadata: Dict[str, Any] = None):
    AUDIT_LOGS.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "email": email,
        "status": status_str,
        "metadata": metadata or {}
    })

def query_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    return AUDIT_LOGS[-limit:]
