from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.models import Pelicula, Genre

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/peliculas", tags=["web"])


# Listar películas
@router.get("", response_class=HTMLResponse)
def list_peliculas(request: Request, db: Session = Depends(get_db)):
    peliculas = db.execute(select(Pelicula).options(joinedload(Pelicula.genero))).scalars().all()

    return templates.TemplateResponse(
        "peliculas/list.html",
        {"request": request, "peliculas": peliculas}
    )


# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request, db: Session = Depends(get_db)):
    generos = db.execute(select(Genre)).scalars().all() 
    
    return templates.TemplateResponse(
        "peliculas/form.html",
        {"request": request, "pelicula": None, "generos": generos}
    )


# crear nueva película
@router.post("/new", response_class=HTMLResponse)
def create_pelicula(
    request: Request,
    titulo: str = Form(...),
    genero_id: str = Form(...),
    duracion: str = Form(...),
    disponible: str = Form(""),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "titulo": titulo,
        "genero_id": genero_id,
        "duracion": duracion,
        "disponible": disponible,
    }
    
    generos = db.execute(select(Genre)).scalars().all()

    # validaciones
    if not titulo or not titulo.strip():
        errors.append("El título es obligatorio.")

    genero_id_value = None
    
    if genero_id and genero_id.strip():
        try:
            genero_id_value = int(genero_id.strip())
            
            if genero_id_value < 1:
                errors.append("El id del género debe ser un número positivo.")
            genero = db.execute(select(Genre).where(Genre.id == genero_id_value)).scalar_one_or_none()
            if genero is None:
                errors.append("El género especificado no existe.")
        except ValueError:
            errors.append("El id del género tiene que ser un entero válido.")
    else:
        errors.append("El id del género es requerido")

    duracion_value = None
    if duracion and duracion.strip():
        try:
            duracion_value = int(duracion.strip())
            
            if duracion_value < 1:
                errors.append("La duración debe ser un número positivo.")
        except ValueError:
            errors.append("La duración tiene que ser un entero válido.")
    else:
        errors.append("La duración es obligatoria.")

    # procesar disponible: '' -> False, 'on' o 'true' -> True
    disponible_val = disponible in ("on", "true")

    if errors:
        return templates.TemplateResponse(
            "peliculas/form.html",
            {"request": request, "pelicula": None, "errors": errors, "form_data": form_data, "generos": generos}
        )

    try:
        pelicula = Pelicula(
            titulo=titulo.strip(),
            genero_id=genero_id_value,
            duracion=duracion_value,
            disponible=disponible_val
        )
        db.add(pelicula)
        db.commit()
        db.refresh(pelicula)

        return RedirectResponse(url=f"/peliculas/{pelicula.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear la película: {str(e)}")
        return templates.TemplateResponse(
            "peliculas/form.html",
            {"request": request, "pelicula": None, "errors": errors, "form_data": form_data, "generos": generos}
        )


# detalle de película
@router.get("/{pelicula_id}", response_class=HTMLResponse)
def pelicula_detail(request: Request, pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.execute(select(Pelicula).where(Pelicula.id == pelicula_id)
                .options(joinedload(Pelicula.genero))).scalar_one_or_none()
    
    if pelicula is None:
        raise HTTPException(status_code=404, detail="404 - Película no encontrada")
    return templates.TemplateResponse(
        "peliculas/detail.html",
        {"request": request, "pelicula": pelicula}
        )


# mostrar formulario editar
@router.get("/{pelicula_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.execute(select(Pelicula).where(Pelicula.id == pelicula_id)
                         .options(joinedload(Pelicula.genero))).scalar_one_or_none()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="404 - Película no encontrada")
    generos = db.execute(select(Genre)).scalars().all()
    return templates.TemplateResponse("peliculas/form.html", {"request": request, "pelicula": pelicula, "generos": generos})


# editar película existente
@router.post("/{pelicula_id}/edit", response_class=HTMLResponse)
def update_pelicula(
    request: Request,
    pelicula_id: int,
    titulo: str = Form(...),
    genero_id: str = Form(...),
    duracion: str = Form(...),
    disponible: str = Form(""),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "titulo": titulo,
        "genero_id": genero_id,
        "duracion": duracion,
        "disponible": disponible,
    }
    
    pelicula = db.execute(
        select(Pelicula)
        .where(Pelicula.id == pelicula_id)
        .options(joinedload(Pelicula.genero))
    ).scalar_one_or_none()
    
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    generos = db.execute(select(Genre)).scalars().all()
    
    # validaciones
    if not titulo or not titulo.strip():
        errors.append("El título es obligatorio.")

    genero_id_value = None
    
    if genero_id and genero_id.strip():
        try:
            genero_id_value = int(genero_id.strip())
            
            if genero_id_value < 1:
                errors.append("El id del género debe ser un número positivo.")
            genero = db.execute(select(Genre).where(Genre.id == genero_id_value)).scalar_one_or_none()
            if genero is None:
                errors.append("El género especificado no existe.")
        except ValueError:
            errors.append("El id del género tiene que ser un entero válido.")
    else:
        errors.append("El id del género es requerido")

    duracion_value = None
    if duracion and duracion.strip():
        try:
            duracion_value = int(duracion.strip())
            
            if duracion_value < 1:
                errors.append("La duración debe ser un número positivo.")
        except ValueError:
            errors.append("La duración tiene que ser un entero válido.")
    else:
        errors.append("La duración es obligatoria.")

    # procesar disponible: '' -> False, 'on' o 'true' -> True
    disponible_val = disponible in ("on", "true")

    if errors:
        return templates.TemplateResponse(
            "peliculas/form.html",
            {"request": request, "pelicula": pelicula, "errors": errors, "form_data": form_data, "generos": generos}
        )

    try:
        pelicula.titulo = titulo.strip()
        pelicula.genero_id = genero_id_value
        pelicula.duracion = duracion_value
        pelicula.disponible = disponible_val
        
        db.commit()
        db.refresh(pelicula)

        return RedirectResponse(url=f"/peliculas/{pelicula.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar la película: {str(e)}")
        return templates.TemplateResponse(
            "peliculas/form.html",
            {"request": request, "pelicula": pelicula, "errors": errors, "form_data": form_data, "generos": generos}
        )


# eliminar película
@router.post("/{pelicula_id}/delete", response_class=HTMLResponse)
def delete_pelicula(request: Request, pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.execute(select(Pelicula).where(Pelicula.id == pelicula_id)).scalar_one_or_none()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="404 - Película no encontrada")
    try:
        db.delete(pelicula)
        db.commit()
        return RedirectResponse("/peliculas", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la película: {str(e)}")
