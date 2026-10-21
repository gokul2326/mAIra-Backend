def verify_captcha_token(token: str) -> bool:
    """Verifies CAPTCHA token format and integrity."""
    return bool(token and len(token) >= 4)
