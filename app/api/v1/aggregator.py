from fastapi import APIRouter

from app.api.v1.endpoints import login, users, email, files

api_router = APIRouter(prefix="/v1")
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(email.router)
api_router.include_router(files.router)
