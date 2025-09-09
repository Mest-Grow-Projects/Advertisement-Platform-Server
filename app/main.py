from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("DB Connection initialized")

    try:
        yield
    finally:
        print("DB Connection closed")


app = FastAPI(
    title="Advertisement Management Platform API Documentation",
    description="API documentation for the Advertisement Management Platform.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get(
    "/",
    tags=["App"],
    summary="Application base route"
)
def get_homepage():
    return {"message": "Welcome to the Advertisement Management Platform API!"}