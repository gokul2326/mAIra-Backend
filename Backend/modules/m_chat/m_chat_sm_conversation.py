from modules.m_chat.m_chat_data import store_message

def generate_role_bounded_response(prompt: str, user_role: str, user_email: str) -> str:
    store_message(user_email, "user", prompt)

    if user_role == "Admin":
        reply = f"[Admin Context] Full access granted. Processed: '{prompt}'"
    elif user_role == "Data Analyst":
        reply = f"[Analyst Context] Access to data queries and visualizations granted. Processed: '{prompt}'"
    elif user_role == "Senior Engineer":
        reply = f"[Engineering Context] Access to systems and code telemetry granted. Processed: '{prompt}'"
    else:
        reply = f"[General Context] Basic assistance. Processed: '{prompt}'"

    store_message(user_email, "assistant", reply)
    return reply
