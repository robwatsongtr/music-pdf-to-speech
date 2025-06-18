from fastapi import FastAPI
from app.routes import router 

#  From project root to run server:
#  % python3 -m uvicorn app.server:app --reload

app = FastAPI(title="Music PDF to Speech API")

app.include_router(router)



