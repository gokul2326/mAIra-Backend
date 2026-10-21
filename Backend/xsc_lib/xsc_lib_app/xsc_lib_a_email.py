from xsc_lib.xsc_lib_app.xsc_lib_a_logging import logger

def dispatch_otp_email(recipient_email: str, otp: str, purpose: str = "Verification") -> bool:
    logger.info(f"[EMAIL SERVICE] Dispatched {purpose} OTP to '{recipient_email}': {otp}")
    return True
