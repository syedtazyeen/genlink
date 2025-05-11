"""Authentication API"""
import json
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse, HTMLResponse
from app.services.auth import AuthService
from app.models.user import UserResponse
from app.models.auth import SignUpRequest, TokenResponse, PasswordResetRequest, VerifyResetCodeRequest, ChangePasswordRequest
from app.core.config import get_config
from app.routes.deps import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/sign-up", response_model=TokenResponse)
async def sign_up_credentials(payload: SignUpRequest):
    """ Register a new user and get access token """
    return await auth_service.create_user_credentials(payload)

@router.post("/sign-in", response_model=TokenResponse)
async def sign_in_credentials(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 login to receive token"""
    return await auth_service.authenticate_user_credentials(form_data.username, form_data.password)

@router.post("/forgot-password")
async def forgot_password_credentials(payload: PasswordResetRequest):
    """Send password reset code to email"""
    return await auth_service.reset_password(payload.email)

@router.post("/verify-reset-code")
async def verify_password_reset_code(payload: VerifyResetCodeRequest):
    """Verify password reset code"""
    return await auth_service.verify_password_reset_code(payload.email, payload.reset_code)

@router.post("/reset-password", response_model=UserResponse)
async def reset_password_credentials(payload:ChangePasswordRequest):
    """Change password with reset code"""
    return await auth_service.change_password(payload.email, payload.reset_code, payload.new_password)

@router.get("")
async def read_current_user(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    """Get the current user"""
    return current_user

@router.get("/google")
async def sign_in_google():
    """Redirects the user to Google OAuth URL."""
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={get_config().GOOGLE_CLIENT_ID}"
        f"&redirect_uri={get_config().GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
        "&prompt=consent"
        "&access_type=offline"
        "&include_granted_scopes=true"
    )
    return RedirectResponse(auth_url)

@router.get("/google/callback", response_class=HTMLResponse)
async def sign_in_google_callback(code: str):
    try:
        res = await auth_service.authenticate_user_google(code)
        data = jsonable_encoder(res)
    except Exception as e:
        data = {
            "error": str(e)
        }

    html = f"""
    <html>
        <body>
            <script>
                window.opener.postMessage({json.dumps(data)}, "*");
                window.close();
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html)