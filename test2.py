from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List

app = FastAPI()

# схема для авторизации клиента
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Client(BaseModel):
    id: int
    token: str

class Transaction(BaseModel):
    id: int
    category: str
    mss_code: str

class Document(BaseModel):
    id: int
    type: str
    content: str

# Хранилище для демонстрации
clients = {}
transactions = {}
documents = {}

@app.post("/authorize")
async def authorize_client(client_id: int, token: str = Depends(oauth2_scheme)):
    # Авторизация клиента и сохранение токена
    # clients[client_id] = token
    return {"message": "Клиент авторизован"}

@app.get("/transactions")
async def get_transactions(client_id: int):
    # Получение транзакций для авторизованного клиента
    if client_id not in clients:
        raise HTTPException(status_code=401, detail="Клиент не авторизован")
    # Симуляция получения транзакций из бд или серва
    transactions_for_client = [
        Transaction(id=1, category="Еда", mss_code="1234"),
        Transaction(id=2, category="Транспорт", mss_code="5678"),
    ]
    return {"transactions": transactions_for_client}

@app.post("/request_documents")
async def request_documents(client_id: int, transaction_ids: List[int]):
    # Запрос документов для выбранных транзакций
    if client_id not in clients:
        raise HTTPException(status_code=401, detail="Клиент не авторизован")
    # Симуляция получения документов из бд или серва
    documents_for_transactions = [
        Document(id=1, type="Чек", content="Содержимое документа 1"),
        Document(id=2, type="Счет", content="Содержимое документа 2"),
    ]
    return {"documents": documents_for_transactions}

@app.post("/validate_documents")
async def validate_documents(client_id: int, documents: List[Document]):
    # Валидация отправленных документов
    if client_id not in clients:
        raise HTTPException(status_code=401, detail="Клиент не авторизован")
    # +- логика для валидации
    for document in documents:
        if document.type == "Invalid":
            raise HTTPException(status_code=400, detail="Некорректный документ")
    return {"message": "Документы успешно провалидированы"}

@app.post("/submit_documents")
async def submit_documents(client_id: int, documents: List[Document]):
    # Отправка документов в ФНС
    if client_id not in clients:
        raise HTTPException(status_code=401, detail="Клиент не авторизован")
    # Симуляция отправки документов в ФНС
    return {"message": "Документы успешно отправлены в ФНС"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)