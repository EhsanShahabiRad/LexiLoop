from fastapi import FastAPI, Request
from app.core.config import settings
from app.api.routes import user_routes, auth, user_profile
from fastapi.middleware.cors import CORSMiddleware
import time
from app.db import base
import inspect
import app.api.routes.auth as actual_auth
from app.api.routes import language_pairs

app = FastAPI(title=settings.project_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def combined_middleware(request: Request, call_next):
    if not settings.debug:
        return await call_next(request)

    start_time = time.time()
    try:
        body = await request.body()
        print(f"\n📥 REQUEST: {request.method} {request.url}")
        print(f"🔸 Headers: {dict(request.headers)}")
        print(f"🔸 Body: {body.decode('utf-8') if body else '(empty)'}")
    except Exception as e:
        print(f"⚠️ Failed to read request body: {e}")

    response = await call_next(request)

    duration = time.time() - start_time
    print(f"📤 RESPONSE status={response.status_code} duration={duration:.2f}s")
    print("🟰" * 50)

    return response



# @app.middleware("http")
# async def combined_middleware(request: Request, call_next):
#     start_time = time.time()
#     body = await request.body()

#     print(f"\n📥 REQUEST: {request.method} {request.url}")
#     print(f"🔸 Headers: {dict(request.headers)}")
#     print(f"🔸 Body: {body.decode('utf-8') if body else '(empty)'}")

#     response = await call_next(request)

#     duration = time.time() - start_time
#     print(f"📤 RESPONSE status={response.status_code} duration={duration:.2f}s")
#     print("🟰" * 50)

#     return response


# Route registration
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user_profile.router, prefix=settings.api_v1_str, tags=["profile"])
app.include_router(language_pairs.router, prefix="/api/v1/language-pairs", tags=["LanguagePairs"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": f"{settings.project_name} API is running!"}








# from fastapi import FastAPI, Request
# from app.core.config import settings
# from app.api.routes import user_routes, auth, user_profile
# from fastapi.middleware.cors import CORSMiddleware
# import time
# from app.db import base
# import inspect
# import app.api.routes.auth as actual_auth
# from app.api.routes import language_pairs

# app = FastAPI(title=settings.project_name, debug=settings.debug)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.middleware("http")
# async def noop_middleware(request: Request, call_next):
#     return await call_next(request)



# # 🔍 Log all requests and responses
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     start_time = time.time()
#     body = await request.body()

#     print(f"\n📥 REQUEST: {request.method} {request.url}")
#     print(f"🔸 Headers: {dict(request.headers)}")
#     print(f"🔸 Body: {body.decode('utf-8') if body else '(empty)'}")

#     response = await call_next(request)

#     duration = time.time() - start_time
#     print(f"📤 RESPONSE status={response.status_code} duration={duration:.2f}s")
#     print("🟰" * 50)

#     return response


# app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(user_profile.router, prefix=settings.api_v1_str, tags=["profile"])
# app.include_router(language_pairs.router, prefix="/api/v1/language-pairs", tags=["LanguagePairs"])


# @app.get("/")
# def read_root():
#     return {"message": f"{settings.project_name} API is running!"}
