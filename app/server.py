from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Music PDF to Speech API")

app.include_router(router)
