from fastapi import APIRouter
from src.web.api import healthcheck, messages



main_router = APIRouter(prefix="/api")

main_router.include_router(healthcheck.router)

main_router.include_router(messages.router)