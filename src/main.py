from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.collection import Collection

from src.database.connection import db, ensure_db_and_collection
from src.repositories.expense_repository import ExpenseRepository
from src.routers.expense_router import router as expense_router
from src.services.expense_service import ExpenseService

tags_metadata = []
description = """ """

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Splitways API",
    description=description,
    openapi_tags=tags_metadata,
    version="0.0.1",
    contact={"name": "Splitways"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the collections
expense_collection: Collection = db["expense"]

# Create an instance of the expense repository and service
expense_repository = ExpenseRepository(expense_collection)
expense_service = ExpenseService(expense_repository)

# Add routers to the application
app.include_router(expense_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    ensure_db_and_collection()


@app.get("/")
async def root():
    return {"message": "Hello World"}
