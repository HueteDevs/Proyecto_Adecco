# app/main.py
# Punto de entrada principal de la aplicación FastAPI.
# Contiene solo:
#  - Instancia de la app
#  - Inicialización de base de datos
#  - Montaje de estáticos
#  - Manejador global de errores
#  - Inclusión de routers
#  - Endpoint raíz que delega la lógica de Películas a utils_pelicula.py

import os
from typing import Optional

from fastapi import FastAPI, Depends, Query, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from starlette.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config import APP_TITLE

# --- Configuración global y utilidades de infraestructura ---
from app.config import (
    APP_TITLE,
    templates,
    APP_METADATA,
    DB_FILE_PATH,
    SCHEMA_FILE_PATH,
    SEED_FILE_PATH,
    STATIC_DIR,
)

from app.database.db import get_db


# Importamos modelos para asegurar la creación de tablas
from app.models import pelicula, genero  

# Routers de la aplicación
from app.routers import pelicula_router, genero_router
# from app.routers import sala_router, socio_router, login_router  # cuando estén listos

# Utilidades específicas de la entidad Película
from app.utils_pelicula import cargar_datos_homepage, get_home_title



# 1. INSTANCIA PRINCIPAL DE LA APLICACIÓN
app = FastAPI(**APP_METADATA)

# Configuración sección static en main para imagenes, css etc
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Directorio base donde está main.py (app/)
BASE_DIR = Path(__file__).resolve().parent

# Montar la carpeta estática DENTRO de app (app/static) para imagenes, css etc
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

# 3. MANEJO GLOBAL DE ERRORES HTTP (404, etc.)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    """
    Maneja errores HTTP para servir una plantilla HTML personalizada en el 404
    y un mensaje HTML genérico para otros códigos.
    """
    if exc.status_code == 404:
        try:
            return templates.TemplateResponse(
                "404.html",
                {"request": request,
                "titulo": APP_TITLE},
                status_code=404,
            )
        except Exception:
            # Fallback si falla la carga de la plantilla
            return HTMLResponse(
                "<h1>404 Not Found</h1><p>Error en el servidor de la aplicación.</p>",
                status_code=404,
            )

    # Otros errores HTTP
    return HTMLResponse(
        f"<h1>Error {exc.status_code}</h1><p>{exc.detail}</p>",
        status_code=exc.status_code,
    )


# 4. MONTAJE DE ARCHIVOS ESTÁTICOS
try:
    app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name=STATIC_DIR)
except RuntimeError:
    # Si el directorio no existe, lo creamos y volvemos a montar
    print(f"⚠️ Advertencia: creando directorio '{STATIC_DIR}/' para archivos estáticos.")
    os.makedirs(STATIC_DIR, exist_ok=True)
    app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name=STATIC_DIR)


# 5. INCLUSIÓN DE ROUTERS
app.include_router(pelicula_router.router)
app.include_router(genero_router.router)
# app.include_router(sala_router.router)
# app.include_router(socio_router.router)
# app.include_router(login_router.router)


# 6. ENDPOINT RAÍZ (WEB UI) – Delegado a utilidades de Película
@app.get("/", tags=["Web UI"])
def homepage_cartelera(
    request: Request,
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None),
    genero_id: Optional[str] = Query(None),
    duracion_max: Optional[str] = Query(None),
    disponible: Optional[str] = Query(None),
):
    """
    Ruta principal de la UI web.
    La lógica de filtros y carga de datos se delega a utils_pelicula.cargar_datos_homepage.
    """
    peliculas, generos_disponibles, filtros_activos = cargar_datos_homepage(
        db=db,
        q=q,
        genero_id=genero_id,
        duracion_max=duracion_max,
        disponible=disponible,
    )

    return templates.TemplateResponse(
        "app/peliculas/index.html",
        {
            "request": request,
            "titulo": get_home_title(),
            "peliculas": peliculas,
            "generos": generos_disponibles,
            "filtros_activos": filtros_activos,
        },
    )
