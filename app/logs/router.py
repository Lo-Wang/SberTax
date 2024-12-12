from fastapi import APIRouter, HTTPException
from app.database import async_session_maker
from app.crud import get_log, get_logs

router = APIRouter(prefix='/logs', tags=['Работа с логами'])

@router.get("/", summary="Получить список логов")
async def get_all_logs(skip: int = 0, limit: int = 10):
    async with async_session_maker() as session:
        logs = await get_logs(session, skip=skip, limit=limit)
        return logs

@router.get("/{log_id}", summary="Получить лог по ID")
async def get_log_by_id(log_id: int):
    async with async_session_maker() as session:
        log = await get_log(session, log_id)  # Используем функцию CRUD

        if log is None:
            raise HTTPException(status_code=404, detail="Лог не найден")
        return log