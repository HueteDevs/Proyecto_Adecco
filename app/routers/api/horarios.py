from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Horario
from app.schemas import HorarioResponse, HorarioCreate, HorarioUpdate, HorarioPatch



#crear router para endpoints

router = APIRouter(prefix="/api/horarios", tags=["horarios"])


#GET-Obtener todas los horarios
@router.get("", response_model=list[HorarioResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Horario).options(joinedload(Horario.sala))
        ).scalars().unique().all()

#db.execute(): ejecuta la consulta
    #select(Song): crea consulta SELECT * FROM Song
    #.scarlars(): extrae los objetos Song
    #.all(): obtiene los resultados como lista


#GET - Obtener un horario por id

@router.get("/{id}",response_model=HorarioResponse)
def find_by_id(id:int, db: Session = Depends(get_db)):
    horario = db.execute(
        select(Horario).where(Horario.id == id)
        .options(joinedload(Horario.sala))
    ).scalar_one_or_none()
    
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
        
    return horario


#POST - Crear un nuev horario
@router.post("", response_model=HorarioResponse, status_code=status.HTTP_201_CREATED)
def create(horario_dto: HorarioCreate, db: Session = Depends(get_db)):

    #Crear el objeto horario
    horario = Horario(
        pelicula_id=horario_dto.pelicula_id,
        sala_id=horario_dto.sala_id,
        hora=horario_dto.hora,
        disponible=horario_dto.disponible
    )
    
    db.add(horario)
    db.commit()
    db.refresh(horario)
    
    horario_con_sala = db.execute(
        select(Horario)
        .where(Horario.id == horario.id)
        .options(joinedload(Horario.sala))
    ).scalar_one()
    
    return horario_con_sala

#PUT - actualizar completamente un horario
@router.put("/{id}", response_model=HorarioResponse)
def update_full(id: int, horario_dto: HorarioUpdate, db: Session = Depends(get_db)):
    horario = db.execute(
        select(Horario).where(Horario.id == id).options(joinedload(Horario.sala))
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
        
    # guarda el diccionario sacado de song_dto
    update_data = horario_dto.model_dump()
    
   #bucle para asignar el valor del diccionario a cada atributo
        
    for field, value in update_data.items():
        setattr(horario, field, value)
    
    db.commit()
    db.refresh(horario)
    return horario


@router.patch("/{id}", response_model=HorarioResponse)
def update_parcial(id:int, horario_dto: HorarioPatch, db: Session = Depends(get_db)):
    # buscar el horario por id
    
    horario = db.execute(
        select(Horario).where(Horario.id == id)
        .options(joinedload(Horario.sala))
    ).scalar_one_or_none()
    
    # si no existe, error 404
    
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
    
    update_data = horario_dto.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(horario, field, value)
        
    db.commit()
    db.refresh(horario)
    return horario

#Delete - eliminar un horario por id

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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