from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import user_routes, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.project_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
app.include_router(auth.router, prefix=settings.api_v1_str, tags=["auth"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": f"{settings.project_name} API is running!"}
