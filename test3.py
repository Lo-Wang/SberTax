import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# Модели данных пока без бд
class Transaction(BaseModel):
    id: int
    amount: float
    category: str
    mcc_code: str


class Document(BaseModel):
    name: str
    is_received: bool


class UserToken(BaseModel):
    token: str


class UserData(BaseModel):
    user_id: int
    transactions: List[Transaction]
    documents: List[Document]


# Пример данных
fake_transactions = [
    Transaction(id=1, amount=100.0, category="Medical", mcc_code="1234"),
    Transaction(id=2, amount=200.0, category="Education", mcc_code="5678"),
]

fake_documents = [
    Document(name="Receipt", is_received=False),
    Document(name="Invoice", is_received=False),
]


@app.post("/authorize")
async def authorize_service():
    # Разрешить сервису доступ к транзакциям
    return {"message": "Сервису разрешен доступ к транзакциям"}


@app.post("/get_user_data/{user_id}", response_model=UserData)
async def get_user_data(user_id: int):
    # Получить информацию о транзакциях
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Неверный ID пользователя")

    # Запросить токен пользователя
    user_token = UserToken(token="example_token")

    transactions = fake_transactions  # Получение MCC-кодов и категорий транзакций
    documents = fake_documents

    # Проверить возможность вычета по данным категориям
    eligible_transactions = [tx for tx in transactions if tx.category in ["Medical", "Education"]]

    return UserData(user_id=user_id, transactions=eligible_transactions, documents=documents)


@app.post("/send_documents")
async def send_documents(user_data: UserData):
    # Провести валидацию отправленных документов
    missing_documents = [doc for doc in user_data.documents if not doc.is_received]

    if missing_documents:
        raise HTTPException(status_code=400, detail="Отсутствуют необходимые документы: " + ", ".join(
            [doc.name for doc in missing_documents]))

    # Конечное событие - отправка документов в ФНС
    return {"message": "Документы успешно отправлены в ФНС"}


@app.post("/receive_document/{document_name}")
async def receive_document(document_name: str):
    # Функция для получения документа
    for doc in fake_documents:
        if doc.name == document_name:
            doc.is_received = True
            return {"message": f"Документ {document_name} получен"}

    raise HTTPException(status_code=404, detail="Документ не найден")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)