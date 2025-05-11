from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from pydantic.main import ConfigDict
from app.lib.datetime import UTCDateTime, get_datetime
from app.lib.utils import generate_uuid


class UserBase(BaseModel):
    id: str = Field(default_factory=lambda: generate_uuid(), alias="_id")
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., min_length=1, max_length=100)
    image: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)
    
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
class UserAuthProvider(str, Enum):
    GOOGLE = "google"
    CREDENTIALS = "credentials"
    
class User(UserBase):
    password: str
    provider: UserAuthProvider 
    status: UserStatus = UserStatus.ACTIVE
    role: UserRole = UserRole.USER
    is_email_verified: bool = False
    created_at: UTCDateTime = Field(default_factory=lambda: get_datetime(), alias="_created_at")
    updated_at: UTCDateTime = Field(default_factory=lambda: get_datetime(), alias="_updated_at")
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    
class UserResponse(User):
    password : str  = Field(..., exclude=True)
    model_config = ConfigDict(populate_by_name=True)

