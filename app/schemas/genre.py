from pydantic import Basemodel, ConfigDict, field_validator

class GenreResponse(Basemodel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name_genre: str
    
class GenreCreate(Basemodel):
    model_config = ConfigDict(from_attributes=True)
    
    name_genre: str
    
    @field_validator("name_genre")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()
        

class GenreUpdate(Basemodel):
    model_config = ConfigDict(from_attributes=True)
    
    name_genre= str
    
    @field_validator("name_genre")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()
    

class GenrePatch(Basemodel):
    model_config = ConfigDict(from_attributes=True)

    name_genre: str | None = None
    
    @field_validator("name_genre")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None
        
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()
    
    
   
        





