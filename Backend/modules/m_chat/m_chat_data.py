from datetime import datetime, timezone
from typing import List, Dict, Any

CONVERSATION_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

def store_message(email: str, role: str, message: str):
    user_email = email.lower().strip()
    if user_email not in CONVERSATION_HISTORY:
        CONVERSATION_HISTORY[user_email] = []
    CONVERSATION_HISTORY[user_email].append({
        "sender": role,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

def retrieve_user_chat_history(email: str) -> List[Dict[str, Any]]:
    return CONVERSATION_HISTORY.get(email.lower().strip(), [])
