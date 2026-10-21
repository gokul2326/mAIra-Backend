from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from xsc_lib.xsc_lib_app.xsc_lib_a_config import settings
from xsc_lib.xsc_lib_app.xsc_lib_a_middleware import RequestLoggingMiddleware
from modules.m_auth.m_auth import router as auth_router
from modules.m_user.m_user import router as user_router
from modules.m_chat.m_chat import router as chat_router
from modules.m_admin.m_admin import router as admin_router
from modules.m_audit.m_audit import router as audit_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Conversational AI Backend with RBAC & Secure Auth",
    version="1.0.0"
)

# Global Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

# Wire all module routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/api/user", tags=["User Identity"])
app.include_router(chat_router, prefix="/api/chat", tags=["AI Engine"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin Access"])
app.include_router(audit_router, prefix="/api/audit", tags=["Audit"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "online", "app": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
