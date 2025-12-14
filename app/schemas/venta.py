from app.models.venta import MetodoPago 
from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas import HorarioResponse

# Schema para TODAS las respuestas de la API
 # Usos:
 # GET, POST, PUT, PATCH
class VentaResponse(BaseModel):
    
# ConfigDict hace que Pydantic pueda crear los modelos a partir de instancias 
# de SQLAlchemy (valida objetos ORM)
    model_config = ConfigDict(from_attributes=True)
     
    id: int
    horario_id: int
    horario: HorarioResponse
    precio_total: float
    cantidad: int
    metodo_pago: MetodoPago
    
# Equema para CREAR una venta
# No se incluye id porque se genera automáticamente
class VentaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int 
    cantidad: int
    metodo_pago: MetodoPago 
    
    @field_validator("horario_id", "cantidad")
    @classmethod
    def validate_not_empty(cls, v: int) -> int:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()
    
    @field_validator("precio_total")
    @classmethod
    def validate_not_empty(cls, v: float) -> float:
        if not v or not v.strip():
            raise ValueError("El campo precio no puede estar vacío")
        return v.strip()


# Esquema para actualización completa (PUT)
# Todos los campos son obligarorios
class VentaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int 
    cantidad: int
    metodo_pago: MetodoPago
    
    @field_validator("horario_id", "cantidad")
    @classmethod
    def validate_not_empty(cls, v: int) -> int:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()
    

    
    @field_validator("precio_total")
    @classmethod
    def validate_not_empty(cls, v: float) -> float:
        if not v or not v.strip():
            raise ValueError("El campo precio no puede estar vacío")
        return v.strip()

# Esquema actualualización parcial (PATCH)
# Todos los campos son opcionales.
class VentaPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int | None = None#RELACION
    cantidad: int | None = None
    metodo_pago: MetodoPago | None = None
    
    @field_validator("horario_id", "cantidad")
    @classmethod
    def validate_not_empty(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()
    
    @field_validator("precio_total")
    @classmethod
    def validate_not_empty(cls, v: float | None) -> float | None:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()