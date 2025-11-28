"""
Configuración de la aplicación FastAPI
"""


# app/main.py
# Punto de entrada principal de la aplicación FastAPI.
# Contiene solo:
#  - Instancia de la app
#  - Inicialización de base de datos
#  - Montaje de estáticos
#  - Manejador global de errores
#  - Inclusión de routers
#  - Endpoint raíz que delega la lógica de Películas a utils_pelicula.py

from fastapi import FastAPI
from app.database import init_db
from app.routers.api import router as api_router
from app.routers.web import router as web_router

# crea la instancia de la aplicacion FastAPI
app = FastAPI(title="CinePython", version="1.0.0")

# inicializa la base de datos
init_db()
#registra los routers
app.include_router(api_router)
app.include_router(web_router)