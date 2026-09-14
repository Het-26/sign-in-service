from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


# --- Signup request ---
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


# --- User response ---
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Token response ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# --- Refresh token ---
class RefreshTokenRequest(BaseModel):
    refresh_token: str