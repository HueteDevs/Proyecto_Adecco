from models import MetodoPago 
from pydantic import BaseModel, ConfigDict

# Schema para TODAS las respuestas de la API
 # Usos:
 # GET, POST, PUT, PATCH
class VentaResponse(BaseModel):
    
# ConfigDict hace que Pydantic pueda crear los modelos a partir de instancias 
# de SQLAlchemy (valida objetos ORM)
    model_config = ConfigDict(from_attributes=True)
     
    id: int
    horario_id: int
    precio_total: float
    cantidad: int
    metodo_pago: MetodoPago
    
# Equema para CREAR una venta
# No se incluye id porque se genera automáticamente
class VentaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int #RELACION (preguntar a María)
    cantidad: int
    metodo_pago: MetodoPago

# Esquema para actualización completa (PUT)
# Todos los campos son obligarorios
class VentaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int #RELACION
    cantidad: int
    metodo_pago: MetodoPago

# Esquema actualualización parcial (PATCH)
# Todos los campos son opcionales.
class VentaPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int | None = None#RELACION
    cantidad: int | None = None
    metodo_pago: MetodoPago | None = None