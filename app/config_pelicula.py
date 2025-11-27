# app/config_pelicula.py
"""
Configuración específica del módulo de Películas.
Centraliza textos, constantes y nombres de parámetros de filtro.
"""

from typing import Final

# Título para la página principal de la cartelera
HOME_TITLE: Final[str] = "Gestión de Cartelera - Cine"

# Nombres de parámetros en la query string (coinciden con los 'name' del formulario HTML)
PARAM_Q: Final[str] = "q"
PARAM_GENERO_ID: Final[str] = "genero_id"
PARAM_DURACION_MAX: Final[str] = "duracion_max"
PARAM_DISPONIBLE: Final[str] = "disponible"
