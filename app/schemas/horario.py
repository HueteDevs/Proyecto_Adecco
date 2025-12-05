#SCHEMAS (modelos pydantic)
    
#schema para TODAS las respuestas de la API
#lo usamos en GET, POST, PUT, PATCH

from pydantic import BaseModel, ConfigDict


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