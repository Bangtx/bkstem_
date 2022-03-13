from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.setting import WEB_URL, APP_ENV, PROJECT_NAME
from config.database import db

from core.api_v1.api import api_router


docs_url = "/docs" if APP_ENV == "dev" else None
redoc_url = "/redoc" if APP_ENV == "dev" else None
openapi_url = "/openapi.json" if APP_ENV == "dev" else None

app = FastAPI(
    title=f"{PROJECT_NAME} api",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[WEB_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    if db.is_closed():
        db.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not db.is_closed():
        db.close()


app.include_router(api_router)
