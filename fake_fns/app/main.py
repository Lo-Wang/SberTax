from fastapi import FastAPI
from app.fns.router import router as router_documents

app = FastAPI()

app.include_router(router_documents)