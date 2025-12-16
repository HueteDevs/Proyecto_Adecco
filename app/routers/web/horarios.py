from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.models import Horario, SalaORM

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/horarios", tags=["web"])


# Listar horarios
@router.get("", response_class=HTMLResponse)
def list_horarios(request: Request, db: Session = Depends(get_db)):
    horarios = db.execute(select(Horario).options(joinedload(Horario.sala))).scalars().all()

    return templates.TemplateResponse(
        "horarios/list.html",
        {"request": request, "horarios": horarios}
    )


# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request, db: Session = Depends(get_db)):
    salas = db.execute(select(SalaORM)).scalars().all() 
    
    return templates.TemplateResponse(
        "horarios/form.html",
        {"request": request, "horario": None, "salas": salas}
    )



# crear nuevo horario
@router.post("/new", response_class=HTMLResponse)
def create_horario(
    request: Request,
    pelicula_id: str = Form(...),
    sala_id: str = Form(...),
    hora: str = Form(...),
    disponible: str = Form(""),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "pelicula_id": pelicula_id,
        "sala_id": sala_id,
        "hora": hora,
        "disponible": disponible,
    }
    
    salas = db.execute(select(SalaORM)).scalars().all()

    # validaciones
    try:
        peli_val = int(pelicula_id)
        if peli_val < 1:
            errors.append("El id de la pelicula debe ser un número positivo.")
    except Exception:
        errors.append("El id de la pelicula tiene que ser un entero válido.")

    sala_id_value = None
    
    if sala_id and sala_id.strip():
        try:
            sala_id_value = int(sala_id.strip())
            
            if sala_id_value < 1:
                errors.append("El id de la sala debe ser un número positivo.")
            sala = db.execute(select(SalaORM).where(SalaORM.id == sala_id_value)).scalar_one_or_none()
        except ValueError:
            errors.append("El id de la sala tiene que ser un entero válido.")
    else:
        errors.append("El id de la sala es requerido")

    if not hora or not hora.strip():
        errors.append("La hora es obligatoria.")

    # procesar disponible: '' -> None, 'true' -> True, 'false' -> False
    if disponible == "true":
        disponible_val = True
    elif disponible == "false":
        disponible_val = False
    else:
        disponible_val = None


    try:
        horario = Horario(
            pelicula_id=peli_val,
            sala_id=sala_id_value,
            hora=hora.strip(),
            disponible=disponible_val if disponible_val is not None else False
        )
        db.add(horario)
        db.commit()
        db.refresh(horario)

        return RedirectResponse(url=f"/horarios/{horario.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el horario: {str(e)}")
        return templates.TemplateResponse(
            "horarios/form.html",
            {"request": request, "horario": None, "errors": errors, "form_data": form_data}
        )


# detalle de horario
@router.get("/{horario_id}", response_class=HTMLResponse)
def horario_detail(request: Request, horario_id: int, db: Session = Depends(get_db)):
    horario = db.execute(select(Horario).where(Horario.id == horario_id)
                .options(joinedload(Horario.sala))).scalar_one_or_none()
    
    if horario is None:
        raise HTTPException(status_code=404, detail="404 - Horario no encontrado")
    return templates.TemplateResponse(
        "horarios/detail.html",
        {"request": request, "horario": horario}
        )


# mostrar formulario editar
@router.get("/{horario_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, horario_id: int, db: Session = Depends(get_db)):
    horario = db.execute(select(Horario).where(Horario.id == horario_id)
                         .options(joinedload(Horario.sala))).scalar_one_or_none()
    if horario is None:
        raise HTTPException(status_code=404, detail="404 - Horario no encontrado")
    salas = db.execute(select(SalaORM)).scalars().all()
    return templates.TemplateResponse("horarios/form.html", {"request": request, "horario": horario, "salas": salas})


# editar horario existente
@router.post("/{horario_id}/edit", response_class=HTMLResponse)
def update_horario(
    request: Request,
    horario_id: int,
    pelicula_id: str = Form(...),
    sala_id: str = Form(...),
    hora: str = Form(...),
    disponible: str = Form(""),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "pelicula_id": pelicula_id,
        "sala_id": sala_id,
        "hora": hora,
        "disponible": disponible,
    }
    
    horario = db.execute(
        select(Horario)
        .where(Horario.id == horario_id)
        .options(joinedload(Horario.sala))
    ).scalar_one_or_none()
    
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    salas = db.execute(select(SalaORM)).scalars().all()
    
    # validaciones
    try:
        peli_val = int(pelicula_id)
        if peli_val < 1:
            errors.append("El id de la pelicula debe ser un número positivo.")
    except Exception:
        errors.append("El id de la pelicula tiene que ser un entero válido.")

    sala_id_value = None
    
    if sala_id and sala_id.strip():
        try:
            sala_id_value = int(sala_id.strip())
            
            if sala_id_value < 1:
                errors.append("El id de la sala debe ser un número positivo.")
            sala = db.execute(select(SalaORM).where(SalaORM.id == sala_id_value)).scalar_one_or_none()
        except ValueError:
            errors.append("El id de la sala tiene que ser un entero válido.")
    else:
        errors.append("El id de la sala es requerido")

    if not hora or not hora.strip():
        errors.append("La hora es obligatoria.")

    # procesar disponible: '' -> None, 'true' -> True, 'false' -> False
    if disponible == "true":
        disponible_val = True
    elif disponible == "false":
        disponible_val = False
    else:
        disponible_val = None

    if errors:
        return templates.TemplateResponse(
            "horarios/form.html",
            {"request": request, "horario": horario, "errors": errors, "form_data": form_data, "salas": salas}
        )

    try:
        horario.pelicula_id = peli_val
        horario.sala_id = sala_id_value
        horario.hora = hora.strip()
        horario.disponible = disponible_val if disponible_val is not None else False
        
        db.commit()
        db.refresh(horario)

        return RedirectResponse(url=f"/horarios/{horario.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar el horario: {str(e)}")
        return templates.TemplateResponse(
            "horarios/form.html",
            {"request": request, "horario": horario, "errors": errors, "form_data": form_data, "salas": salas}
        )

# eliminar horario
@router.post("/{horario_id}/delete", response_class=HTMLResponse)
def delete_horario(request: Request, horario_id: int, db: Session = Depends(get_db)):
    horario = db.execute(select(Horario).where(Horario.id == horario_id)).scalar_one_or_none()
    if horario is None:
        raise HTTPException(status_code=404, detail="404 - Horario no encontrado")
    try:
        db.delete(horario)
        db.commit()
        return RedirectResponse("/horarios", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el horario: {str(e)}")
