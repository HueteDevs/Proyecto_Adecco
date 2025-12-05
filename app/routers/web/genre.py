from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.database import get_db
from app.models import Genre

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/genres", tags=["web"])

# listar aristas (http://localhost:8000/artists)
@router.get("", response_class=HTMLResponse)
def list_genres(request: Request, db: Session = Depends(get_db)):
    genres = db.execute(select(Genre)).scalars().all()
    
    return templates.TemplateResponse(
        "genres/list.html",
        {"request": request, "genres": genres}
    )

# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request): #objeto 
    return templates.TemplateResponse(
        "genres/form.html",
        {"request": request, "genres": None}# estoy creando un nuevo genero, si coloco genre, lo estaría modificando.
    )

# crear nuevo genero
@router.post("/new", response_class=HTMLResponse)
def create_genre(
    request: Request,
    name_genre: str = Form(...),# ... obligatorio
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "name_genre": name_genre # ¿como consigo que sea detectado?
    }
    
    name_genre_value = str # aquí como no tengo que convertir nada, porque mi dato es un string... no coloco None, si no str. supongo!
    # if name_genre and name_genre.strip():
    #     try:
    #         name_genre_value = datetime.strptime(name_genre.strip())
    #     except ValueError:
    #         errors.append("El género tiene que tener formato String")
    # Esto no lo necesito.
    
    if not name_genre or not name_genre.strip():
        errors.append("El género es requerido")
    
    if errors:
        return templates.TemplateResponse(
            "genres/form.html",
            {"request": request, "genre": None, "errors": errors, "form_data": form_data}
        )

# Creando el género
    try:
        genre = Genre(
            name_genre=name_genre.strip(),
            
        )
        
        db.add(genre)
        db.commit()
        db.refresh(genre)
        
        # Redirigir a pantalla detalle
        
        return RedirectResponse(url=f"/genres/{genre.id}", status_code=303)
    except Exception as e:
        db.rollback()# deshace los cambios que he hecho
        errors.append(f"Error al crear el género: {str(e)}")
        return templates.TemplateResponse(
            "genre/form.html",
            {"request": request, "genre": None, "errors": errors, "form_data": form_data}
        )

# detalle género 
# (http://localhost:8000/artists/5)

@router.get("/{genre_id}", response_class=HTMLResponse)
def genre_detail(request: Request, genre_id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(genre).where(Genre.id == genre_id)).scalar_one_or_none()
    
    if genre is None:
        raise HTTPException(status_code=404, detail="404 - Género no encontrado")
    
    return templates.TemplateResponse(
        "genre/detail.html",
        {"request": request, "genre": genre}
    )

# mostrar formulario editar
@router.get("/{genre_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, genre_id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(genre).where(Genre.id == genre_id)).scalar_one_or_none()#db.execute= ejecutar consulta en las siguientes carpetas/ scalar devuelve el objeto y si no lo encuentra devuelve None
    
    if genre is None:
        raise HTTPException(status_code=404, detail="404 - Género no encontrado")
    
    return templates.TemplateResponse(
        "genres/form.html",
        {"request": request, "genre": genre}# hay que colocar genre, porque hay un género, pero es modificable.
    )
#REVISAR MAÑANA DESDE AQUI   
# Editar canción existente

@router.post("/{genre_id}/edit", response_class=HTMLResponse)
def update_genre(
    request: Request,
    genre_id: str = Form(...),# esto va? supongo que sí porque relaciona el id
    name_genre: str = Form(...),
    db: Session = Depends(get_db)    
):
    genre = db.execute(select(Genre).where(Genre.id == genre_id)).scalar_one_or_none()
    
    if genre is None:
        raise HTTPException(status_code=404, detail="404 - Género no encontrado")
    
    errors = []
    form_data = {
        "name_genre": name_genre,
    }  

# AQUÍ ME QUEDO PARA REVISAR MAÑANA
 
    if not name_genre or not name_genre.strip():
        errors.append("El género es requerido")
   
    
    if errors:
        return templates.TemplateResponse(
            "genre/form.html",
            {"request": request, "genre": genre, "errors": errors, "form_data": form_data}
        )
    
    try:
        genre.name_genre = name_genre.strip()
        

        db.commit()
        db.refresh(genre)
        
        return RedirectResponse(url=f"/genre/{genre.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar el género: {str(e)}")
        return templates.TemplateResponse(
            "genres/form.html",
            {"request": request, "genre": genre, "errors": errors, "form_data": form_data}
        )

# eliminar género

@router.post("/{genre_id}/delete", response_class=HTMLResponse)
def delete_genre(request: Request, genre_id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(Genre).where(Genre.id == genre_id)).scalar_one_or_none()
    
    if genre is None:
        raise HTTPException(status_code=404, detail="404 - Género no encontrado")
    
    # eliminar género
    try:
        db.delete(genre)
        db.commit()
        
        return RedirectResponse("/genre", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el género: {str(e)}")