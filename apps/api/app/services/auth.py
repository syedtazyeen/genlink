import asyncio, requests, random, string
from fastapi import HTTPException, status

from app.core.security import get_security
from app.services.base import BaseService
from app.services.user import UserService
from app.models.user import User, UserResponse, UserAuthProvider
from app.models.auth import SignUpRequest, TokenResponse, PasswordResetCode
from app.models.response import StringResponse
from app.services.email import EmailService
from app.lib.datetime import get_datetime

class AuthService(BaseService):
    """Authentication service"""
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.security = get_security()
        self.email_service = EmailService()
        self.reset_password_code_collection = self.db["password_reset_codes"]

    async def authenticate_user_credentials(self, email: str, password: str) -> TokenResponse:
        """Authenticate user with credentials."""
        user_data = await self.user_service.get_user_by_email(email)

        if not user_data or not self.security.verify_password(password, user_data["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user = User(**user_data)
                
        token = self.security.create_access_token(data={"sub": str(user.id)})
        return TokenResponse(access_token=token, user=UserResponse(**user.dict()))

    async def create_user_credentials(self, payload: SignUpRequest) -> TokenResponse:
        """Register a new user with credentials."""
        if not await self.user_service.isEmailUnique(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
                headers={"WWW-Authenticate": "Bearer"},
            )
        hashed_password = self.security.create_hash_password(payload.password)
        user = User(**payload.dict(exclude={"password"}), provider=UserAuthProvider.CREDENTIALS, password=hashed_password)
        await self.user_service.create_user(user.dict(by_alias=True))

        asyncio.create_task(
            self.email_service.send_welcome_email(
                to_email=payload.email,
                full_name=payload.name,
            )
        )

        token = self.security.create_access_token(data={"sub": str(user.id)})
        return TokenResponse(access_token=token, user=UserResponse(**user.dict()))
    
    async def authenticate_user_google(self, code: str) -> TokenResponse:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
        "code": code,
        "client_id": self.config.GOOGLE_CLIENT_ID,
        "client_secret": self.config.GOOGLE_CLIENT_SECRET,
        "redirect_uri": self.config.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
        }
        token_resp = requests.post(token_url, data=data)
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        
        user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
        ).json()
        
        if not user_info or not user_info.get("email"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_data = await self.user_service.get_user_by_email(user_info["email"])
        if user_data:
            if user_data["provider"] != UserAuthProvider.GOOGLE:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Google authentication failed",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user = User(**user_data)
            token = self.security.create_access_token(data={"sub": str(user.id)})
            return TokenResponse(access_token=token, user=UserResponse(**user.dict()))  
        
        user = User(
            name=user_info["name"],
            email=user_info["email"], 
            password="", 
            image=user_info["picture"],
            provider=UserAuthProvider.GOOGLE,
            is_email_verified=True)
        await self.user_service.create_user(user.dict(by_alias=True))
        
        # Send welcome email
        asyncio.create_task(
            self.email_service.send_welcome_email(
                to_email=user_info["email"],
                full_name=user_info["name"],
            )
        )
        
        token = self.security.create_access_token(data={"sub": str(user.id)})
        return TokenResponse(access_token=token, user=UserResponse(**user.dict()))
    

    async def reset_password(self, email: str):
        user_data = await self.user_service.get_user_by_email(email)

        if not user_data:
            return StringResponse(value="Password reset code sent successfully if email exists")
        
        reset_code = "".join(random.choices(string.digits, k=6))
        expires_at = get_datetime(minutes=self.config.PASSWORD_RESET_CODE_EXPIRE_MINUTES)
        
        password_reset_code = PasswordResetCode(
            email=email,
            reset_code=reset_code,
            expires_at=expires_at,
        )
        
        await self.reset_password_code_collection.insert_one(password_reset_code.model_dump(by_alias=True))
        
        asyncio.create_task(
            self.email_service.send_password_reset_code(
                to_email=email,
                reset_code=reset_code,
            )
        ) 
        return StringResponse(value="Password reset code sent successfully if email exists")
    
    
    async def _verify_reset_code(self, email: str, reset_code: str):
        password_reset_code = await self.reset_password_code_collection.find_one(
            {
                "email": email, 
                "reset_code": reset_code,
                "is_used": False,
                "expires_at": {"$gt": get_datetime()},
            }
        )
        
        if not password_reset_code:
            return False
            
        return True
    
    
    async def verify_password_reset_code(self, email: str, reset_code: str):
        
        if not await self._verify_reset_code(email, reset_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset code",
            )
        
        return StringResponse(value="Reset code verified successfully")


    async def change_password(self, email: str, reset_code: str, password: str) -> UserResponse:
        if not await self._verify_reset_code(email, reset_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset code",
            )
            
        hashed_password = self.security.create_hash_password(password)    
        user_data = await self.user_service.update_user_by_email(email, {"password": hashed_password})
        user = User(**user_data)
        
        await self.reset_password_code_collection.update_one(
            {"email": email, "reset_code": reset_code},
            {"$set": {"is_used": True}},
        )

        return UserResponse(**user.dict())
        
        
    
    