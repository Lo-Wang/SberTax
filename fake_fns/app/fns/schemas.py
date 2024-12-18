from datetime import datetime
from pydantic import BaseModel

class DocumentBase(BaseModel):
    document_type: str
    filename: str
    upload_date: datetime
    status: str
    amount: float  # Добавляем поле для суммы
    category: str  # Добавляем поле для категории
    mcc_code: str  # Добавляем поле для кода MCC
    description: str  # Новое поле для описания

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    document_id: int

    class Config:
        from_attributes = True