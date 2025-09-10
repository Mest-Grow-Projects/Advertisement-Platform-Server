from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import init_db
from app.auth.auth_router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.food.food_route import router as food_router


origins = [
    "http://localhost:4200",
    "http://localhost:8080",
]


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
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["App"], summary="Application base route")
def get_homepage():
    return {"message": "Welcome to the Advertisement Management Platform API!"}


app.include_router(auth_router, prefix="/auth")
app.include_router(food_router, prefix="/food")
