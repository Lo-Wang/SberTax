from fastapi import APIRouter, HTTPException
from app.database import async_session_maker
from app.crud import get_transaction, get_transactions, delete_transaction

router = APIRouter(prefix='/transactions', tags=['Работа с транзакциями'])

@router.get("/", summary="Получить список транзакций")
async def get_all_transactions(skip: int = 0, limit: int = 10):
    async with async_session_maker() as session:
        transaction = await get_transactions(session, skip=skip, limit=limit)
        return transaction

@router.get("/{transaction_id}", summary="Получить транзакцию по ID")
async def get_transaction_by_id(transaction_id: int):
    async with async_session_maker() as session:
        transaction = await get_transaction(session, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return transaction

@router.delete("/{transaction_id}", summary="Удалить транзакцию по ID")
async def delete_transaction_endpoint(transaction_id: int):
    async with async_session_maker() as session:
        # Проверяем, существует ли транзакция
        transaction = await get_transaction(session, transaction_id)

        if transaction is None:
            raise HTTPException(status_code=404, detail="Транзакция не найдена")

        # Удаляем транзакцию
        await delete_transaction(session, transaction_id)

        #return JSONResponse(status_code=204)  # Возвращаем 204 No Content