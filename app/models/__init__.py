"""
Modelos de base de datos (SQLAlchemy)
"""

# Todos los modelos han sido incluídos (Kary)

from app.models.horario import Horario
from app.models.genre import Genre
#from app.models.pelicula import PeliculaORM
"from app.models.sala import Sala"
from app.models.venta import Venta
from app.models.venta import MetodoPago
# Modelos de base de datos (SQLAlchemy)
from app.models.sala import SalaORM

__all__ = [Horario, SalaORM, Genre, Venta, MetodoPago] 

