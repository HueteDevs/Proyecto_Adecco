"""
Esquemas Pydantic para validación de datos
"""

from .horario import HorarioResponse, HorarioCreate, HorarioUpdate, HorarioPatch
from .sala import SalaResponse, SalaCreate, SalaUpdate   
from .genre import GenreCreate, GenrePatch, GenreResponse, GenreUpdate

__all__ = ["HorarioResponse", "HorarioCreate", "HorarioUpdate", "HorarioPatch","SalaResponse", "SalaCreate", "SalaUpdate","GenreCreate", "GenrePatch", "GenreResponse", "GenreUpdate"]  
