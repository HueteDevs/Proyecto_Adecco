"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""



# Falta importar desde la carpeta api venta y pelicula
from app.routers.api import peliculas
from app.routers.api import horarios
from app.routers.api import genre
from app.routers.api import salas
from app.routers.api import ventas
from fastapi import APIRouter

# router principal
router = APIRouter()    


#incluir router de horarios en router principal
#router.include_router(pelicula.router)
router.include_router(peliculas.router)
router.include_router(salas.router)
router.include_router(ventas.router)
router.include_router(horarios.router)
router.include_router(genre.router)
