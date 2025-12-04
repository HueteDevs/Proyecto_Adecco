from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Genre
from app.schemas import GenreResponse, GenreCreate, GenreUpdate, GenrePatch

router = APIRouter(prefix="/api/genres",tags=["genres"])

@router.get("", response_model=list[GenreResponse])
def find_all(db:Session = Depends(get_db)):
    return db.execute(select(Genre)).scalars().all()

@router.get("/{id}", response_model=GenreResponse)
def find_by_id(id:int, db:Session = Depends(get_db)):
    # aquí esta una de mis dudas... es genre o name_genre
    genre = db.execute(select(Genre).where(Genre.id ==id)).scalar_one_or_none()
    
    if not genre:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado el género con el id {id}")
    return genre
# POST
@router.post("", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
def create(genre_dto: GenreCreate, db:Session = Depends(get_db)):
    
    genre = Genre(
        name_genre= genre_dto.name_genre
    )

    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre
#put
@router.put("/{id}", response_model=GenreResponse)
def update_full(id: int, genre_dto:GenreUpdate, db: Session = Depends(get_db)):
    
    genre = db.execute(
        select(Genre).where(Genre.id == id)
    ).scalar_one_or_none()

    if not genre:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se ha encontrado el género id {id}"
    )
    
    update_data = genre_dto.model_dump()
    
    for field, value in update_data.items():
        setattr(name_genre, field, value)
        
    db.commit()
    db.refresh(genre)
    return Genre

#patch
@router.patch("/{id}", response_model= GenreResponse)
def update_partial(id: int, genre_dto: GenrePatch, db: Session = Depends(get_db)):
    
    genre = db.execute(
        select(Genre).where(Genre.id ==id)
    ).scalar_one_or_none()
    
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el género con id {id}"
        )
        
    update_data = genre_dto.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(genre, field, value)
    
    db.commit()
    db.refresh(genre) 
    return genre

# DELETE
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    
    genre = db.execute(
        select(Genre).where(Genre.id == id)
    ).scalar_one_or_none()
    
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el género con id {id}"  
        )

    db.delete(genre) 
    db.commit() 
    return None
        
    
    


        

