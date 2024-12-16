from fastapi import APIRouter, HTTPException, Form

from app.Authorization.Auth import Token, authenticate_user, create_access_token
from app.crud import get_user_by_username, create_user
from app.database import async_session_maker
from app.users.schemas import User, UserCreate

router = APIRouter(prefix="/auth", tags=["Авторизация"])



@router.post("/registry", summary="Создать нового пользователя", response_model=Token)  # Измените response_model на Token
async def create_new_user(user: UserCreate):
    async with async_session_maker() as session:  # Начинаем сессию
        existing_user = await get_user_by_username(session, user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

        new_user = await create_user(session, user)

        # Создаем токен доступа
        access_token = await create_access_token(data={"sub": new_user.username})

        return Token(access_token=access_token, token_type="bearer", user_id=new_user.user_id,first_name=new_user.first_name,
            last_name=new_user.last_name)

@router.get("/login", summary="Меню входа")
async def login_menu():
    return {
        "username": "Имя пользователя",
        "password": "Пароль"
    }

@router.post("/login", summary="Вход", response_model=Token)
async def login(username: str = Form(...), password: str = Form(...)):
    async with async_session_maker() as session:  # Начинаем сессию
        user = await authenticate_user(username, password, session)

        if not user:  # Проверяем, был ли пользователь найден
            raise HTTPException(status_code=400, detail="Неверные учетные данные")

        access_token = await create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer", user_id=user.user_id, first_name=user.first_name,
            last_name=user.last_name)

@router.get("/users/me", summary="Получить информацию о текущем пользователе", response_model=User)
async def read_users_me(username: str):  # Принимаем имя пользователя как параметр
    async with async_session_maker() as session:  # Начинаем сессию
        user = await get_user_by_username(session, username)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user  # Возвращаем текущего пользователя