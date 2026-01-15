"""
Esquemas Pydantic para validación de datos
"""
from app.schemas.pelicula import PeliculaResponse, PeliculaCreate, PeliculaPatch, PeliculaUpdate
from app.schemas.horario import HorarioResponse, HorarioCreate, HorarioUpdate, HorarioPatch
from app.schemas.sala import SalaResponse, SalaCreate, SalaUpdate   
from app.schemas.genre import GenreCreate, GenrePatch, GenreResponse, GenreUpdate
from app.schemas.venta import VentaCreate, VentaPatch, VentaResponse, VentaUpdate
__all__ = ["HorarioResponse", "HorarioCreate", "HorarioUpdate", "HorarioPatch",
           "SalaResponse", "SalaCreate", "SalaUpdate",
           "GenreCreate", "GenrePatch", "GenreResponse", "GenreUpdate",
           "VentaCreate", "VentaPatch", "VentaResponse", "VentaUpdate",
           "PeliculaResponse","PeliculaCreate","PeliculaPatch","PeliculaUpdate"
           ]  
