from app.api.api_v1.endpoints import user
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
