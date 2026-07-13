from fastapi import FastAPI

from app.FastAPI.routes import router

app = FastAPI(
    title="Jarvis AIOS",
)

app.include_router(router)
