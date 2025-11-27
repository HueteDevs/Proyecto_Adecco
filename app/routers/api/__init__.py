"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""


from app.routers.api import horarios

from fastapi import APIRouter

#router pricipal

router = APIRouter()

#incluir router de horarios en router principal
router.include_router(horarios.router)