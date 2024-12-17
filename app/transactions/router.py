from fastapi import APIRouter, HTTPException, Header

from app.Authorization.Auth import get_current_user
from app.database import async_session_maker
from app.crud import get_transaction, get_transactions

router = APIRouter(prefix='/transactions', tags=['Работа с транзакциями'])

@router.get("/my", summary="Мои заявки")
async def get_transaction_me(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split(" ")[1]  # Получаем токен из "Bearer <token>"

    async with async_session_maker() as session:
        user = await get_current_user(token, session)
        transactions = await get_transactions(session, user_id=user.user_id)

        return transactions  # Возвращаем все транзакции для пользователя

@router.get("/{transaction_id}", summary="Получить транзакцию по ID")
async def get_transaction_by_id(transaction_id: int):
    async with async_session_maker() as session:
        transaction = await get_transaction(session, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return transaction

# @router.delete("/{transaction_id}", summary="Удалить транзакцию по ID")
# async def delete_transaction_endpoint(transaction_id: int):
    #    async with async_session_maker() as session:
        # Проверяем, существует ли транзакция
    #      transaction = await get_transaction(session, transaction_id)

    #       if transaction is None:
    #           raise HTTPException(status_code=404, detail="Транзакция не найдена")

    #       # Удаляем транзакцию
#      await delete_transaction(session, transaction_id)

        #return JSONResponse(status_code=204)  # Возвращаем 204 No Content