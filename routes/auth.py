from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

from database import get_db
from models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# JWT configuration
SECRET_KEY = "smarthire-dev-secret"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


# Login request body
class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    # Find user
    user = (
        db.query(User)
        .filter(User.username == login_data.username)
        .first()
    )

    # Check username/password
    if not user or user.password != login_data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT payload
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(
            minutes=TOKEN_EXPIRE_MINUTES
        )
    }

    # Generate token
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }