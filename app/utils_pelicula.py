# app/utils_pelicula.py
"""
Utilidades específicas para la entidad Película.

Responsabilidades:
- Normalizar parámetros de filtro recibidos por query string.
- Invocar al servicio de Películas para obtener el listado filtrado.
- Cargar la lista de Géneros para el combo.
- Construir el diccionario 'filtros_activos' para la plantilla.
"""

from typing import Optional, Tuple, Dict, Any, List
from sqlalchemy.orm import Session

from app.services import pelicula_service, genero_service
from app.config_pelicula import (
    HOME_TITLE,
    PARAM_Q,
    PARAM_GENERO_ID,
    PARAM_DURACION_MAX,
    PARAM_DISPONIBLE,
)


def normalizar_filtros(
    q: Optional[str],
    genero_id: Optional[str],
    duracion_max: Optional[str],
    disponible: Optional[str],
) -> Tuple[Optional[str], Optional[int], Optional[int], bool]:
    """
    Convierte los parámetros de la query string (str) a tipos adecuados.

    - genero_id: str -> int | None
    - duracion_max: str -> int | None
    - disponible: str ("True" / None) -> bool
    """
    clean_genero_id: Optional[int] = (
        int(genero_id) if genero_id and genero_id.isdigit() else None
    )
    clean_duracion_max: Optional[int] = (
        int(duracion_max) if duracion_max and duracion_max.isdigit() else None
    )

    # El checkbox de 'disponible' solo envía valor cuando está marcado
    filtro_disponible: bool = disponible == "True"

    return q, clean_genero_id, clean_duracion_max, filtro_disponible


def cargar_datos_homepage(
    db: Session,
    q: Optional[str],
    genero_id: Optional[str],
    duracion_max: Optional[str],
    disponible: Optional[str],
) -> Tuple[List[Any], List[Any], Dict[str, Any]]:
    """
    Carga todos los datos necesarios para la homepage de la cartelera:

    - Lista de películas filtradas.
    - Lista de géneros para el combo.
    - Diccionario de filtros activos para repintar el formulario.
    """
    (
        q_normalizada,
        clean_genero_id,
        clean_duracion_max,
        filtro_disponible_bool,
    ) = normalizar_filtros(q, genero_id, duracion_max, disponible)

    # 1. Películas filtradas (buscador + filtros)
    peliculas = pelicula_service.get_peliculas_filtradas(
        db=db,
        query=q_normalizada,
        genero_id=clean_genero_id,
        duracion_max=clean_duracion_max,
        disponible=filtro_disponible_bool,
    )

    # 2. Lista de géneros para el selector
    generos_disponibles = genero_service.get_all_generos(db)

    # 3. Construir filtros_activos exactamente con las claves usadas en index.html
    filtros_activos: Dict[str, Any] = {
        PARAM_Q: q_normalizada,
        PARAM_GENERO_ID: clean_genero_id,
        PARAM_DURACION_MAX: clean_duracion_max,
        PARAM_DISPONIBLE: filtro_disponible_bool,
    }

    return peliculas, generos_disponibles, filtros_activos


def get_home_title() -> str:
    """
    Devuelve el título de la homepage de la cartelera.
    Se encapsula por si en el futuro quieres hacerlo dinámico.
    """
    return HOME_TITLE
