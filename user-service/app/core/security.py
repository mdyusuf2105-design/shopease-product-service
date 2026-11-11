import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db


bearer_scheme = HTTPBearer(auto_error=False)


def get_authenticated_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> int:

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication token required"
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = int(payload.get("sub"))

        if user_id <= 0:
            raise ValueError("Invalid user ID")

        return user_id

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token"
        )
