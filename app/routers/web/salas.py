from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import SalaORM


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/salas", tags=["web"])

# listar salas (http://localhost:8000/salas)
@router.get("", response_class=HTMLResponse)
def list_salas(request: Request, db: Session = Depends(get_db)):
    salas = db.execute(select(SalaORM)).scalars().all()
    
    return templates.TemplateResponse(
        "salas/list.html",
        {"request": request, "salas": salas}
    )
    
# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "salas/form.html",
        {"request": request, "sala": None}
    )
    
# crear nueva sala
@router.post("/new", response_class=HTMLResponse)
def create_sala(
    request: Request, 
    nombre: str = Form(...),
    capacidad: str = Form(...), 
    tipo: str = Form(...),
    precio: str = Form(...),
    db: Session = Depends(get_db)
    ):
    
    errors = []
    form_data = {
        "nombre": nombre,
        "capacidad": capacidad,
        "tipo": tipo,
        "precio": precio
    }   
    
    # Validaciones
    if not nombre or not nombre.strip():
        errors.append("El nombre es obligatorio.")
    
    if capacidad and capacidad.strip():
        try:
            capacidad_value = int(capacidad)
            if capacidad_value <= 0:
                errors.append("La capacidad debe ser un número positivo.")
        except ValueError:
            errors.append("La capacidad debe ser un número entero válido.")
    elif not capacidad or not capacidad.strip():
        errors.append("La capacidad es obligatoria.")
     
    if tipo and tipo.strip():
        tipo_value = tipo.strip().upper()
        if tipo_value not in ("2D", "3D", "IMAX"):
            errors.append("El tipo no es válido.")
    elif not tipo or not tipo.strip():
        errors.append("El tipo es obligatorio.")
    
    if precio and precio.strip():
        try:
            precio_value = float(precio)
            if precio_value < 0:
                errors.append("El precio no puede ser negativo.")
        except ValueError:
            errors.append("El precio debe ser un número válido.")
    elif not precio or not precio.strip():
        errors.append("El precio es obligatorio.")
        
    # Si hay errores, volver al formulario con mensajes de error
    if errors:
        return templates.TemplateResponse(
            "salas/form.html",
            {
                "request": request,
                "sala": None,
                "errors": errors,
                "sala": form_data
            }
        )
        
    try:
        nueva_sala = SalaORM(
            nombre=nombre.strip(),
            capacidad=capacidad_value,
            tipo=tipo_value,
            precio=precio_value
        )
        db.add(nueva_sala)
        db.commit()
        db.refresh(nueva_sala)
        
        # Redirigir a la pantalla de detalle de la sala creada
        return RedirectResponse(
            url=f"/salas/{nueva_sala.id}",
            status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear la sala: {str(e)}. Inténtalo de nuevo.")
        return templates.TemplateResponse(
            "salas/form.html",
            {
                "request": request,
                "sala": None,
                "errors": errors,
                "form_data": form_data
            }
        )
    
    
    
# detalle de sala (http://localhost:8000/salas/3)
@router.get("/{sala_id}", response_class=HTMLResponse)
def salas_detail(request: Request, sala_id: int, db: Session = Depends(get_db)):
    sala= db.execute(select(SalaORM).where(SalaORM.id == sala_id)).scalar_one_or_none()
    
    if sala is None:
        raise HTTPException(status_code=404, detail="404 - Sala no encontrada")
    
    return templates.TemplateResponse(
        "salas/detail.html",
        {"request": request, "sala": sala}
    )
    
# mostrar formulario editar
@router.get("/{sala_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, sala_id: int, db: Session = Depends(get_db)):
    # obtener sala por id
    sala = db.execute(select(SalaORM).where(SalaORM.id == sala_id)).scalar_one_or_none()
    
    # lanzar error 404 si no existe canción
    if sala is None:
        raise HTTPException(status_code=404, detail="404 -  Sala no encontrada")
    
    return templates.TemplateResponse(
        "salas/form.html",
        {"request": request, "sala": sala}
    )
    
# editar sala existente
@router.post("/{sala_id}/edit", response_class=HTMLResponse)
def update_sala(
    request: Request,
    sala_id: int,
    nombre: str = Form(...),
    capacidad: str = Form(...), 
    tipo: str = Form(...),
    precio: str = Form(...),
    db: Session = Depends(get_db)
   
):
    sala = db.execute(select(SalaORM).where(SalaORM.id == sala_id)).scalar_one_or_none()
    
    if sala is None:
        raise HTTPException(status_code=404, detail="404 - Sala no encontrada")
    
    errors = []
    form_data = {
        "nombre": nombre,
        "capacidad": capacidad,
        "tipo":  tipo,
        "precio": precio
    }
    
    if not nombre or not nombre.strip():
        errors.append("El nombre es requerido")
    
    if capacidad and capacidad.strip():
        try:
            capacidad_value = int(capacidad)
            if capacidad_value < 0:
                errors.append("La capacidad debe ser un número positivo")
        except ValueError:
            errors.append("La capacidad debe ser un número válido")
    elif not capacidad or not capacidad.strip():
        errors.append("La capacidad es requerida")
    
    if tipo and tipo.strip():    
        tipo_value = tipo.strip().upper()
        print(tipo_value)
        if tipo_value not in ("2D", "3D", "IMAX"):
            errors.append("El tipo no es válido.")
    elif not tipo or not tipo.strip():
        errors.append("El tipo es requerido")
        
    if precio and precio.strip():    
        try:
            precio_value = float(precio)
            if precio_value < 0:
                errors.append("El precio no puede ser negativo.")
        except ValueError:
            errors.append("El precio debe ser un número válido.")   
    elif not precio or not precio.strip():
        errors.append("El precio es requerido")
    
    if errors:
        return templates.TemplateResponse(
            "salas/form.html",
            {"request": request, "sala": sala, "errors": errors, "form_data": form_data}
        )
    
    try:
        sala.nombre = nombre.strip()
        sala.capacidad = capacidad_value
        sala.tipo = tipo_value
        sala.precio = precio_value

        db.commit()
        db.refresh(sala)
        
        return RedirectResponse(url=f"/salas/{sala.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar la sala: {str(e)}")
        return templates.TemplateResponse(
            "salas/form.html",
            {"request": request, "sala": sala, "errors": errors, "form_data": form_data}
        )  
    
# eliminar sala
@router.post("/{sala_id}/delete", response_class=HTMLResponse)
def delete_song(request: Request, sala_id: int, db: Session = Depends(get_db)):
    sala = db.execute(select(SalaORM).where(SalaORM.id == sala_id)).scalar_one_or_none()
    
    if sala is None:
        raise HTTPException(status_code=404, detail="404 - Sala no encontrada")
    
    # eliminar canción
    try:
        db.delete(sala)
        db.commit()
        
        return RedirectResponse("/salas", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la canción: {str(e)}")