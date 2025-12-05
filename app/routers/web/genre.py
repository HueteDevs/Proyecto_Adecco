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

# listar géneros
@router.get("", response_class=HTMLResponse)
def list_genres(request: Request, db: Session = Depends(get_db)):
    genres = db.execute(select(Genre)).scalars().all()
    return templates.TemplateResponse(
        "genres/list.html",
        {"request": request, "genres": genres}
    )

# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "genres/form.html",
        {"request": request, "genre": None}
    )



# crear nuevo genero
@router.post("/new", response_class=HTMLResponse)
def create_genre(
    request: Request,
    name_genre: str = Form(...),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {"name_genre": name_genre}

    if not name_genre or not name_genre.strip():
        errors.append("El género es requerido")

    if errors:
        return templates.TemplateResponse(
            "genres/form.html",
            {"request": request, "genre": None, "errors": errors, "form_data": form_data}
        )

    try:
        genre = Genre(name_genre=name_genre.strip())
        db.add(genre)
        db.commit()
        db.refresh(genre)
        return RedirectResponse(url=f"/genres/{genre.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el género: {str(e)}")
        return templates.TemplateResponse(
            "genres/form.html",
            {"request": request, "genre": None, "errors": errors, "form_data": form_data}
        )

# detalle género
@router.get("/{genre_id}", response_class=HTMLResponse)
def genre_detail(request: Request, genre_id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(Genre).where(Genre.id == genre_id)).scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=404, detail="404 - Género no encontrado")
    return templates.TemplateResponse(
        "genres/detail.html",
        {"request": request, "genre": genre}
    )

# mostrar formulario editar
@router.get("/{genre_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, genre_id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(Genre).where(Genre.id == genre_id)).scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=404, detail="404 - Género no encontrado")
    return templates.TemplateResponse(
        "genres/form.html",
        {"request": request, "genre": genre}
    )


# Editar género existente
@router.post("/{genre_id}/edit", response_class=HTMLResponse)
def update_genre(
    request: Request,
    genre_id: int,                     # path param (NO Form)
    name_genre: str = Form(...),       # campo del formulario
    db: Session = Depends(get_db)
):
    genre = db.execute(select(Genre).where(Genre.id == genre_id)).scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=404, detail="404 - Género no encontrado")

    errors = []
    form_data = {"name_genre": name_genre}

    if not name_genre or not name_genre.strip():
        errors.append("El género es requerido")

    if errors:
        return templates.TemplateResponse(
            "genres/form.html",
            {"request": request, "genre": genre, "errors": errors, "form_data": form_data}
        )

    try:
        genre.name_genre = name_genre.strip()
        db.commit()
        db.refresh(genre)
        return RedirectResponse(url=f"/genres/{genre.id}", status_code=303)
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
    try:
        db.delete(genre)
        db.commit()
        return RedirectResponse("/genres", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el género: {str(e)}")

