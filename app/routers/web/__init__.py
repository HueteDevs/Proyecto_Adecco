"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""
# Habría que incluír el archivo home

#from app.routers.web import pelicula
from app.routers.web import ventas
from app.routers.web import genre
from app.routers.web import horarios
from app.routers.web import home
from app.routers.web import salas

from fastapi import APIRouter

router = APIRouter()


#router.include_router(pelicula.router)
router.include_router(salas.router)
#router.include_router(venta.router)
router.include_router(horarios.router)

router.include_router(ventas.router)
router.include_router(genre.router)
router.include_router(home.router)

