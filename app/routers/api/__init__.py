"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""


from app.routers.web import home
from app.routers.web import pelicula
from app.routers.web import sala
from app.routers.web import venta
from app.routers.web import genre

# Falta importar desde la carpeta api venta y pelicula
from app.routers.api import horarios
from app.routers.api import genre
from app.routers.api import salas

from fastapi import APIRouter

# router principal
router = APIRouter()    


#incluir router de horarios en router principal
router.include_router(pelicula.router)
router.include_router(sala.router)
router.include_router(venta.router)
router.include_router(horarios.router)
router.include_router(genre.router)
