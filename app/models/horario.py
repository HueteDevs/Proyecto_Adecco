from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
#modelo de la tabla horario( se crea un solo modelo)
class Horario(Base):
    __tablename__ = "horarios" #nombre de la tabla en bd
    #clave primaria
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    #relacion ManyToOne con Peliculas
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("peliculas.id"),nullable=False)
    #relacion ManyToOne con Salas
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), nullable=False)
    hora: Mapped[str] = mapped_column(String, nullable=False)
    disponible:Mapped[bool] = mapped_column(Boolean, nullable=False)
    