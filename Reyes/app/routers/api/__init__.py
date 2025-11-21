from app.routers.api import salas
from fastapi import APIRouter

# router principal
router = APIRouter()    

# incluir router de salas en router principal
router.include_router(salas.router)