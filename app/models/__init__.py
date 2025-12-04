"""
Modelos de base de datos (SQLAlchemy)
"""

# Todos los modelos han sido incluídos (Kary)

from app.models.horario import Horario
from app.models.genre import Genre
from app.models.pelicula import Pelicula
from app.models.sala import Sala
from app.models.venta import Venta

__all__ = ["Pelicula", "Sala", "Horario", "Genre", "Venta"]