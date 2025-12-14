from app.models.venta import MetodoPago
from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas import HorarioResponse

class VentaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    horario_id: int
    horario: HorarioResponse
    precio_total: float
    cantidad: int
    metodo_pago: MetodoPago

class VentaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    horario_id: int
    cantidad: int
    metodo_pago: MetodoPago = MetodoPago.TARJETA

    @field_validator("horario_id", "cantidad")
    @classmethod
    def validate_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("El id de horario y la cantidad deben ser positivas")
        return v

class VentaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    horario_id: int
    cantidad: int
    metodo_pago: MetodoPago
    precio_total: float

    @field_validator("horario_id", "cantidad")
    @classmethod
    def validate_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("El id de horario y la cantidad deben ser positivas")
        return v

    @field_validator("precio_total")
    @classmethod
    def validate_precio(cls, v: float) -> float:
        if v < 0:
            raise ValueError("El precio total debe ser un número positivo")
        return v

class VentaPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    horario_id: int | None = None
    cantidad: int | None = None
    metodo_pago: MetodoPago | None = None
    precio_total: float | None = None

    @field_validator("horario_id", "cantidad")
    @classmethod
    def validate_positive_optional(cls, v: int | None) -> int | None:
        if v is None:
            return None
        if v < 1:
            raise ValueError("El id de horario y la cantidad deben ser positivas")
        return v

    @field_validator("precio_total")
    @classmethod
    def validate_precio_optional(cls, v: float | None) -> float | None:
        if v is None:
            return None
        if v < 0:
            raise ValueError("El precio debe ser un número positivo")
        return v