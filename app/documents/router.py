from datetime import datetime

from fastapi import APIRouter, HTTPException, File, UploadFile
from starlette.responses import JSONResponse

from app.crud import get_documents, get_document, create_document, create_transaction, create_log, delete_document_and_related
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
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "",
    status: str = "pending",  # Устанавливаем статус по умолчанию
    amount: float = 0.0,
    category: str = "",
    mcc_code: str = "",
    user_id: int = 1  # Предполагаем, что вы получаете user_id откуда-то (например, из токена)
):
    try:
        # Читаем данные файла
        file_data = await file.read()

        async with async_session_maker() as session:
            # Создаем новую транзакцию с переданными данными
            transaction_create = TransactionCreate(
                amount=amount,
                category=category,
                mcc_code=mcc_code
            )
            transaction = await create_transaction(session, transaction_create)

            # Устанавливаем статус на "success" после успешной загрузки файла
            status = "success"

            # Создаем объект документа с полученным transaction_id
            document_create = DocumentCreate(
                document_type=document_type,
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
                user_id=user_id,
                document_id=document.document_id
            )
            await create_log(session, log_create)  # Создание лога

        return JSONResponse(status_code=201, content={"document_id": document.document_id})

    except Exception as e:
        # Обработка ошибок
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{document_id}", summary="Удалить документ по ID")
async def delete_document(document_id: int):
    async with async_session_maker() as session:
        # Удаляем документ и связанные записи
        await delete_document_and_related(session, document_id)
        return {"detail": "Документ и связанные записи успешно удалены"}