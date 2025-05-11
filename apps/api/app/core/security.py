from datetime import timedelta
from passlib.context import CryptContext
from functools import lru_cache
from jose import jwt
from authlib.integrations.starlette_client import OAuth
from app.lib.datetime import get_datetime
from app.core.config import get_config

class Security:
    settings = get_config()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    oauth = OAuth()
    oauth.register(
      name="google",
      client_id=settings.GOOGLE_CLIENT_ID,
      client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    refresh_token_url=None,
    authorize_state=settings.SECRET_KEY,
    redirect_uri="http://127.0.0.1:8000/auth",
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    client_kwargs={"scope": "openid profile email"},
)
    
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)
    
    @classmethod
    def create_access_token(cls, data: dict) -> str:
        expire = get_datetime() + timedelta(minutes=cls.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {**data, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, cls.settings.SECRET_KEY, algorithm=cls.settings.ALGORITHM)
        return encoded_jwt
    
    
@lru_cache()
def get_security() -> Security:
    return Security()