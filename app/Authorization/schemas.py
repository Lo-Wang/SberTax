from pydantic import BaseModel

# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    first_name: str  # Добавлено поле для имени
    last_name: str   # Добавлено поле для фамилии

# Схема для данных токена
class TokenData(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    first_name: str
    last_name: str
    username: str  # Добавьте это поле, если оно необходимо

# Определяем простую схему для входа
class TokenRequest(BaseModel):
    username: str
    password: str