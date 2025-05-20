from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import user_routes

app = FastAPI(title=settings.project_name, debug=settings.debug)
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
@app.get("/")
def read_root():
    return {"message": f"{settings.project_name} API is running!"}