import logging
from datetime import datetime

import requests
from fastapi import APIRouter, HTTPException, File, UploadFile
from starlette.responses import JSONResponse
from app.crud import get_documents, get_document, create_document, create_transaction, create_log, \
    delete_document_and_related, send_request
from app.database import async_session_maker
from app.documents.schemas import DocumentCreate
from app.logs.schemas import LogCreate
from app.transactions.schemas import TransactionCreate

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

@router.post("/", summary="Загрузить новый документ")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Читаем данные файла
        file_data = await file.read()

        async with async_session_maker() as session:
            # Создаем новую транзакцию с переданными данными
            transaction_create = TransactionCreate(
                amount=0.0,
                category="",
                mcc_code=""
            )
            transaction = await create_transaction(session, transaction_create)

            # Устанавливаем статус на "success" после успешной загрузки файла
            status = "success"

            # Создаем объект документа с полученным transaction_id
            document_create = DocumentCreate(
                document_type=file.filename.split(".")[-1],
                filename=file.filename,
                upload_date=datetime.now(),
                file_data=file_data,
                status=status,
                transaction_id=transaction.id  # Используем transaction.id
            )

            # Сохраняем документ в базе данных
            document = await create_document(session, document_create)

            # Создаем лог о загрузке документа
            log_create = LogCreate(
                service_name="Document Upload Service",
                log_level="INFO",
                message=f"Загружен документ: {document.filename} с ID транзакции: {transaction.id}",
                user_id=1,
                document_id=document.document_id
            )
            await create_log(session, log_create)  # Создание лога

            # Отправляем запрос на второй сервер для сохранения документа
            url = "http://localhost:7000/"
            response = await send_request(url, document_create)

            # Проверяем статус ответа
            #if response.status == 200:
            #    text = await response.text()
            #    return JSONResponse(status_code=201, content={"document_id": document.document_id})
            #else:
            #    raise HTTPException(status_code=400, detail="Ошибка сохранения документа на втором сервере")

    except Exception as e:
        # Обработка ошибок
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{document_id}", summary="Удалить документ по ID")
async def delete_document(document_id: int):
    async with async_session_maker() as session:
        # Удаляем документ и связанные записи
        await delete_document_and_related(session, document_id)
        return {"detail": "Документ и связанные записи успешно удалены"}