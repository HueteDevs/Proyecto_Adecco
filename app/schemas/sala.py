""" 
Esquemas Pydantic para estructura y validación de datos de Sala
"""
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator

# schema para TODAS las respuestas de la API
# lo usamos en GET, POST, PUT, PATCH
# Modelo Pydantic para la Sala (schema)
class SalaResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    nombre: str
    capacidad: int
    tipo: str
    precio: float
        
class SalaCreate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    nombre: str
    capacidad: int
    tipo: str
    precio: float
    
    @field_validator("nombre", "tipo")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        # verificar si el valor está vacío o sólo tiene espacios
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")

        # retorna el valor sin espacios al principio y al final (normalizar)
        return v.strip()
    
    @field_validator("capacidad")
    @classmethod
    def validate_capacidad_positive(cls, v: int) -> int:
        # valida sólo si se da un valor (no es None)
        if  v <= 0:
            raise ValueError("La capacidad debe ser un número positivo")
        return v
    
    @field_validator("precio")
    @classmethod
    def validate_precio_positive(cls, v: float) -> float:
        # valida sólo si se da un valor (no es None)
        if v < 0:
            raise ValueError(" El precio debe ser un número positivo o cero")
        return v
    
    @field_validator("tipo")
    @classmethod    
    def validate_tipo(cls, v: str) -> str:
        # valia el tipo de sala
        if v not in ["2D", "3D", "IMAX", "2d", "3d", "imax", "Imax"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de sala inválido")
        return v.upper()

class SalaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    nombre: str | None = None
    capacidad: int | None = None
    tipo: str | None = None
    precio: float | None = None 
    
    @field_validator("nombre", "tipo")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        # si no se proporcionó valor (None), no validamos
        if v is None:
            return None
        
        # verificar si el valor está vacío o sólo tiene espacios
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")

        # retorna el valor sin espacios al principio y al final (normalizar)
        return v.strip()
    
    @field_validator("capacidad")
    @classmethod
    def validate_capacidad_positive(cls, v: int) -> int:
        # si no se proporcionó valor (None), no validamos
        if v is None:
            return None
        
        # valida sólo si se da un valor (no es None)
        if  v <= 0:
            raise ValueError("La capacidad debe ser un número positivo")
        return v
    
    @field_validator("precio")
    @classmethod
    def validate_precio_positive(cls, v: float) -> float:
        # si no se proporcionó valor (None), no validamos
        if v is None:
            return None
        
        # valida sólo si se da un valor (no es None)
        if v < 0:
            raise ValueError(" El precio debe ser un número positivo o cero")
        return v
    
    @field_validator("tipo")
    @classmethod    
    def validate_tipo(cls, v: str) -> str:
        # si no se proporcionó valor (None), no validamos
        if v is None:
            return None
        
        # valia el tipo de sala
        if v not in ["2D", "3D", "IMAX", "2d", "3d", "imax", "Imax"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de sala inválido")
        return v.upper()