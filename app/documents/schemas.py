from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.logs.schemas import Log

class DocumentBase(BaseModel):
    document_type: str
    filename: str
    upload_date: datetime
    status: str
    transaction_id: int

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    document_id: int
    logs: List[Optional["Log"]] = []

    class Config:
        from_attributes = True