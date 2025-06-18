from fastapi import FastAPI
from app.routes import router 
import uvicorn

#  From project root to run server:
#  % PYTHONPATH=. uvicorn app.server:app --reload

app = FastAPI(title="Music PDF to Speech API")

app.include_router(router)


