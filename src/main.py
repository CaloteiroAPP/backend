from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.connection import ensure_db_and_collection
from src.routers.expense_router import router as expense_router
from src.routers.session_router import router as session_router
from src.routers.user_router import router as user_router

tags_metadata = []
description = "CaloteiroAPP API is a simple API to manage expenses and debts between friends."

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="CaloteiroAPP API",
    description=description,
    openapi_tags=tags_metadata,
    version="0.0.1",
    contact={"name": "CaloteiroAPP"},
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers to the application
app.include_router(expense_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(session_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    ensure_db_and_collection()


@app.get("/")
async def root():
    return {"message": "Hello World"}
