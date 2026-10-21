from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from typing import Dict, Any, List
from xsc_lib.xsc_lib_app.xsc_lib_a_security import get_current_user_claims
from modules.m_chat.m_chat_sm_conversation import generate_role_bounded_response
from modules.m_chat.m_chat_data import retrieve_user_chat_history

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    role: str

@router.post("/query", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat_query(payload: ChatRequest, user: Dict[str, Any] = Depends(get_current_user_claims)):
    reply = generate_role_bounded_response(payload.prompt, user["role"], user["sub"])
    return ChatResponse(response=reply, role=user["role"])

@router.get("/history", response_model=List[Dict[str, Any]])
def chat_history(user: Dict[str, Any] = Depends(get_current_user_claims)):
    return retrieve_user_chat_history(user["sub"])
