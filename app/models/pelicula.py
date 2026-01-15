
# app/models/pelicula.py
# Define la tabla 'peliculas' en la BBDD

from sqlalchemy import String, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base # Importamos la Base declarativa
from app.models.genre import Genre


class Pelicula(Base):
    __tablename__ = "peliculas"

    # --- Columnas Requeridas ---
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # --- Relación ManyToOne con Genero ---
    # Esto cumple con "genero_id: int"
    genero_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), nullable=False)
    genero: Mapped["Genre"] = relationship("Genre")
    duracion: Mapped[int] = mapped_column(Integer, nullable=False) # int, no float
    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    
   