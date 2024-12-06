from fastapi import APIRouter, HTTPException

from app.crud import get_user, get_users, get_user_by_username, create_user, update_user, delete_user
from app.database import async_session_maker
from app.users.schemas import User, UserCreate, UserUpdate

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

@router.get("/", summary="Получить список пользователей")
async def get_all_users(skip: int = 0, limit: int = 10):
    async with async_session_maker() as session:
        users = await get_users(session, skip=skip, limit=limit)
        return users

@router.get("/{user_id}", summary="Получить пользователя по ID", response_model=User )
async def get_user_by_id(user_id: int):
    async with async_session_maker() as session:  # Начинаем сессии
        user = await get_user(session, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user


# @router.post("/", summary="Создать нового пользователя", response_model=User)
# async def create_new_user(user: UserCreate):
#     async with async_session_maker() as session:  # Начинаем сессию
#         existing_user = await get_user_by_username(session, user.username)
#         if existing_user:
#             raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
#
#         new_user = await create_user(session, user)
#         return new_user


@router.put("/{user_id}", summary="Обновить информацию о пользователе", response_model=User )
async def update_user_info(user_id: int, user_update: UserUpdate):
    async with async_session_maker() as session:  # Начинаем сессию
        updated_user = await update_user(session, user_id, user_update)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return updated_user

@router.delete("/{user_id}", summary="Удалить пользователя")
async def delete_user_by_id(user_id: int):
    async with async_session_maker() as session:
        deleted_user = await delete_user(session, user_id)
        if deleted_user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return {"detail": "Пользователь успешно удален"}