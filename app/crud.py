from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas import UserCreate, UserUpdate
from app.transactions.schemas import TransactionCreate, Transaction
from app.logs.schemas import LogCreate, Log
from sqlalchemy.future import select
from app.documents.schemas import DocumentCreate, Document
from app.logs.models import Log as LogModel
from app.logs.models import Transaction as TransactionModel
from app.logs.models import Document as DocumentModel
from app.logs.models import User
import bcrypt

# CRUD операции для Transaction
async def get_transaction(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    result = await db.execute(select(TransactionModel).where(TransactionModel.id == transaction_id))
    return result.scalar_one_or_none()

async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Transaction]:
    result = await db.execute(select(TransactionModel).offset(skip).limit(limit))
    transactions = result.scalars().all()
    return list(transactions)

async def create_transaction(db: AsyncSession, transaction_create: TransactionCreate) -> TransactionModel:
    transaction = TransactionModel(**transaction_create.dict())
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)  # Обновляем объект, чтобы получить сгенерированные поля (например, transaction_id)
    return transaction

# CRUD операции для Log
async def get_log(db: AsyncSession, log_id: int) -> Optional[Log]:
    result = await db.execute(select(LogModel).where(LogModel.log_id == log_id))
    return result.scalar_one_or_none()

async def get_logs(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Log]:
    result = await db.execute(select(LogModel).offset(skip).limit(limit))
    return list(result.scalars())  # Преобразуем в список

async def create_log(db: AsyncSession, log_create: LogCreate) -> LogModel:
    log = LogModel(**log_create.dict())
    db.add(log)
    await db.commit()
    await db.refresh(log)  # Обновляем объект, чтобы получить сгенерированные поля (например, log_id)
    return log

# CRUD операции для Document
async def get_document(db: AsyncSession, document_id: int) -> Optional[Document]:
    result = await db.execute(select(DocumentModel).where(DocumentModel.document_id == document_id))
    return result.scalar_one_or_none()  # Возвращает Document или None

async def get_documents(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Document]:
    result = await db.execute(select(DocumentModel).offset(skip).limit(limit))
    return list(result.scalars())  # Преобразуем в список

async def create_document(db: AsyncSession, document_create: DocumentCreate) -> DocumentModel:
    document = DocumentModel(
        document_type=document_create.document_type,
        filename=document_create.filename,
        upload_date=document_create.upload_date,
        file_data=document_create.file_data,
        status=document_create.status,
        transaction_id=document_create.transaction_id
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)  # Обновляем объект, чтобы получить сгенерированные поля (например, document_id)
    return document

async def delete_document_by_id(db: AsyncSession, document_id: int) -> None:
    document = await get_document(db, document_id)
    if document:
        await db.delete(document)
        await db.commit()  # Сохраняем изменения
    else:
        raise HTTPException(status_code=404, detail="Документ не найден")

async def delete_transaction(db: AsyncSession, transaction_id: int) -> None:
    transaction = await get_transaction(db, transaction_id)
    if transaction:
        await db.delete(transaction)
        await db.commit()  # Сохраняем изменения
    else:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

# CRUD операции для USERS
async def get_users(session: AsyncSession, skip: int = 0, limit: int = 10):
    result = await session.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user: UserCreate) -> User:
    # Проверяем, существует ли уже пользователь с таким именем или email
    existing_user = await session.execute(
        select(User).where(User.username == user.username)
    )
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует.")

    existing_email = await session.execute(
        select(User).where(User.email == user.email)
    )
    if existing_email.scalars().first():
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")

    # Хэшируем пароль
    hashed_password = hash_password(user.password)

    # Создаем нового пользователя с хешированным паролем
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,  # Сохраняем хешированный пароль
    )

    # Добавляем нового пользователя в сессию и сохраняем в базе данных
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

async def update_user(session: AsyncSession, user_id: int, user_update: UserUpdate):
    user = await get_user(session, user_id)
    if user is None:
        return None

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = hash_password(user_update.password)  # Хэшируем новый пароль

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def delete_user(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    if user is None:
        return None

    await session.delete(user)
    await session.commit()
    return user