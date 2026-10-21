# mira-backend
Conversational AI Backend with Role-Based Access Control (RBAC), multi-step registration, 2FA login, and audit logs.

## Setup Instructions
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
