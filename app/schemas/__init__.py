"""
Esquemas Pydantic para validación de datos
"""

from app.schemas.horario import HorarioResponse, HorarioCreate, HorarioUpdate, HorarioPatch
from app.schemas.sala import SalaResponse, SalaCreate, SalaUpdate   

__all__ = ["HorarioResponse", "HorarioCreate", "HorarioUpdate", "HorarioPatch","SalaResponse", "SalaCreate", "SalaUpdate"]  
