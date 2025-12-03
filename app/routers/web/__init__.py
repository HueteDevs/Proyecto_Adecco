"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""
# Habría que incluír el archivo home
from app.routers.web import pelicula
from app.routers.web import sala
from app.routers.web import venta
from app.routers.web import genre
from app.routers.web import horario

from fastapi import APIRouter

router = APIRouter()

router.include_router(pelicula.router)
router.include_router(sala.router)
router.include_router(venta.router)
router.include_router(genre.router)
router.include_router(horario.router)

