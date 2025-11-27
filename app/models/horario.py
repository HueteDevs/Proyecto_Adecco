from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
#modelo de la tabla horario( se crea un solo modelo)
class Horario(Base):
    __tablename__ = "horarios" #nombre de la tabla en bd
    #clave primaria
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pelicula_id: Mapped[int] = mapped_column(Integer,nullable=False)
    sala_id: Mapped[int] = mapped_column(Integer,nullable=False)
    hora: Mapped[str] = mapped_column(String, nullable=False)
    disponible:Mapped[bool] = mapped_column(Boolean, nullable=False)