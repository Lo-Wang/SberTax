from fastapi import APIRouter, HTTPException

from app.crud import get_documents, get_document
from app.database import async_session_maker

router = APIRouter(prefix='/documents', tags=['Работа с документами'])

@router.get("/", summary="Получить список документов")
async def get_all_documents(skip: int = 0, limit: int = 10):
    async with async_session_maker() as session:
        documents = await get_documents(session, skip=skip, limit=limit)
        return documents

@router.get("/{document_id}", summary="Получить документ по ID")
async def get_document_by_id(document_id: int):
    async with async_session_maker() as session:
        document = await get_document(session, document_id)  # Используем функцию CRUD

        if document is None:
            raise HTTPException(status_code=404, detail="Документ не найден")
        return document