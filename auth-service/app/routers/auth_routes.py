import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.auth_schema import (
    RegisterRequest, RegisterResponse, LoginRequest,
    LoginResponse, UserResponse, TokenVerificationResponse,
    ChangePasswordRequest
)
from app.services.auth_service import (
    register_user, login_user, change_user_password
)
from app.core.security import decode_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication token required")

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload.get("sub"))
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return user

@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(data, db)
    return {"message": "Registration successful", "user": user}

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user, token = login_user(data.email, data.password, db)
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user

@router.post("/verify-token", response_model=TokenVerificationResponse)
def verify_token(user: User = Depends(get_current_user)):
    return {
        "valid": True,
        "message": "Token is valid",
        "user_id": user.id,
        "role": user.role
    }

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    change_user_password(
        user, data.current_password, data.new_password, db
    )
    return {"message": "Password changed successfully"}
