from fastapi import Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.crud import get_user_by_username, verify_password
from app.database import async_session_maker
from app.Authorization.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def authenticate_user(username: str, password: str, session: AsyncSession):
    user = await get_user_by_username(session, username)
    if user is None:
        return False  # Пользователь не найден

    if not verify_password(password, user.password):
        return False  # Пароль неверный

    return user  # Возвращаем пользователя, если аутентификация успешна

async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)  # Время жизни токена
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")  # Замените на ваш секретный ключ
    return encoded_jwt

async def get_current_user(token: str, session: AsyncSession):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])  # Замените на ваш секретный ключ
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        first_name: str = payload.get("first_name")
        last_name: str = payload.get("last_name")

        if username is None:
            raise credentials_exception

        token_data = TokenData(
            username=username,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            access_token=token,
            token_type="bearer"
        )
    except jwt.PyJWTError:
        raise credentials_exception

    user = await get_user_by_username(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user