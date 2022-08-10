from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from jose import jwt
import datetime
from app.core.config import settings
from app.api import dependencies


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )

not_authenticated_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": "Not authenticated"},
        headers={"WWW-Authenticate": "Bearer"},
    )


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_email_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.EMAIL_TOKEN_SECRET_KEY, algorithm=settings.EMAIL_TOKEN_ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.REFRESH_TOKEN_ALGORITHM)
    return encoded_jwt


def decode_email_token(access_token: str = Depends(dependencies.oauth2_scheme)):
    if not access_token:
        raise not_authenticated_exception
    try:
        payload = jwt.decode(access_token, settings.EMAIL_TOKEN_SECRET_KEY,
                             algorithms=[settings.EMAIL_TOKEN_ALGORITHM])
        user_email = payload.get("sub")
    except Exception:
        raise credentials_exception
    return user_email


def decode_access_token(access_token: str = Depends(dependencies.oauth2_scheme)):
    if not access_token:
        raise not_authenticated_exception
    try:
        payload = jwt.decode(access_token, settings.ACCESS_TOKEN_SECRET_KEY,
                             algorithms=[settings.ACCESS_TOKEN_ALGORITHM])
    except Exception:
        raise credentials_exception
    return payload


def decode_refresh_token(refresh_token: str = Depends(dependencies.oauth2_scheme)):
    if not refresh_token:
        raise not_authenticated_exception
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET_KEY,
                             algorithms=[settings.REFRESH_TOKEN_ALGORITHM])
    except Exception:
        raise credentials_exception
    return payload
