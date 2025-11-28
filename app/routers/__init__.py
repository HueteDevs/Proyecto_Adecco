"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""

from app.routers.web import horarios


from fastapi import APIRouter

router = APIRouter()

router.include_router(horarios.router)