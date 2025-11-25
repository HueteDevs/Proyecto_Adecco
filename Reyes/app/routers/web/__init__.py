from app.routers.web import home
from app.routers.web import salas

from fastapi import APIRouter

router = APIRouter()

router.include_router(home.router)
router.include_router(salas.router)
