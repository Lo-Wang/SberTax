from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.app.core.postgres.database import SessionLocal, Transaction
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модели Pydantic
class TransactionCreate(BaseModel):
    amount: float
    category: str
    mcc_code: str

class DocumentRequest(BaseModel):
    transaction_id: int
    documents: List[str]

class UserTransactionsResponse(BaseModel):
    transactions: List[TransactionCreate]

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/authorize")
async def authorize_service(user_id: str):
    return {"message": "Доступ разрешен"}

@app.get("/get_transactions/{user_id}", response_model=UserTransactionsResponse)
async def get_transactions(user_id: str, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return UserTransactionsResponse(transactions=[TransactionCreate(**t.__dict__) for t in transactions])