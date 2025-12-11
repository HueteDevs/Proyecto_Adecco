#SCHEMAS (modelos pydantic)
    
#schema para TODAS las respuestas de la API
#lo usamos en GET, POST, PUT, PATCH

from pydantic import BaseModel, ConfigDict, field_validator


class HorarioResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic
    id: int
    pelicula_id: int
    sala_id: int
    hora: str
    disponible: bool


#Schema para crear un horario (POST)
#no incluimos id porque se genera automaticamente

class HorarioCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic
    
    pelicula_id: int
    sala_id:int
    hora: str
    disponible:bool
    
    @field_validator("pelicula_id")
    @classmethod
    def validate_pelicula_id_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("El id de pelicula debe ser un número positivo")
        
        return v
    
    @field_validator("sala_id")
    @classmethod
    def validate_sala_id_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("El id de pelicula debe ser un número positivo")
        
        return v
    
    @field_validator("hora")
    @classmethod
    def validate_hora_not_empty(cls, v: int) -> int:
                if not v or not v.strip():
                    raise ValueError("Este campo no puede estar vacío")
        
                return v.strip()

# schema para Actualizacion completa (PUT)
# todos los campos se tienen que enviar

class HorarioUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic

    pelicula_id: int
    sala_id:int
    hora: str
    disponible:bool

#schema para actualizacion parcial (PATCH)
#solo se envian los campos que quieres actualizar
class HorarioPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic
    
    pelicula_id: int | None = None
    sala_id:int | None = None
    hora: str | None = None
    disponible: bool | None = None