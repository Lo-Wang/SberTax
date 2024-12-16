from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt  # Импортируем библиотеку pyjwt
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.crud import get_user_by_username, verify_password
from app.database import async_session_maker
from app.Authorization.schemas import TokenData

# Определяем схему для получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для аутентификации пользователя
async def authenticate_user(username: str, password: str, session: AsyncSession):
    user = await get_user_by_username(session, username)
    if user is None:
        return False  # Пользователь не найден

    # Используем verify_password для проверки пароля
    if not verify_password(password, user.password):
        return False  # Пароль неверный

    return user  # Возвращаем пользователя, если аутентификация успешна
# Функция для создания токена доступа
async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)  # Время жизни токена
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")  # Замените на ваш секретный ключ
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(async_session_maker)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Невозможно проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем токен
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])  # Замените на ваш секретный ключ
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:  # Обработка ошибок декодирования токена
        raise credentials_exception

    # Получаем пользователя по имени
    user = await get_user_by_username(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user