from fastapi import Depends , Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")

async def get_current_user(request: Request,  token: str = Depends(oauth2_scheme)) -> UserResponse:
    payload = request.app.decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    user =  await request.app.mongodb["users"].find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user)
