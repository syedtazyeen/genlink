from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserResponse
from app.lib.datetime import get_datetime, UTCDateTime

class SignUpRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    
class TokenType(str, Enum):
    BEARER = "bearer"

class TokenResponse(BaseModel):
    access_token: str
    token_type: TokenType = Field(default=TokenType.BEARER)
    user: UserResponse
    

class PasswordResetRequest(BaseModel):
    email: EmailStr
    
class PasswordResetCode(BaseModel):
    email: EmailStr
    reset_code: str
    is_used: bool = False
    expires_at: UTCDateTime
    created_at: UTCDateTime = Field(default_factory=lambda: get_datetime(), alias="_created_at")
    
    
class VerifyResetCodeRequest(BaseModel):
    email: EmailStr
    reset_code: str
    
class ChangePasswordRequest(VerifyResetCodeRequest):
    new_password: str = Field(..., min_length=8, max_length=100)