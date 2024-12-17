from pydantic import BaseModel
from typing import List, Optional
from app.documents.schemas import Document

class TransactionBase(BaseModel):
    amount: float
    category: str
    mcc_code: str
    description: str
    user_id: Optional[int]  # Добавлено поле user_id

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    documents: List[Optional["Document"]] = []
    class Config:
        from_attributes = True