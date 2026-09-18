from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.security import decode_access_token


def user_or_ip_key(request: Request) -> str:
    """
    Rate-limit key for authenticated endpoints.

    Uses the JWT subject so one user cannot spend another user's budget (and
    so users behind a shared proxy/NAT are not lumped into one bucket). Falls
    back to the client IP when there is no valid bearer token.
    """
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        payload = decode_access_token(auth[7:].strip())
        if payload and payload.get("sub") is not None:
            return f"user:{payload['sub']}"
    return get_remote_address(request)


limiter = Limiter(key_func=get_remote_address)
