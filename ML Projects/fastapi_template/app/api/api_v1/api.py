from fastapi import APIRouter
from app.api.api_v1.endpoints import sample ,token

api_router = APIRouter()

api_router.include_router(sample.router)
api_router.include_router(token.router)