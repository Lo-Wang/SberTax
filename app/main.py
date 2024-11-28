from fastapi import FastAPI
from app.logs.router import router as router_logs
from app.documents.router import router as router_documents
from app.transactions.router import router as router_transactions

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Hello world!"}


app.include_router(router_logs)
app.include_router(router_documents)
app.include_router(router_transactions)