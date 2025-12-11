#SCHEMAS (modelos pydantic)

from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas.sala import SalaResponse  # import directo desde el submódulo

# schema para TODAS las respuestas de la API
# lo usamos en GET, POST, PUT, PATCH
class HorarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Traduce los atributos de SQLAlchemy para Pydantic
    id: int
    pelicula_id: int
    sala_id: int
    sala: SalaResponse
    hora: str
    disponible: bool

# Schema para crear un horario (POST)
# no incluimos id porque se genera automaticamente
class HorarioCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pelicula_id: int
    sala_id: int
    hora: str
    disponible: bool

    @field_validator("pelicula_id")
    @classmethod
    def validate_pelicula_id_positive(cls, v: int) -> int:
        if v is None or v < 1:
            raise ValueError("El id de película debe ser un número positivo")
        return v

    @field_validator("sala_id")
    @classmethod
    def validate_sala_id_positive(cls, v: int) -> int:
        if v is None or v < 1:
            raise ValueError("El id de sala debe ser un número positivo")
        return v

    @field_validator("hora")
    @classmethod
    def validate_hora_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La hora no puede estar vacía")
        return v.strip()

# schema para Actualizacion completa (PUT)
# todos los campos se tienen que enviar
class HorarioUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pelicula_id: int
    sala_id: int
    hora: str
    disponible: bool

# schema para actualizacion parcial (PATCH)
# solo se envian los campos que quieres actualizar
class HorarioPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pelicula_id: int | None = None
    sala_id: int | None = None
    hora: str | None = None
    disponible: bool | None = None
    
    