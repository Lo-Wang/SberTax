from fastapi import FastAPI, UploadFile, Form
from typing import List, Optional

app = FastAPI()

# Хранилище для транзакций и документов
transactions = []
documents = {}

@app.post("/authorize")
async def authorize_service(user_id: str):
    # Логика авторизации сервиса
    return {"message": f"Service authorized for user {user_id}"}

@app.get("/transactions/{user_id}")
async def get_transactions(user_id: str):
    # Получение транзакций по ID пользователя
    # Здесь должен быть доступ к базе данных или API для получения данных
    # Для демонстрации просто возвращаем тестовые данные
    global transactions
    transactions = [
        {"id": 1, "mcc": "1234", "category": "Category A"},
        {"id": 2, "mcc": "5678", "category": "Category B"}
    ]
    return {"transactions": transactions}

@app.get("/check_deduction/{user_id}")
async def check_deduction(user_id: str):
    # Проверка возможности вычета
    eligible_transactions = [t for t in transactions if t['category'] == 'Category A']
    return {"eligible_transactions": eligible_transactions}

@app.post("/request_documents/")
async def request_documents(missing_docs: List[str] = Form(...)):
    # Запрос недостающих документов у клиента
    return {"message": "Requesting missing documents", "missing_docs": missing_docs}

@app.post("/upload_document/{user_id}")
async def upload_document(user_id: str, file: UploadFile):
    # Загружает документ от клиента
    if user_id not in documents:
        documents[user_id] = []
    documents[user_id].append(file.filename)
    return {"message": f"Document {file.filename} uploaded successfully."}

@app.get("/validate_documents/{user_id}")
async def validate_documents(user_id: str):
    # Валидация загруженных документов
    if user_id not in documents or len(documents[user_id]) < 3:  # Пример условия
        return {"status": "pending", "message": "Missing documents, please upload more."}
    else:
        return {"status": "success", "message": "All documents are valid."}

@app.post("/submit_to_fns/{user_id}")
async def submit_to_fns(user_id: str):
    validation_result = await validate_documents(user_id)
    if validation_result["status"] == "success":
        return {"message": "Documents submitted to FNS for tax deduction."}
    else:
        return {"message": "Cannot submit due to missing documents."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)