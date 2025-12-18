from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.models import Venta, MetodoPago, Horario


# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/ventas", tags=["web"])

#Listar ventas

@router.get("", response_class=HTMLResponse)
def list_artists(request: Request, db: Session = Depends(get_db)):
    ventas = db.execute(select(Venta)).scalars().all()

    return templates.TemplateResponse(
        "ventas/list.html",
        {"request": request, "ventas": ventas}
    )



@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request, db: Session = Depends(get_db)):
    horarios = db.execute(select(Horario)).scalars().all()
    
    return templates.TemplateResponse(
        "ventas/form.html",
        {"request": request, "venta": None, "horarios": horarios, "metodo_pago": MetodoPago}      
    )
    

@router.post("/new", response_class=HTMLResponse)
def create_venta(
    request:Request,
    horario_id: str = Form(...),
    precio_total: str = Form(...),
    cantidad: str = Form(...),
    metodo_pago: str = Form(...),
    db:Session = Depends(get_db)
    
):
    errors = []
    form_data = {
        "horario_id": horario_id,
        "precio_total": precio_total,
        "cantidad": cantidad,
        "metodo_pago": metodo_pago
    }
    
    horarios = db.execute(select(Horario)).scalars().all()
    
    horario_id_value = None
    if horario_id and horario_id.strip():
        try:
            horario_id_value = int(horario_id.strip())
            if horario_id_value < 1:
                errors.append("El id del horario tiene que ser un numero positivo")
            horario = db.execute(select(Horario).where(Horario.id == horario_id_value)).scalar_one_or_none()
            if not horario:
                errors.append("El horario seleccionado no existe")
        except ValueError:
            errors.append("El id del horario tiene que ser un número válido")
    else:
        errors.append("El id del artista es requerido")
    
    precio_total_value = None
    if precio_total and precio_total.strip():
        try:
            precio_total_value = float(precio_total.strip())
            if precio_total_value < 0:
                errors.append("El precio debe ser un numero positivo")
        except ValueError:
            errors.append("El precio debe ser un numero valido")
    else:
        errors.append("El precio es requerido")
    
    cantidad_value = None
    if cantidad and cantidad.strip():
        try:
            cantidad_value = int(cantidad.strip())
            if cantidad_value < 0:
                errors.append("La cantidad debe ser un numero positivo")
        except ValueError:
            errors.append("La cantidad debe ser un numero valido")
    
    
         
    metodo_pago_value = None
    try:
        metodo_pago_value = MetodoPago(metodo_pago)
    except ValueError:
        errors.append("El metodo de pago debe ser efectivo o tarjeta")
    
    
    if errors:
        return templates.TemplateResponse(
            "ventas/form.html",
            {"request": request, "venta": None, "horarios": horarios,"metodos_pagos": MetodoPago,"errors": errors, "form_data": form_data}
        )
    
    try:
        venta = Venta(
            
            horario_id =  horario_id_value,
            precio_total =  precio_total_value,
            cantidad = cantidad_value,
            metodo_pago =  metodo_pago_value
            )
        
        db.add(venta)
        db.commit()
        db.refresh(venta)
        
        return RedirectResponse(url=f"/ventas/{venta.id}", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear la venta: {str(e)}")
        
        return templates.TemplateResponse(
            "ventas/form.html",
            {"request": request,"venta": None, "horarios": horarios, "metodos_pagos": MetodoPago, errors: errors, "form_data": form_data}
        )
    
@router.get("/{venta_id}", response_class=HTMLResponse)
def venta_detail(request: Request, venta_id: int, db: Session = Depends(get_db)):
    venta = db.execute(
        select(Venta)
        .where(Venta.id == venta_id)
        .options(joinedload(Venta.horario))
    ).scalar_one_or_none()
    
    if venta is None:
        raise HTTPException(status_code=404, detail="Venta no encotrada")
    
    return templates.TemplateResponse(
        "ventas/detail.html",
        {"request": request, "venta": venta}
    )


@router.get("/{venta_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, venta_id: int, db:Session = Depends(get_db)):
    venta = db.execute(
        select(Venta)
        .where(Venta.id == venta_id)
        .options(joinedload(Venta.horario))
    ).scalar_one_or_none()
    
    if venta is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    horarios = db.execute(select(Horario)).scalars().all()
    
    return templates.TemplateResponse(
            "ventas/form.html",
            {"request": request,"venta": venta, "horarios": horarios, "metodos_pagos": MetodoPago}
        )


@router.post("/{venta_id}/edit", response_class=HTMLResponse)
def update_venta(
    request: Request,
    venta_id: int,
    horario_id: str = Form(...),
    precio_total: str = Form(...),
    cantidad: str = Form(...),
    metodo_pago: str = Form(...),
    db: Session = Depends(get_db) 
):
    venta = db.execute(
        select(Venta)
        .where(Venta.id == venta_id)
        .options(joinedload(Venta.horario))
    ).scalar_one_or_none()
    
    
    if venta is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    errors = []
    form_data = {
        "horario_id": horario_id,
        "precio_total": precio_total,
        "cantidad": cantidad,
        "metodo_pago": metodo_pago
    }
    
    horarios = db.execute(select(Horario)).scalars().all()
    
    horario_id_value = None
    if horario_id and horario_id.strip():
        try:
            horario_id_value = int(horario_id.strip())
            if horario_id_value < 1:
                errors.append("El id del horario tiene que ser un numero positivo")
            horario = db.execute(select(Horario).where(Horario.id == horario_id_value)).scalar_one_or_none()
            if not horario:
                errors.append("El horario seleccionado no existe")
        except ValueError:
            errors.append("El id del horario tiene que ser un número válido")
    else:
        errors.append("El id del horario es requerido")
    
    precio_total_value = None
    if precio_total and precio_total.strip():
        try:
            precio_total_value = float(precio_total.strip())
            if precio_total_value < 0:
                errors.append("El precio debe ser un numero positivo")
        except ValueError:
            errors.append("El precio debe ser un numero valido")
    else:
        errors.append("El precio es requerido")
    
    cantidad_value = None
    if cantidad and cantidad.strip():
        try:
            cantidad_value = int(cantidad.strip())
            if cantidad_value < 0:
                errors.append("La cantidad debe ser un numero positivo")
        except ValueError:
            errors.append("La cantidad debe ser un numero valido")
    
    
         
    metodo_pago_value = None
    try:
        metodo_pago_value = MetodoPago(metodo_pago)
    except ValueError:
        errors.append("El metodo de pago debe ser efectivo o tarjeta")
    
    
    if errors:
        return templates.TemplateResponse(
            "ventas/form.html",
            {"request": request, "venta": venta, "horarios": horarios,"metodos_pagos": MetodoPago,"errors": errors, "form_data": form_data}
        )
    
    try:
        # ACTUALIZAR la venta existente en lugar de crear una nueva
        venta.horario_id = horario_id_value
        venta.precio_total = precio_total_value
        venta.cantidad = cantidad_value
        venta.metodo_pago = metodo_pago_value
        
        db.commit()
        db.refresh(venta)
        
        return RedirectResponse(url=f"/ventas/{venta.id}", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar la venta: {str(e)}")
        
        return templates.TemplateResponse(
            "ventas/form.html",
            {"request": request,"venta": venta, "horarios": horarios, "metodos_pagos": MetodoPago, "errors": errors, "form_data": form_data}
        )