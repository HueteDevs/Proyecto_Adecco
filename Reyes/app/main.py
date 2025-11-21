"""
Configuración de la aplicación FastAPI
"""

from fastapi import FastAPI
from app.routers.api import router as api_router

# crea la instancia de la aplicación FastAPI
app = FastAPI(title="Salas", version="1.0.0")

# inicializa la base de datos con canciones por defecto

# registrar los routers
app.include_router(api_router)
