from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import ensure_db_and_collection

# from routers.dare import router as router_dare

tags_metadata = []
description = """ """

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc",
              title="Splitways API",
              description=description,
              openapi_tags=tags_metadata,
              version="0.0.1",
              contact={
                  "name": "Splitways"
                  }
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()
app.include_router(prefix="/api", router=router)


@app.on_event("startup")
async def startup_event():
    ensure_db_and_collection()


@router.get("/")
async def root():
    return {"message": "Hello World"}