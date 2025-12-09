from sqlalchemy import Float, ForeignKey,Integer
from database import Base
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped,mapped_column
from enum import Enum



# MODELO BASE DE DATOS (sqlalchemy)

# clase método de pago para que el usuario escoja como quiere pagar mediante un Enum
class MetodoPago(str, Enum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
#modelo de la tabla venta

class Venta(Base):
    __tablename__ = 'ventas'
    
    # Clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requierido, RELACION CON IDs de horario
    horario_id:Mapped[int] = mapped_column(ForeignKey("horarios.id"), nullable=False)
    # requierido, Precio total (haremos el cálculo con el precio base de las salas y la cantidad)
    precio_total: Mapped[float] = mapped_column(Float, nullable=False)
    # requerido.
    cantidad: Mapped[int]= mapped_column(Integer, nullable=False)
    # requerido
    metodo_pago: Mapped[MetodoPago] = mapped_column(SQLEnum(MetodoPago, name="metodo_pago_enum"),
    nullable=False)