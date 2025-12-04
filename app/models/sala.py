
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, Float, Enum
from app.database import Base

# Modelo Sala de la base de datos
class SalaORM(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(Enum("2D", "3D", "IMAX", "2d", "3d", "imax", "Imax", name="tipo_enum"), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    