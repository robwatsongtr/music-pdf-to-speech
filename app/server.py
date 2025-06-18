from fastapi import FastAPI
from app.routes import router 
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

#  From project root to run server:
#  % PYTHONPATH=. uvicorn app.server:app --reload
#   or
#  % python3 -m uvicorn app.server:app --reload

app = FastAPI(title="Music PDF to Speech API")

app.include_router(router)



