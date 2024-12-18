from datetime import datetime
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from starlette.responses import JSONResponse

from app.fns.schemas import DocumentCreate
from app.fns.models import Document
from app.database import async_session_maker

router = APIRouter()

@router.post("/")  # Убедитесь, что путь соответствует вашему запросу
async def save_document(
    amount: float = Form(...),
    category: str = Form(...),
    mcc_code: str = Form(...),
    description: str = Form(...),  # Новое поле для описания
    file: UploadFile = File(...)  # Обработка загружаемого файла
):
    try:
        async with async_session_maker() as session:
            # Создаем объект DocumentCreate
            create_document = DocumentCreate(
                document_type=file.filename.split(".")[-1],  # Получаем тип документа
                filename=file.filename,
                upload_date=datetime.now(),
                status="success",  # Или другой статус, если нужно
                amount=amount,
                category=category,
                mcc_code=mcc_code,
                description=description  # Добавлено новое поле для описания
            )

            # Создаем новый документ
            document = Document(
                document_type=create_document.document_type,
                filename=create_document.filename,
                upload_date=create_document.upload_date,
                status=create_document.status,
                amount=create_document.amount,
                category=create_document.category,
                mcc_code=create_document.mcc_code,
                description=create_document.description  # Добавлено новое поле для описания
            )
            session.add(document)
            await session.commit()
            return JSONResponse(status_code=201, content={"message": "Документ сохранен"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))