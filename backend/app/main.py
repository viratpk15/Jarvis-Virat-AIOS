from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Jarvis AIOS",
)

app.include_router(router)
