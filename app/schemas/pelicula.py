# app/schemas/pelicula.py
# Define los modelos Pydantic (BaseModel) para validación en la API

from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Any


# Campos comunes que se comparten al crear y leer.
class PeliculaBase(BaseModel):
    titulo: str
    duracion: int
    disponible: bool
    
    # Campos opcionales
    director: Optional[str] = None
    descripcion: Optional[str] = None
    trailer: Optional[str] = None
    productora: Optional[str] = None
    idioma: Optional[str] = None
    vose: Optional[bool] = None
    actores: Optional[List[str]] = None

# --- Esquema de Creación (POST /peliculas) ---
# Hereda de Base y añade campos necesarios solo al crear.
class PeliculaCreate(PeliculaBase):
    genero_id: int # Al crear, solo pasamos el ID del género

# --- Esquema de Actualización (PUT /peliculas/{id}) ---
class PeliculaUpdate(BaseModel):
    titulo: Optional[str] = None
    duracion: Optional[int] = None
    disponible: Optional[bool] = None
    genero_id: Optional[int] = None
    director: Optional[str] = None
    descripcion: Optional[str] = None
    trailer: Optional[str] = None
    productora: Optional[str] = None
    idioma: Optional[str] = None
    vose: Optional[bool] = None
    actores: Optional[List[str]] = None

# --- Esquema de Lectura (GET /peliculas) ---
# Hereda de Base y añade campos que se devuelven desde la BBDD.
class PeliculaRead(PeliculaBase):
    id: int
    genero_id: int
    
    # Configuración para que Pydantic pueda leer desde el modelo ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

# Schema para lectura con género anidado)
# Si quisieramos devolver el objeto género completo en lugar del ID:
#
# from .genero import GeneroRead # (Suponiendo que Kary crea este schema)
#
# class PeliculaReadWithGenero(PeliculaRead):
#     genero: GeneroRead

# Importar GeneroRead para el anidamiento
from .genero import GeneroRead
 
class PeliculaReadWithGenero(PeliculaRead):
    # Sobreescribe el campo de la base para incluir el objeto ORM cargado
    genero: GeneroRead
    
# --- Esquema de Importación---
# Se utiliza para validar las filas de datos recibidas en CSV/JSON antes de la inserción.
class PeliculaImport(BaseModel):
    # Campos requeridos para la inserción
    titulo: str
    duracion: int
    disponible: bool = True # Asumimos que si no se indica, está disponible
    
    # Relación por nombre de género (temporal para importación)
    genero_nombre: str # Usaremos el nombre para buscar el ID

    # Campos que deben coincidir con las columnas del CSV/JSON de exportación
    director: Optional[str] = None
    descripcion: Optional[str] = None
    trailer: Optional[str] = None
    productora: Optional[str] = None
    idioma: Optional[str] = None
    vose: bool = False
    
    # Campo para manejar los actores (puede venir como cadena o como lista)
    actores: Optional[Any] = None

    # Validador para normalizar el campo 'actores' a una lista de strings
    @field_validator('actores', mode='before')
    @classmethod
    def split_actors_string(cls, v: Any) -> Optional[List[str]]:
        """Convierte una cadena de actores separada por comas en una lista."""
        if isinstance(v, str):
            # Limpiar y dividir por coma. Filtrar strings vacías.
            actors = [a.strip() for a in v.split(',') if a.strip()]
            return actors if actors else None
        # Si ya es una lista, o None, lo dejamos pasar.
        if isinstance(v, list) or v is None:
            return v
        # Intentar forzar la conversión a string si es otro tipo, luego limpiar
        if v:
            return cls.split_actors_string(str(v))
        return None
        
    @field_validator('duracion', mode='before')
    @classmethod
    def validate_duration(cls, v: Any) -> int:
        """Asegura que la duración sea un número entero válido."""
        if isinstance(v, str) and v.isdigit():
            return int(v)
        if isinstance(v, int):
            return v
        raise ValueError("La duración debe ser un número entero.")

    @field_validator('disponible', 'vose', mode='before')
    @classmethod
    def validate_boolean_field(cls, v: Any) -> bool:
        """Normaliza los valores de verdad (como 'Sí' o 'No', 'True' o 'False') a booleano."""
        if isinstance(v, str):
            # Convertir 'Sí'/'sÍ', 'True'/'TRUE' a True
            return v.strip().lower() in ['si', 'sí', 'true', '1']
        return bool(v)