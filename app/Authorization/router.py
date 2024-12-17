from fastapi import APIRouter, HTTPException, Form, Response, Depends, Cookie, Header
from app.Authorization.Auth import authenticate_user, create_access_token, oauth2_scheme, get_current_user
from app.Authorization.schemas import TokenData, Token
from app.crud import get_user_by_username, create_user
from app.database import async_session_maker
from app.users.schemas import User, UserCreate

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/registry", summary="Создать нового пользователя", response_model=Token)
async def create_new_user(user: UserCreate):
    async with async_session_maker() as session:
        existing_user = await get_user_by_username(session, user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

        new_user = await create_user(session, user)

        access_token = await create_access_token(data={"sub": new_user.username})

        return Token(access_token=access_token, token_type="bearer", user_id=new_user.user_id,
                     first_name=new_user.first_name, last_name=new_user.last_name)

@router.post("/login", summary="Вход", response_model=TokenData)
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    async with async_session_maker() as session:
        user = await authenticate_user(username, password, session)

        if not user:
            raise HTTPException(status_code=400, detail="Неверные учетные данные")

        access_token = await create_access_token(data={
            "sub": user.username,
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
        response.set_cookie(key="access_token", value=access_token)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        }

@router.get("/users/me", summary="Получить информацию о текущем пользователе", response_model=User )
async def read_users_me(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Извлекаем токен из заголовка
    token = authorization.split(" ")[1]  # Получаем токен из "Bearer <token>"

    async with async_session_maker() as session:
        user = await get_current_user(token, session)
        return user