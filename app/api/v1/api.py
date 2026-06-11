from fastapi import APIRouter
from app.api.v1.endpoints.sala import router as sala_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(sala_router)
