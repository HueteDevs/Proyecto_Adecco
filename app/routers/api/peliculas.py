from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Pelicula
from app.schemas import PeliculaResponse, PeliculaCreate, PeliculaPatch, PeliculaUpdate
#crear router para endpoints
router = APIRouter(prefix="/api/peliculas", tags=["peliculas"])



#GET-Obtener todas los peliculas
@router.get("", response_model=list[PeliculaResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Pelicula).options(joinedload(Pelicula.genero))
        ).scalars().unique().all()

#GET - Obtener una pelicula por id

@router.get("/{id}",response_model=PeliculaResponse)
def find_by_id(id:int, db: Session = Depends(get_db)):
    pelicula = db.execute(
        select(Pelicula).where(Pelicula.id == id)
        .options(joinedload(Pelicula.genero))
    ).scalar_one_or_none()
    
    if not pelicula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado una pelicula con la id {id}"
        )
        
    return pelicula

#POST - Crear un nuevo pelicula
@router.post("", response_model=PeliculaResponse, status_code=status.HTTP_201_CREATED)
def create(pelicula_dto: PeliculaCreate, db: Session = Depends(get_db)):

    #Crear el objeto pelicula
    pelicula = pelicula(
        titulo=pelicula_dto.titulo,
        genero_id=pelicula_dto.genero_id,
        duracion=pelicula_dto.duracion,
        disponible=pelicula_dto.disponible
    )
    
    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)
    
    pelicula_con_genero = db.execute(
        select(Pelicula)
        .where(Pelicula.id == Pelicula.id)
        .options(joinedload(Pelicula.genero))
    ).scalar_one()
    
    return pelicula_con_genero

#PUT - actualizar completamente un pelicula
@router.put("/{id}", response_model=PeliculaResponse)
def update_full(id: int, pelicula_dto: PeliculaUpdate, db: Session = Depends(get_db)):
    pelicula = db.execute(
        select(Pelicula).where(Pelicula.id == id).options(joinedload(Pelicula.genero))
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    
    if not pelicula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
        
    # guarda el diccionario sacado de song_dto
    update_data = pelicula_dto.model_dump()
    
   #bucle para asignar el valor del diccionario a cada atributo
        
    for field, value in update_data.items():
        setattr(pelicula, field, value)
    
    db.commit()
    db.refresh(pelicula)
    return pelicula


@router.patch("/{id}", response_model=PeliculaResponse)
def update_parcial(id:int, pelicula_dto: PeliculaPatch, db: Session = Depends(get_db)):
    # buscar el pelicula por id
    
    pelicula = db.execute(
        select(pelicula).where(Pelicula.id == id)
        .options(joinedload(Pelicula.genero))
    ).scalar_one_or_none()
    
    # si no existe, error 404
    
    if not pelicula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un pelicula con la id {id}"
        )
    
    update_data = pelicula_dto.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(pelicula, field, value)
        
    db.commit()
    db.refresh(pelicula)
    return pelicula

#Delete - eliminar un pelicula por id

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session= Depends(get_db)):
    #busca el pelicula por id
    pelicula = db.execute(
        select(Pelicula).where(Pelicula.id == id)
    ).scalar_one_or_none()
    
    #si no existe, error 404
    if not pelicula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un pelicula con la id {id}"
        )
    
    db.delete(pelicula)
    db.commit()
    return None

