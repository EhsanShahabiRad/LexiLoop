from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.project_name, debug=settings.debug)

@app.get("/")
def read_root():
    return {"message": f"{settings.project_name} API is running!"}