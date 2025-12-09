"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""

from app.routers.web import horarios
from app.routers.web import genre
from app.routers.web import salas
from app.routers.web import ventas

from fastapi import APIRouter

router = APIRouter()

router.include_router(horarios.router)
router.include_router(genre.router)
router.include_router(salas.router)
router.include_router(ventas.router)
