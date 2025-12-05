
# app/models/pelicula.py
# Define la tabla 'peliculas' en la BBDD

from sqlalchemy import String, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base # Importamos la Base declarativa

# Importación de tipo para la relación bidireccional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .genero import GeneroORM

class PeliculaORM(Base):
    __tablename__ = "peliculas"

    # --- Columnas Requeridas ---
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # --- Relación ManyToOne con Genero ---
    # Esto cumple con "genero_id: int"
    genero_id: Mapped[int] = mapped_column(ForeignKey("generos.id"), nullable=False)
    
    duracion: Mapped[int] = mapped_column(Integer, nullable=False) # int, no float
    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # --- Columnas (nullable=True) ---
    director: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    trailer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    productora: Mapped[str | None] = mapped_column(String(100), nullable=True)
    idioma: Mapped[str | None] = mapped_column(String(50), nullable=True)
    vose: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    
    # --- Manejo de "actores: lista" ---
    # La mejor forma de almacenar una lista simple en SQL sin una tabla M2M
    # es usar un tipo JSON. SQLite lo soporta nativamente.
    actores: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # --- Relación Bidireccional (Lado "Many") ---
    # Esto permite que desde un objeto Pelicula, podamos acceder 
    # a su género con `pelicula.genero`
    genero: Mapped["GeneroORM"] = relationship(back_populates="peliculas")
    
    # (Aquí irían otras relaciones)
    
    
    
    def __repr__(self):
        return f"<Pelicula(id={self.id}, titulo='{self.titulo}')>"
