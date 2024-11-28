from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.transactions.schemas import TransactionCreate, Transaction, TransactionBase
from app.logs.schemas import LogCreate, Log
from sqlalchemy.future import select
from app.documents.schemas import DocumentCreate, Document
from app.logs.models import Log as LogModel
from app.logs.models import Transaction as TransactionModel
from app.logs.models import Document as DocumentModel

# CRUD операции для Transaction
async def get_transaction(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    result = await db.execute(select(TransactionModel).where(TransactionModel.id == transaction_id))
    return result.scalar_one_or_none()

async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Transaction]:
    result = await db.execute(select(TransactionModel).offset(skip).limit(limit))
    transactions = result.scalars().all()
    return list(transactions)

# CRUD операции для Log
async def get_log(db: AsyncSession, log_id: int) -> Optional[Log]:
    result = await db.execute(select(LogModel).where(LogModel.log_id == log_id))
    return result.scalar_one_or_none()

async def get_logs(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Log]:
    result = await db.execute(select(LogModel).offset(skip).limit(limit))
    return list(result.scalars())  # Преобразуем в список

# CRUD операции для Document
async def get_document(db: AsyncSession, document_id: int) -> Optional[Document]:
    result = await db.execute(select(DocumentModel).where(DocumentModel.document_id == document_id))
    return result.scalar_one_or_none()  # Возвращает Document или None

async def get_documents(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Document]:
    result = await db.execute(select(DocumentModel).offset(skip).limit(limit))
    return list(result.scalars())  # Преобразуем в список