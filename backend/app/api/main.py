from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.postgres.database import SessionLocal, Transaction, Log, Document
from pydantic import BaseModel
from typing import List, Optional

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


# Модель для создания документа
class DocumentCreate(BaseModel):
    document_type: str
    filename: str
    upload_date: str  # Дата в строковом формате
    file_data: bytes
    status: str
    transaction_id: int

# Получение всех документов
@app.get("/documents/", response_model=List[DocumentCreate])
async def get_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents

# Создание логов
class LogCreate(BaseModel):
    timestamp: str  # Дата в строковом формате
    service_name: str
    log_level: str
    message: str
    user_id: int
    document_id: Optional[int] = None

@app.post("/logs/", response_model=LogCreate)
async def create_log(log: LogCreate, db: Session = Depends(get_db)):
    new_log = Log(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

# Получение всех логов
@app.get("/logs/", response_model=List[LogCreate])
async def get_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).all()
    return logs

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