from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import SalaORM
from app.schemas import SalaResponse, SalaCreate, SalaUpdate

# Crear router para endpoints
router = APIRouter(prefix="/api/salas", tags=["salas"]) 

@router.get("/salas", response_model=list[SalaResponse])
def obtener_salas(db: Session = Depends(get_db)):
    salas = db.execute(select(SalaORM)).scalars().all()
    return salas

@router.get("/salas/{sala_id}", response_model=SalaResponse)
def obtener_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.execute(
        select(SalaORM).where(SalaORM.id == sala_id)
        ).scalar_one_or_none()
    if sala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="Sala no encontrada")
    return sala 

@router.post("/salas", response_model=SalaResponse, status_code=status.HTTP_201_CREATED)
def crear_sala(sala: SalaCreate, db: Session = Depends(get_db)):
    #if existe ya la sala es un error
    if db.execute(
        select(SalaORM).where(SalaORM.nombre == sala.nombre)
        ).scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe una sala con ese nombre")
    
    nueva_sala = SalaORM()
    update_data = sala.model_dump()
    
    for field, value in update_data.items():
        setattr(nueva_sala, field, value)
    
    db.add(nueva_sala)
    db.commit()
    db.refresh(nueva_sala)
    return nueva_sala

@router.patch("/salas/{sala_id}", response_model=SalaResponse)
def actualizar_sala(sala_id: int, sala: SalaUpdate, db: Session =  Depends(get_db)):
    sala_existente = db.execute(
        select(SalaORM).where(SalaORM.id == sala_id)
        ).scalar_one_or_none()
    if sala_existente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada")
    
    update_data = sala.model_dump()
    
    for field, value in update_data.items():
        setattr(sala_existente, field, value)
    
    db.commit()
    db.refresh(sala_existente)
    return sala_existente

@router.delete("/salas/{sala_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sala(sala_id: int, db: Session = Depends(get_db)):
    sala_existente = db.execute(
        select(SalaORM).where(SalaORM.id == sala_id)
        ).scalar_one_or_none()
    if sala_existente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada")
    db.delete(sala_existente)
    db.commit()
    return None