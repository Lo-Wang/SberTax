from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.logs.router import router as router_logs
from app.documents.router import router as router_documents
from app.transactions.router import router as router_transactions
from app.users.router import router as router_users
from app.Authorization.router import router as router_auth

app = FastAPI()

origins = [
    "http://localhost:3000",  # React приложение работает на этом порту
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home_page():
    return {"message": "Hello world!"}

app.include_router(router_auth)
app.include_router(router_logs)
app.include_router(router_documents)
app.include_router(router_transactions)
app.include_router(router_users)