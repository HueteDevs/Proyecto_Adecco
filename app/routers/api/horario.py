from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.horario import Horario
from app.schemas.horario import HorarioResponse, HorarioCreate, HorarioUpdate, HorarioPatch



#crear router para endpoints

router = APIRouter(prefix="/api/horarios", tags=["horarios"])
#GET-Obtener todas los horarios
@app.get("/api/horarios", response_model=list[HorarioResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Horario)).scalars().all()

#db.execute(): ejecuta la consulta
    #select(Song): crea consulta SELECT * FROM Song
    #.scarlars(): extrae los objetos Song
    #.all(): obtiene los resultados como lista


#GET - Obtener un horario por id

@app.get("/api/horarios/{id}",response_model=HorarioResponse)
def find_by_id(id:int, db: Session = Depends(get_db)):
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
        
    return horario


#POST - Crear un nuev horario
@app.post("/api/horarios", response_model=HorarioResponse, status_code=status.HTTP_201_CREATED)
def create(horario_dto: HorarioCreate, db: Session = Depends(get_db)):
    #Hacemos las validaciones necesarias
    if  horario_dto.pelicula_id is not None and horario_dto.pelicula_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pelicula_id no puede ser negativa"
        )
        
    if horario_dto.sala_id is not None and horario_dto.sala_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sala_id no puede ser negativa"
        )
    
    if not horario_dto.hora.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La hora no puede estar vacia"
        )

    #Crear el objeto horario
    horario = Horario(
        pelicula_id=horario_dto.pelicula_id,
        sala_id=horario_dto.sala_id,
        hora=horario_dto.hora.strip(),
        disponible=horario_dto.disponible
    )
    
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario

#PUT - actualizar completamente un horario
@app.put("/api/horarios/{id}", response_model=HorarioResponse)
def update_full(id: int, horario_dto: HorarioUpdate, db: Session = Depends(get_db)):
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    if  horario_dto.pelicula_id is not None and horario_dto.pelicula_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pelicula_id no puede ser negativa"
        )
        
    if horario_dto.sala_id is not None and horario_dto.sala_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sala_id no puede ser negativa"
        )
    
    if not horario_dto.hora.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La hora no puede estar vacia"
        )
    
    #Actualizar todos los campos
    horario.pelicula_id = horario_dto.pelicula_id
    horario.sala_id = horario_dto.sala_id
    horario.hora = horario_dto.hora.strip()
    horario.disponible = horario_dto.disponible
    
    db.commit()
    db.refresh(horario)
    return horario


@app.patch("/api/horarios/{id}", response_model=HorarioResponse)
def update_parcial(id:int, horario_dto: HorarioPatch, db: Session = Depends(get_db)):
    # buscar el horario por id
    
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    # si no existe, error 404
    
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
    
    #actualizar solo los campos enviados
    
    if horario_dto.pelicula_id is not None:
        if  horario_dto.pelicula_id < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tiene que haber una pelicula y con un numero valido"
            )
    
        horario.pelicula_id = horario_dto.pelicula_id
    
    if horario_dto.sala_id is not None:
        if horario_dto.sala_id < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tiene que haber una sala y con un numero valido"
            )
    
        horario.sala_id = horario_dto.sala_id
    
    if horario_dto.hora is not None:
        if not horario_dto.hora.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora no puede estar vacia"
            )
        horario.hora = horario_dto.hora.strip()
    
    if horario_dto.disponible is not None:
        horario.disponible = horario_dto.disponible
    
    db.commit()
    
    db.refresh(horario)
    return horario

#Delete - eliminar un horario por id

@app.delete("/api/horarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session= Depends(get_db)):
    #busca el horario por id
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    #si no existe, error 404
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
    
    db.delete(horario)
    db.commit()
    return None