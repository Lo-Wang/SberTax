from pydantic import BaseModel

# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str

# Схема для данных токена
class TokenData(BaseModel):
    username: str

# Определяем простую схему для входа
class TokenRequest(BaseModel):
    username: str
    password: str