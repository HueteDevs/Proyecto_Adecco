# app/schemas/pelicula.py
# Define los modelos Pydantic (BaseModel) para validación en la API

from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Any
from app.schemas.genre import GenreResponse

# Campos comunes que se comparten al crear y leer.
class PeliculaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Traduce los atributos de SQLAlchemy para Pydantic
    id: int
    titulo: str
    duracion: int
    disponible: bool
    genero_id: int
    genero: GenreResponse 

# --- Esquema de Creación (POST /peliculas) ---
# Hereda de Base y añade campos necesarios solo al crear.
class PeliculaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Traduce los atributos de SQLAlchemy para Pydantic
    
    titulo: str
    duracion: int
    disponible: bool
    genero_id: int
    genero: GenreResponse
    
    
    @field_validator("titulo")
    @classmethod
    def validate_titulo_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El titulo no puede estar vacío")
        return v.strip()
    
    @field_validator("duracion")
    @classmethod
    def validate_duracion_positive(cls, v: int) -> int:
        if v is None or v < 1:
            raise ValueError("La duracion debe de ser positiva")
        return v
    
    @field_validator("genero_id")
    @classmethod
    def validate_genero_id_positive(cls, v: int) -> int:
        if v is None or v < 1:
            raise ValueError("El id de genero debe ser un número positivo")
        return v
    
    

# --- Esquema de Actualización (PUT /peliculas/{id}) ---
class PeliculaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Traduce los atributos de SQLAlchemy para Pydantic
    
    titulo: str
    duracion: int
    disponible: bool
    genero_id: int
    genero: GenreResponse
    
    
    
    @field_validator("titulo")
    @classmethod
    def validate_titulo_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El titulo no puede estar vacío")
        return v.strip()
    
    @field_validator("duracion")
    @classmethod
    def validate_duracion_positive(cls, v: int) -> int:
        if v is None or v < 1:
            raise ValueError("La duracion debe de ser positiva")
        return v
    
    @field_validator("genero_id")
    @classmethod
    def validate_genero_id_positive(cls, v: int) -> int:
        if v is None or v < 1:
            raise ValueError("El id de genero debe ser un número positivo")
        return v
    

class PeliculaPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    titulo: str | None = None
    duracion: int | None = None
    disponible: bool | None = None
    genero_id: int | None = None
    

    
    @field_validator("titulo")
    @classmethod
    def validate_titulo_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None
        
        if not v or not v.strip():
            raise ValueError("El titulo no puede estar vacio")
        
        return v.strip()
    
    @field_validator("duracion")
    @classmethod
    def validate_duracion_id_positive(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        if v < 1:
            raise ValueError("El id de la pelicula debe ser un número positivo")
        
        return v
    
    
    @field_validator("genero_id")
    @classmethod
    def validate_duracion_id_positive(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        if v < 1:
            raise ValueError("El id del genero debe ser un número positivo")
        
        return v
