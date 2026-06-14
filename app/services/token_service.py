"""
TokenService — decode JWT access tokens and extract typed user information.

Usage:
    from app.services.token_service import TokenService

    # In a FastAPI endpoint (no DB call needed):
    payload = TokenService.get_user_info(credentials.credentials)
    print(payload.email, payload.exam_type)

    # Or use the FastAPI dependency:
    from app.services.token_service import get_token_payload
    payload: TokenPayload = Depends(get_token_payload)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.schemas.user import TokenPayload

_security = HTTPBearer()


class TokenService:
    """Utilities for decoding and extracting user info from JWT tokens."""

    @staticmethod
    def get_user_info(token: str) -> TokenPayload:
        """
        Decode a JWT access token and return typed user information.

        Raises HTTPException 401 if token is invalid or missing required fields.
        """
        payload = decode_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is not an access token",
            )

        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID",
            )

        return TokenPayload(
            sub=user_id,
            email=payload.get("email", ""),
            full_name=payload.get("full_name", ""),
            exam_type=payload.get("exam_type"),
            target_score=payload.get("target_score"),
            type=payload.get("type", "access"),
        )

    @staticmethod
    def get_user_id(token: str) -> str:
        """Extract only the user UUID string from the token."""
        return TokenService.get_user_info(token).sub


# ── FastAPI dependency ────────────────────────────────────────────────────────

def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
) -> TokenPayload:
    """
    FastAPI dependency — injects decoded token payload.

    Use when you need user info from the JWT without a DB call.

    Example:
        @router.get("/me/info")
        async def my_info(payload: TokenPayload = Depends(get_token_payload)):
            return {"email": payload.email, "exam": payload.exam_type}
    """
    return TokenService.get_user_info(credentials.credentials)
