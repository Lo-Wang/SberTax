from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

# Базовая схема для пользователя
class UserBase(BaseModel):
    username: constr(min_length=1, max_length=50)  # Ограничение на длину имени пользователя
    email: EmailStr  # Валидация электронной почты
    password: constr(min_length=8)  # Минимальная длина пароля
    first_name: constr(min_length=1, max_length=50)  # Имя пользователя
    last_name: constr(min_length=1, max_length=50)  # Фамилия пользователя
    coins: float = 0  # Поле для хранения результата, по умолчанию 0

# Схема для создания нового пользователя
class UserCreate(UserBase):
    pass

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    username: constr(min_length=1, max_length=50) = None
    email: EmailStr = None
    password: constr(min_length=8) = None
    first_name: constr(min_length=1, max_length=50) = None
    last_name: constr(min_length=1, max_length=50) = None
    coins: float = None  # Добавьте coins для обновления

# Схема для отображения пользователя
class User(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True